from __future__ import annotations

from datetime import datetime, timezone

from practical_chat_agent.connectors.delivery.base import DeliveryConnector
from practical_chat_agent.core.enums import ActionStatus, Platform
from practical_chat_agent.core.models import ActionExecutionRecord, AuditLogEntry
from practical_chat_agent.services.policy import PolicyEngine
from practical_chat_agent.storage.repositories.base import ActionRepository, AgentRepository, AuditRepository


class ActionDeliveryService:
    """Coordinates human approval, official-platform delivery, and audit logging."""

    def __init__(
        self,
        *,
        action_repository: ActionRepository,
        agent_repository: AgentRepository,
        audit_repository: AuditRepository,
        delivery_connectors: dict[Platform, DeliveryConnector],
        policy_engine: PolicyEngine,
    ) -> None:
        self.action_repository = action_repository
        self.agent_repository = agent_repository
        self.audit_repository = audit_repository
        self.delivery_connectors = delivery_connectors
        self.policy_engine = policy_engine

    def approve(self, *, action_id: str) -> ActionExecutionRecord:
        action = self._require_action(action_id)
        if action.status == ActionStatus.SENT:
            raise ValueError(f"Action is already sent: {action_id}")
        if action.status == ActionStatus.POLICY_BLOCKED:
            raise ValueError(f"Action is policy-blocked and cannot be approved: {action_id}")
        if action.status == ActionStatus.DRAFT_ONLY:
            raise ValueError(f"Action is draft-only and cannot be approved for sending: {action_id}")

        now = datetime.now(timezone.utc)
        updated = action.model_copy(
            update={
                "status": ActionStatus.APPROVED,
                "requires_approval": False,
                "approved_at": action.approved_at or now,
                "updated_at": now,
            },
        )
        stored = self.action_repository.update(updated)
        self._audit(
            action=stored,
            audit_action="action_approve",
            status="approved",
            details={"action_id": stored.action_id},
        )
        return stored

    def send(self, *, action_id: str) -> ActionExecutionRecord:
        action = self._require_action(action_id)
        if action.status == ActionStatus.SENT:
            return action
        if action.status == ActionStatus.PENDING_APPROVAL:
            raise ValueError(f"Action requires approval before send: {action_id}")
        if action.status == ActionStatus.POLICY_BLOCKED:
            raise ValueError(f"Action is policy-blocked and cannot be sent: {action_id}")
        if action.status == ActionStatus.DRAFT_ONLY:
            raise ValueError(f"Action is draft-only and cannot be sent: {action_id}")
        if action.status not in {ActionStatus.APPROVED, ActionStatus.FAILED}:
            raise ValueError(f"Action status does not allow send: {action.status.value}")

        action = self._enforce_send_policy(action)
        connector = self.delivery_connectors.get(action.platform)
        if connector is None:
            raise ValueError(f"No delivery connector registered for platform: {action.platform.value}")

        now = datetime.now(timezone.utc)
        try:
            result = connector.send_text(action)
        except Exception as exc:  # noqa: BLE001
            failed = action.model_copy(
                update={
                    "status": ActionStatus.FAILED,
                    "delivery_connector_name": getattr(connector, "connector_name", None),
                    "error_message": str(exc),
                    "updated_at": now,
                },
            )
            stored = self.action_repository.update(failed)
            self._audit(
                action=stored,
                audit_action="action_send",
                status="failed",
                details={
                    "action_id": stored.action_id,
                    "error": str(exc),
                    "delivery_connector_name": stored.delivery_connector_name,
                },
            )
            raise

        sent = action.model_copy(
            update={
                "status": ActionStatus.SENT,
                "delivery_connector_name": result.connector_name,
                "delivery_response": result.model_dump(mode="json"),
                "error_message": None,
                "sent_at": now,
                "updated_at": now,
            },
        )
        stored = self.action_repository.update(sent)
        self._audit(
            action=stored,
            audit_action="action_send",
            status="sent",
            details={
                "action_id": stored.action_id,
                "delivery_connector_name": result.connector_name,
                "provider_message_id": result.provider_message_id,
            },
        )
        return stored

    def _require_action(self, action_id: str) -> ActionExecutionRecord:
        action = self.action_repository.get(action_id)
        if action is None:
            raise ValueError(f"Unknown action: {action_id}")
        return action

    def _enforce_send_policy(self, action: ActionExecutionRecord) -> ActionExecutionRecord:
        agent = self.agent_repository.get(action.agent_id)
        if agent is None:
            raise ValueError(f"Unknown agent for action: {action.agent_id}")
        decision = self.policy_engine.review_outbound_action(
            action=action,
            agent=agent,
            event=None,
        )
        if decision.allowed and not decision.draft_only:
            if decision != action.policy_decision:
                now = datetime.now(timezone.utc)
                action = action.model_copy(
                    update={
                        "policy_decision": decision,
                        "updated_at": now,
                    },
                )
                return self.action_repository.update(action)
            return action

        now = datetime.now(timezone.utc)
        blocked_status = ActionStatus.DRAFT_ONLY if decision.draft_only else ActionStatus.POLICY_BLOCKED
        blocked = action.model_copy(
            update={
                "status": blocked_status,
                "policy_decision": decision,
                "updated_at": now,
            },
        )
        stored = self.action_repository.update(blocked)
        self._audit(
            action=stored,
            audit_action="action_send",
            status=blocked_status.value,
            details={
                "action_id": stored.action_id,
                "policy_decision": decision.model_dump(mode="json"),
            },
        )
        raise ValueError(f"Policy blocked send: {decision.reason}")

    def _audit(
        self,
        *,
        action: ActionExecutionRecord,
        audit_action: str,
        status: str,
        details: dict[str, object],
    ) -> None:
        self.audit_repository.add(
            AuditLogEntry(
                agent_id=action.agent_id,
                action=audit_action,
                status=status,
                details=details,
            ),
        )
