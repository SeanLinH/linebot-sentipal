from dataclasses import dataclass, field
from src.prisma.util import nowTimeStampISO

@dataclass(kw_only=True)
class Response:
	user_id: str = None
	group_id: str = None
	ai_text: str
	aim_to_mood_timestamp: str = None
	timestamp: str = field(init=False, default_factory=nowTimeStampISO)