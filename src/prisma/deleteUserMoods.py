import asyncio
from prisma import Prisma
from src.prisma.user import User
from src.prisma.util import glog

async def delete_user_moods_core(db:Prisma, user_id: str) -> int:
	total = await db.mood.delete_many(
		where={
			'user_id': user_id
		}
	)
	return total

async def delete_user_moods(user_id: str) -> int:
	async with Prisma() as db:
		return await delete_user_moods_core(db, user_id)
	

# async def main() -> None:
# 	user_id = '2234'
# 	await delete_user_moods(user_id)
# 	glog(f'user_id:{user_id} ==> Your record has been cleared!')

# if __name__ == '__main__':
#     asyncio.run(main())