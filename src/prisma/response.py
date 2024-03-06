from dataclasses import dataclass, field
from util import nowTimeStampISO

@dataclass(kw_only=True)
class Response:
	user_id: str = None
	group_id: str = None
	ai_text: str
	timestamp: str = field(init=False, default_factory=nowTimeStampISO)