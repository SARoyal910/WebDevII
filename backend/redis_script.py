import os
import asyncio
import asyncpg
from backend.redis import RedisAdapter

async def main():
	conn = RedisAdapter()
	await conn.set("W3D1", "Some key")
	await conn.set("user:1230948092384:session_id", "2o3u2oi3hfoiqwhed982hiouhoho8")
	await conn.set("user:1230948092384:csrf_token", "2o3u2oi3hf423v3v4sv982hiouhoho8")
	await conn.set("user:1230948092384:otp", "2o3u2oi3hfoiqwhe5-034-0gi09i")
	
	list_of_keys = await conn.keys("user:1230948092384:*")
	
	for key in list_of_keys:
		print(f"\033[1;33m{key}\033[0m")
		
	got_key = await conn.get("W3D1")
	print(f"\033[1;35m{got_key}\033[0m")

# Run the async entrypoint
if __name__ == "__main__":
	asyncio.run(main())