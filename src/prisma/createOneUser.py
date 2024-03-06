import asyncio
from prisma import Prisma
from user import User
from util import glog

async def create_one_user_core(db:Prisma, user: User) -> User:
	newUser = await db.user.create(
		data={
			'user_id': user.user_id,
			'user_role': 'general'
		}
	)
	return newUser

async def create_one_user(user: User) -> User:
	async with Prisma() as db:
		return await create_one_user_core(db, user)
	

# async def main() -> None:
# 	newU = User(user_id='2234')
# 	nseUserDb = await create_one_user(newU)
# 	if nseUserDb != None:
# 		glog(f' create User success => {nseUserDb}')
# 	else:
# 		glog(f'Fail create user {newU}')

# if __name__ == '__main__':
#     asyncio.run(main())