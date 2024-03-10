from dataclasses import dataclass, field
from src.prisma.user import User

@dataclass(kw_only=True)
class Group:
	group_id: str
	groupUsers: list[User] = field(default_factory=list)
	belongToUserApiId: str = None