from datetime import datetime, timezone

clr_Off = "\x1b[0m"

clr_Black = "\x1b[0;30m"
clr_Red = "\x1b[0;31m"
clr_Green = "\x1b[0;32m"
clr_Yellow = "\x1b[0;33m"
clr_Blue = "\x1b[0;34m"
clr_Purple = "\x1b[0;35m"
clr_Cyan = "\x1b[0;36m"
clr_White = "\x1b[0;37m"

def glog(dbgMsg: str) -> None:
	print(f'{clr_Cyan}{logTimeStampPrefix()}|{clr_Off} {dbgMsg}')

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