import asyncio
from prisma import Prisma
from src.prisma.user import User
from src.prisma.util import glog

"""

"""


async def update_one_user_core(db:Prisma, user_id: str, data: any) -> User:
	updatedUser = await db.user.update(
		where={
			'user_id': user_id,
		},
		data=data
	)
	return User(
		user_id    = updatedUser.user_id,
		user_role  = updatedUser.user_role,
		summary    = updatedUser.summary,
		lastmood_timestamp = updatedUser.lastmood_timestamp,
		lastresponse_timestamp = updatedUser.lastresponse_timestamp,
		)

async def update_one_user(user_id: str, data: any) -> User:
	async with Prisma() as db:
		return await update_one_user_core(db, user_id, data)
	

# async def main() -> None:
# 	updatedUserDb = await update_one_user(
# 		user_id='U7c0b638081d6027c5bd164a8ae23d4d1', 
# 		data={
# 			'user_role': 'general'
# 		})
# 	if updatedUserDb != None:
# 		glog(f' updated User success => {updatedUserDb}')
# 	else:
# 		glog(f'Fail ureate user {user_id}')

# if __name__ == '__main__':
#     asyncio.run(main())