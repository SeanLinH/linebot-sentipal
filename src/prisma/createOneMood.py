import asyncio
from prisma import Prisma
from mood import Mood
from user import User
from findOneUser import find_one_user_core
from createOneUser import create_one_user_core
from util import glog

async def create_one_mood_core(db: Prisma, mood: Mood) -> Mood:
	userDb = await find_one_user_core(db, mood.user_id)
	if userDb == None:
		newUser = User(user_id=mood.user_id)
		userDb = await create_one_user_core(db, newUser)

	moodDb = await db.mood.create(
		data = {
			'user': {
				'connect': {
					'user_id': userDb.user_id,
				}
			},
			'group_id': mood.group_id,
			'user_text': mood.user_text,
			# 'user_mood': 
			# 'mood_score':
			# 'stable_score':
			# 'engage':
			'lastUser': {
				'connect': {
					'user_id': userDb.user_id
				}
			}
		}
	)
	return moodDb

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