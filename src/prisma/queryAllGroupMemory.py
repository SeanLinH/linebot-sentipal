import asyncio
from prisma import Prisma
from datetime import datetime, timedelta
from src.prisma.util import glog, appendLF, clr_Yellow, clr_Red, clr_Off
from langchain.memory import ChatMessageHistory
import os

async def query_all_group_memory_core(db: Prisma, group_id: str, days: int) -> tuple[int, str]:
    # history = ChatMessageHistory()
    moods = await db.mood.find_many(
        skip=0,
		# take=2000,
		where={
			'group_id': group_id,
			'timestamp' : {
				'gte': datetime.now() - timedelta(2)
			},
		},
		order={
			'timestamp': 'desc'
		}
    )
    ans = ''
    glog(f"There ate {len(moods)} matched records in memory.")
    for mood in reversed(moods):
        # history.add_user_message(mood.user_text)
        ans += f'"{mood.user_text}", '
        ans = appendLF(ans)
    return len(moods), ans

async def query_all_group_memory(group_id: str, days: int) -> tuple[int, str]:
	async with Prisma() as db:
		return await query_all_group_memory_core(db, group_id, days=2)

# async def main() -> None:
# 	user_id='U7c0b638081d6027c5bd164a8ae23d4d1'
# 	total, ans = await query_user_memory(user_id)
# 	if total > 0:
# 		glog(f'user_id:{user_id} mem =>\n\ttotal:{clr_Yellow}{total}{clr_Off}\n\tmem:{clr_Yellow}{ans}{clr_Off}')
# 	else:
# 		glog(f'user_id:{user_id} mem => {clr_Red}empty!{clr_Off}')

# if __name__ == '__main__':
#     asyncio.run(main())