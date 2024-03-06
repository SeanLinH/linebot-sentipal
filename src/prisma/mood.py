from dataclasses import dataclass, field
from src.prisma.util import nowTimeStampISO

@dataclass(kw_only=True)
class Mood:
	user_id: str
	group_id: str = None
	user_text: str
	user_mood: str = 0
	mood_score: int = 0
	stable_score: int = 0
	engage: int = 0
	timestamp: str = field(init=False, default_factory=nowTimeStampISO)
