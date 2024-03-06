from datetime import datetime, timezone

def glog(dbgMsg: str) -> None:
	print(f'{logTimeStampPrefix()}| {dbgMsg}')

def logTimeStampPrefix() -> str:
	now = datetime.now()
	t = int(now.time().microsecond/1000.0)
	iso_date = now.replace(microsecond=0,tzinfo=None).isoformat()
	logPrefix = f"{iso_date}.{t}"
	return logPrefix

def nowTimeStampISO() -> str:
	now = datetime.now(timezone.utc)
	t = int(now.time().microsecond/1000.0)
	iso_date = now.replace(microsecond=0,tzinfo=None).isoformat()
	iso_date2 = f"{iso_date}.{t}Z"
	# print(f"nowTimeStampISO => {iso_date2}")
	return iso_date2

# nowTimeStampISO()