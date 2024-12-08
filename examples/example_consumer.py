import logging
from psycopg_pool import AsyncConnectionPool
from pg_asynq import AsynqManager

logging.basicConfig(level=logging.DEBUG)

POSTGRES_CONN_STR = "postgresql://postgres:postgres@localhost:5432/postgres"

async def main():
    default_pool = lambda *args, **kwargs: AsyncConnectionPool(POSTGRES_CONN_STR,
                                                            max_size=4, *args, **kwargs)
    async with AsynqManager(default_pool, "test_queue") as manager:
        async for message in manager.get_next_message():
            print("Processing", message)
            await asyncio.sleep(.2)
            print("Processed", message)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
