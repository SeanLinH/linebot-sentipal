from dataclasses import dataclass, field
from src.prisma.util import nowTimeStampISO

@dataclass(kw_only=True)
class UserApi:
	user_id: str
	user_api: str
	group_id: list[str] = field(default_factory=list)
	timestamp: str = field(init=False, default_factory=nowTimeStampISO)