from dataclasses import dataclass, field
from src.prisma.util import nowTimeStampISO

@dataclass(kw_only=True)
class UserApi:
	user_id: str
	user_api: str
	timestamp: str = field(init=False, default_factory=nowTimeStampISO)