import asyncio
from prisma import Prisma
from src.prisma.user import User
from src.prisma.findOneUser import find_one_user_core
from src.prisma.userApi import UserApi
from src.prisma.util import glog, clr_Red, clr_Off

"""

"""


async def register_user_api_core(db:Prisma, user_id: str, user_api: str) -> UserApi:
	hasUser = await db.user.find_unique(
			where={
				'user_id': user_id
			},
			include={
				'groups': True,
			}
		)
	if hasUser == None:
		glog(f"{clr_Red}register_user_api with invalid user_id '{user_id}' !{clr_Off}")
		return None
	userGroups = []
	for group in hasUser.groups:
		userGroups.append({
			'group_id': group.group_id,
		})
	userApi = await db.userapi.find_unique(
		where={
			'user_id': user_id,
		},
		include={
			'user': True,
			'groups': True,
		}
	)
	if userApi == None:
		userApiDb = await db.userapi.create(
			data={
				'user': {
					'connect': {
						'user_id': user_id,
					}
				},
				'user_api': user_api, # TODO: encrypt APK_KEY here
				'groups': {
					'connect': userGroups,
				}
			},
			include={
				'user': True,
			}
		)
		timestamp = userApiDb.timestamp
		if len(hasUser.groups) > 0:
			for group in hasUser.groups:
				await db.group.update(
					where={
						'group_id': group.group_id,
					},
					data={
						'belongToUserApi': {
							'connect': {
								'user_id': userApiDb.user_id,
							}
						}
					}
				)
			userApi = await db.userapi.find_unique(
				where={
					'user_id': user_id,
				},
				include={
					'user': True,
					'groups': True,
				}
			)
			timestamp = userApi.timestamp
		else:
			userApi = userApiDb

	else:
		timestamp = userApi.timestamp
		if userApi.user_api != user_api:
			userApiDb = await db.userapi.update(
				where={
					'user_id': user_id
				},
				data={
					'user_api': user_api # TODO: encrypt APK_KEY here
				},
				include={
					'user': True,
				}
			)

	ans = UserApi(
		user_id   = userApi.user_id,
		user_api  = userApi.user_api,
		)
	ans.timestamp = timestamp
	return ans

async def register_user_api(user_id: str, user_api: str) -> UserApi:
	async with Prisma() as db:
		return await register_user_api_core(db, user_id, user_api)
	

async def main() -> None:
	userApi = await register_user_api(user_id='2234',user_api='API_KEY')
	if userApi != None:
		glog(f' register UserApi success => {userApi}')
	else:
		glog(f'Fail register userApi')

if __name__ == '__main__':
    asyncio.run(main())