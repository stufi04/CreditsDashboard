from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Message:
    message_id: int
    timestamp: str
    credits_used: float
    report_name: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}