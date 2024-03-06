import asyncio
from prisma import Prisma
from user import User
from util import glog

async def find_one_user_core(db: Prisma, userId: str) -> User:
	bingo = await db.user.find_unique(
			where={
				'user_id': userId
			}
		)
	# glog(f'bingo => {bingo}')
	if bingo == None:
		return None
	return User(
		user_id=bingo.user_id, 
		user_role=bingo.user_role,
		summary=bingo.summary,
		lastmood_timestamp=bingo.lastmood_timestamp,
		lastresponse_timestamp=bingo.lastresponse_timestamp
		)

async def find_one_user(userId: str) -> User:
	async with Prisma() as db:
		return await find_one_user_core(db, userId)

# async def main() -> None:
# 	ans = await find_one_user('123')
# 	if ans != None:
# 		glog(f' => {ans}')

# if __name__ == '__main__':
#     asyncio.run(main())