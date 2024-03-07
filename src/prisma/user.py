from dataclasses import dataclass, field

@dataclass(kw_only=True)
class User:
	user_id: str
	user_role: str = 'general'
	summary: str = None
	lastmood_timestamp: str = None
	lastresponse_timestamp: str = None