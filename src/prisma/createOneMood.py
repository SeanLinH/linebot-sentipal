import asyncio
from prisma import Prisma
from src.prisma.mood import Mood
from src.prisma.user import User
from src.prisma.group import Group
from src.prisma.findOneUser import find_one_user_core
from src.prisma.findOneGroup import find_one_group_core
from src.prisma.createOneUser import create_one_user_core
from src.prisma.createOneGroup import create_one_group_core
from src.prisma.updateOneGroup import update_one_group_core
from src.prisma.util import glog
from api.huggingface import Models


"""
insert user mood to [mood] db
"""

async def create_one_mood_core(db: Prisma, mood: Mood) -> Mood:
	userDb = await find_one_user_core(db, mood.user_id)
	if userDb == None:
		newUser = User(user_id=mood.user_id)
		userDb = await create_one_user_core(db, newUser)

	if mood.group_id != None:
		groupDb = await find_one_group_core(db, mood.group_id, True)
		if groupDb == None:
			newGroup = Group(group_id=mood.group_id, groupUsers=[User(user_id=mood.user_id)])
			groupDb = await create_one_group_core(db, newGroup)
		else:
			userWasInTheGroup = False
			for u in groupDb.groupUsers:
				if u.user_id == mood.user_id:
					userWasInTheGroup = True
					break
			if not userWasInTheGroup:
				groupDb = await update_one_group_core(db, mood.group_id, data={
					'groupUsers': {
						'connect': [
							{
								'user_id': mood.user_id
							}
						]
					}
				})
	moodDb = await db.mood.create(
		data = {
			'user': {
				'connect': {
					'user_id': userDb.user_id,
				}
			},
			'group_id': mood.group_id,
			'user_text': mood.user_text,
			# 'user_mood': None, 
			'mood_score': 0,
			'stable_score': 0,
			'engage': 0,
			'lastUser': {
				'connect': {
					'user_id': userDb.user_id
				}
			}
		}
	)
	ans = Mood(
		user_id    = moodDb.user_id,
		group_id   = moodDb.group_id,
		user_text  = moodDb.user_text,
		user_mood  = moodDb.user_mood,
		mood_score = moodDb.mood_score,
		stable_score = moodDb.stable_score,
		engage     = moodDb.engage,
		)
	ans.timestamp = moodDb.timestamp
	return ans

async def create_one_mood(mood: Mood) -> Mood:
	async with Prisma() as db:
		return await create_one_mood_core(db, mood)

# async def main() -> None:
# 	newMood = Mood(user_id='2234',group_id=None,user_text='第一個訊息來嘍')
# 	ans = await create_one_mood(newMood)
# 	if ans != None:
# 		glog(f' => {ans}')

# if __name__ == '__main__':
#     asyncio.run(main())