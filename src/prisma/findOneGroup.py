import asyncio
from prisma import Prisma
from src.prisma.user import User
from src.prisma.group import Group
from src.prisma.util import glog

"""
find group_id in [Groups] or not
"""

async def find_one_group_core(db: Prisma, groupId: str, includeGroupUsers: bool) -> Group:
	bingo = await db.group.find_unique(
			where={
				'group_id': groupId
			},
			include={
				'groupUsers': includeGroupUsers,
			}
		)
	# glog(f'bingo => {bingo}')
	if bingo == None:
		return None
	
	if includeGroupUsers:
		groupUsers = []
		for e in bingo.groupUsers:
			groupUsers.append(User(
				user_id=e.user_id, 
				user_role=e.user_role,
				summary=e.summary,
				lastmood_timestamp=e.lastmood_timestamp,
				lastresponse_timestamp=e.lastresponse_timestamp
			))

	return Group(
		group_id    	= bingo.group_id,
		groupUsers 		= groupUsers,
		belongToUserApiId = bingo.belongToUserApiId,
		)

async def find_one_group(groupId: str, includeGroupUsers: bool=False) -> Group:
	async with Prisma() as db:
		return await find_one_group_core(db, groupId, includeGroupUsers)

# async def main() -> None:
# 	ans = await find_one_group('')
# 	if ans != None:
# 		glog(f' => {ans}')

# if __name__ == '__main__':
#     asyncio.run(main())