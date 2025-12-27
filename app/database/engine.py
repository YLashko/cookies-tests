from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio


PGDB_USER = os.environ.get("PGDB_USER")
PGDB_PASSWORD = os.environ.get("PGDB_PASSWORD")
PGDB_HOST = os.environ.get("PGDB_HOST")
PGDB_PORT = os.environ.get("PGDB_PORT")
PGDB_DATABASE = os.environ.get("PGDB_DATABASE")


def get_pg_engine(
    user: str,
    password: str,
    host: str,
    port: str,
    database: str,
    async_: bool = True
):
    engine = "asyncpg" if async_ else "psycopg2"
    connection_str = "postgresql+{engine}://{user}:{password}@{host}:{port}/{database}" \
        .format(
            engine=engine,
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
    if async_:
        return create_async_engine(connection_str)
    
    return create_engine(connection_str)


db_kwargs = {
    "user": PGDB_USER,
    "password": PGDB_PASSWORD,
    "host": PGDB_HOST,
    "port": PGDB_PORT,
    "database": PGDB_DATABASE
}
db = get_pg_engine(
    **db_kwargs,
    async_=True
)
db_sync = get_pg_engine(
    **db_kwargs,
    async_=False
)


async def main():
    async with db.connect() as conn:
        res = await conn.execute(
            text("SELECT 1 AS a, 2 AS b")
        )
        print(res.all()[0])


if __name__ == "__main__":
    asyncio.run(main())
