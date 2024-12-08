from psycopg_pool import AsyncConnectionPool
from pg_asynq import AsynqManager

POSTGRES_CONN_STR = "postgresql://postgres:postgres@localhost:5432/postgres"

async def main():
    default_pool = lambda *args, **kwargs: AsyncConnectionPool(POSTGRES_CONN_STR, max_size=4, *args, **kwargs)
    for i in range(10):
        async with AsynqManager(default_pool, "test_queue") as manager:
            await manager.queue_json({"test": "test"})
            print("Queued message")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    