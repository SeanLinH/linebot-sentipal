import asyncio
from prisma import Prisma
from src.prisma.user import User
from src.prisma.group import Group
from src.prisma.util import glog, clr_Yellow, clr_Off

"""

"""


async def update_one_group_core(db:Prisma, group_id: str, data: any) -> User:
	updatedGroup = await db.group.update(
		where={
			'group_id': group_id,
		},
		data=data,
		include={
			'groupUsers': True,
		}
	)
	groupUsers = []
	for e in updatedGroup.groupUsers:
		groupUsers.append(User(
			user_id=e.user_id, 
			user_role=e.user_role,
			summary=e.summary,
			lastmood_timestamp=e.lastmood_timestamp,
			lastresponse_timestamp=e.lastresponse_timestamp
		))
	return Group(
		group_id    	= updatedGroup.group_id,
		groupUsers      = groupUsers,
		belongToUserApiId = updatedGroup.belongToUserApiId,
		)

async def update_one_group(group_id: str, data: any) -> User:
	async with Prisma() as db:
		return await update_one_group_core(db, group_id, data)
	

# async def main() -> None:
# 	group_id='Group1'
# 	updatedUserDb = await update_one_group(
# 		group_id=group_id, 
# 		data={
# 			'groupUsers': {
# 				# 'connect': [
# 				# 	{
# 				# 		'user_id': 'U7c0b638081d6027c5bd164a8ae23d4d1'
# 				# 	},
# 				# ],
# 				'disconnect': [
# 					{
# 						'user_id': 'U7c0b638081d6027c5bd164a8ae23d4d1'
# 					},
# 				]
# 			}
# 		})
# 	if updatedUserDb != None:
# 		glog(f' updated Group success => {updatedUserDb}\n{clr_Yellow}groupUsers count: {len(updatedUserDb.groupUsers)}{clr_Off}')
# 	else:
# 		glog(f'Fail ureate group {group_id}')

# if __name__ == '__main__':
#     asyncio.run(main())