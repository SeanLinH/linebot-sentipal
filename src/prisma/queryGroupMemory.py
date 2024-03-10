import asyncio
from prisma import Prisma
from datetime import datetime, timedelta
from src.prisma.util import glog, appendLF, clr_Yellow, clr_Red, clr_Off

async def query_group_memory_core(db: Prisma, group_id: str, user_id: str, includeResponse: bool, days: int) -> tuple[int, str]:
	if user_id == None:
		where4MoodsQuery={
			'group_id': group_id,
			'timestamp' : {
				'gte': datetime.now() - timedelta(days)
			}
		}
	else:
		where4MoodsQuery={
			'group_id': group_id,
			'user_id': user_id,
			'timestamp' : {
				'gte': datetime.now() - timedelta(days)
			},
		}
	moods = await db.mood.find_many(
		skip=0,
		take=2000,
		where=where4MoodsQuery,
		order={
			'timestamp': 'desc'
		},
		include={
			'hasResponse': True,
		}
	)
	glog(f"There ate {len(moods)} matched records in group memory.")
	lineCount=0
	user_ids=[]
	ans = ""
	for mood in reversed(moods):
		if not mood.user_id in user_ids:
			user_ids.append(mood.user_id)
			userIndex = len(user_ids)
		else:
			userIndex = user_ids.index(mood.user_id)
		
		if includeResponse:
			ans += f"用戶{userIndex}: {mood.user_text}"
			ans = appendLF(ans)
			lineCount += 1
			if mood.hasResponse != None:
				ans += f"SentiPal: {mood.hasResponse.ai_text}"
				ans = appendLF(ans)
				lineCount += 1
		else:
			ans += f"{mood.user_text}"
			ans = appendLF(ans)
			lineCount += 1
	return lineCount, ans


async def query_group_memory(group_id: str, user_id: str = None, includeResponse: bool = True, days: int = 7) -> tuple[int, str]:
	async with Prisma() as db:
		return await query_group_memory_core(db, group_id, user_id, includeResponse, days=7)

# async def main() -> None:
# 	group_id='Cfde2308a4ab86354d3ad36f0e18720f8'
# 	total, ans = await query_group_memory(group_id)
# 	if total > 0:
# 		glog(f'group_id:{group_id} mem =>\n\ttotal:{clr_Yellow}{total}{clr_Off}\n\tmem:{clr_Yellow}{ans}{clr_Off}')
# 	else:
# 		glog(f'group_id:{group_id} mem => {clr_Red}empty!{clr_Off}')

# if __name__ == '__main__':
#     asyncio.run(main())