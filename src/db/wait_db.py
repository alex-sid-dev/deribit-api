import asyncio
import os
import asyncpg

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = int(os.getenv("POSTGRES_PORT"))
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")


async def wait_db():
    try:
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
        )
        await conn.close()
        return True
    except Exception:
        return False


async def main():
    success = await wait_db()
    if not success:
        exit(1)
    exit(0)


if __name__ == "__main__":
    asyncio.run(main())
