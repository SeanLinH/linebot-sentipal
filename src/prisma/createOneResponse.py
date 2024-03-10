import asyncio
from prisma import Prisma
from src.prisma.response import Response
from src.prisma.mood import Mood
from src.prisma.user import User
from src.prisma.util import glog


"""
AI response insert to [Response]
"""

async def create_one_response_core(db: Prisma, response: Response, aimTo: Mood) -> Response:
	aim_to_mood_timestamp = None
	if aimTo != None:
		aim_to_mood_timestamp = aimTo.timestamp
	responseDb = await db.response.create(
		data = {
			'user': {
				'connect': {
					'user_id': response.user_id,
				}
			},
			'group_id': response.group_id,
			'ai_text': response.ai_text,
			'aimTo': {
				'connect': {
					'timestamp': aim_to_mood_timestamp,
				}
			},
			'lastUser': {
				'connect': {
					'user_id': response.user_id
				}
			}
		}
	)
	ans = Response(
		user_id    = responseDb.user_id,
		group_id   = responseDb.group_id,
		ai_text    = responseDb.ai_text,
		aim_to_mood_timestamp = responseDb.aim_to_mood_timestamp
		)
	ans.timestamp = responseDb.timestamp
	return ans

async def create_one_response(response: Response, aimTo: Mood) -> Response:
	async with Prisma() as db:
		return await create_one_response_core(db, response, aimTo)

# async def main() -> None:
# 	newResponse = Response(user_id='2234',group_id=None,ai_text='第一個回應來嘍')
# 	ans = await create_one_response(newResponse)
# 	if ans != None:
# 		glog(f' => {ans}')

# if __name__ == '__main__':
#     asyncio.run(main())