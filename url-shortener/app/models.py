
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class URLRecord:
    long_url: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    clicks: int = 0
    expires_at: Optional[str] = None  # ISO format string or None
    owner: Optional[str] = None

    def to_dict(self):
        return {
            "long_url": self.long_url,
            "created_at": self.created_at,
            "clicks": self.clicks,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            long_url=data["long_url"],
            created_at=data.get("created_at", datetime.now().strftime('%Y-%m-%dT%H:%M:%S')),
            clicks=data.get("clicks", 0),
            
        )


