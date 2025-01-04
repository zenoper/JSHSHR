from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from datetime import datetime, timedelta
from typing import Optional

import config as Config


class Database:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(user=Config.DB_USER, password=Config.DB_PASS, host=Config.DB_HOST, port=Config.DB_PORT, database=Config.DB_NAME)
        return cls(pool)

    async def init_db(self):
        async with self.pool.acquire() as conn:
            # Create users table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    #
                )
            ''')


    async def delete_db(self):
        async with self.pool.acquire() as conn:
            # Create users table
            await conn.execute('''
                DROP TABLE IF EXISTS users CASCADE;
            ''')