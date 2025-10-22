import os
import asyncio
import asyncpg

# db_params = {
#     "host": o,
#     "user": os.getenv("USER"),
#     "password": os.getenv("PASSWORD"),
#     "db": os.getenv("DB"),
#     "port": os.getenv("PORT"),
# }

async def main():
	# Connect to Postgres (adjust user, password, db as needed)
	conn = await asyncpg.connect(
		user=os.getenv("USER"),
		password=os.getenv("PASSWORD"),
		database=os.getenv("DB"),
		host=os.getenv("HOST"),
		port=os.getenv("DB_PORT")
	)
	
	print(os.getenv("USER"))

	# Create a table (if not exists)
	await conn.execute("""
		CREATE TABLE IF NOT EXISTS fake3 (
			id SERIAL PRIMARY KEY,
			name VARCHAR(50) NOT NULL
		)
	""")

	# Insert a row
	await conn.execute("INSERT INTO fake3 (name) VALUES ($1)", "Alfred")

	# Fetch all rows
	rows = await conn.fetch("SELECT * FROM fake3")
	for row in rows:
		print(dict(row))   # row is Record; convert to dict for readability

	rows = await conn.fetch("SELECT * FROM fake2")
	for row in rows:
		print(dict(row))  

	# Close connection
	await conn.close()

# Run the async entrypoint
if __name__ == "__main__":
	asyncio.run(main())