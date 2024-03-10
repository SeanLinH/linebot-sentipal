import asyncio
from prisma import Prisma
from src.prisma.user import User
from src.prisma.group import Group
from src.prisma.util import glog, clr_Red, clr_Off

"""

"""


async def create_one_group_core(db:Prisma, group: Group) -> Group:
	if len(group.groupUsers) == 0:
		glog(f"{clr_Red}create_one_group_core FAILED!\nAt least insert one user in group.groupUsers{clr_Off}")
		return None
	groupUsersConnect=[]
	for user in group.groupUsers:
		groupUsersConnect.append({
			'user_id': user.user_id,
		})
	if group.belongToUserApiId != None:
		data={
			'group_id': group.group_id,
			'groupUsers': {
				'connect': groupUsersConnect,
			},
			'belongToUserApi': {
				'connect': {
					'user_id': group.belongToUserApiId,
				}
			}
		}
	else:
		data={
			'group_id': group.group_id,
			'groupUsers': {
				'connect': groupUsersConnect,
			},
		}
	newGroup = await db.group.create(
		data=data,
		include={
			'groupUsers': True,
		}
	)
	groupUsers = []
	for e in newGroup.groupUsers:
		groupUsers.append(User(
			user_id=e.user_id, 
			user_role=e.user_role,
			summary=e.summary,
			lastmood_timestamp=e.lastmood_timestamp,
			lastresponse_timestamp=e.lastresponse_timestamp
		))

	# if user has key
	userDb = await db.user.find_unique(
			where={
				'user_id': group.groupUsers[0].user_id,
			},
			include={
				'userApi': True,
			}
		)
	if userDb.userApi != None:
		groupDb = await db.group.update(
			where={
				'group_id': group.group_id,
			},
			data={
				'belongToUserApi': {
					'connect': {
						'user_id': userDb.userApi.user_id,
					}
				}
			}
		)

	return Group(
		group_id    	= newGroup.group_id,
		groupUsers      = groupUsers,
		belongToUserApiId = newGroup.belongToUserApiId,
		)

async def create_one_group(group: Group) -> Group:
	async with Prisma() as db:
		return await create_one_group_core(db, group)
	

# async def main() -> None:
# 	newGroup = Group(group_id='Group2', groupUsers=[User(user_id='2234')])
# 	newGroupDb = await create_one_group(newGroup)
# 	if newGroupDb != None:
# 		glog(f' create Group success => {newGroupDb}')
# 	else:
# 		glog(f'Fail create group {newGroupDb}')

# if __name__ == '__main__':
#     asyncio.run(main())