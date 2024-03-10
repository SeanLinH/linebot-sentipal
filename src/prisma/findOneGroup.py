import asyncio
from prisma import Prisma
from src.prisma.group import Group
from src.prisma.util import glog

"""
find group_id in [Groups] or not
"""

async def find_one_group_core(db: Prisma, groupId: str) -> Group:
	bingo = await db.group.find_unique(
			where={
				'group_id': groupId
			}
		)
	# glog(f'bingo => {bingo}')
	if bingo == None:
		return None
	return Group(
		group_id    	= bingo.group_id,
		belongToUserId  = bingo.belongToUserId,
		belongToUserApiId = bingo.belongToUserApiId,
		)

async def find_one_group(groupId: str) -> Group:
	async with Prisma() as db:
		return await find_one_group_core(db, groupId)

# async def main() -> None:
# 	ans = await find_one_group('')
# 	if ans != None:
# 		glog(f' => {ans}')

# if __name__ == '__main__':
#     asyncio.run(main())