import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any

class AuditLogger:
    _instance = None

    def __new__(cls, log_path: str = "audit_compliance.log"):
        if cls._instance is None:
            cls._instance = super(AuditLogger, cls).__new__(cls)
            cls._instance._initialize_logger(log_path)
        return cls._instance

    def _initialize_logger(self, log_path: str) -> None:
        self.logger = logging.getLogger("prism_compliance_audit")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        
        if not self.logger.handlers:
            handler = logging.FileHandler(log_path)
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)

    def log_decision(self, input_data: Dict[str, Any], output_data: Dict[str, Any]) -> str:
        transaction_id = str(uuid.uuid4())
        audit_entry = {
            "transaction_id": transaction_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "automated_credit_decision",
            "request_payload": input_data,
            "model_decision": output_data
        }
        self.logger.info(json.dumps(audit_entry))
        return transaction_id