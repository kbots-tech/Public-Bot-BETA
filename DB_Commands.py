import aiomysql
from settings import host,db_user,db_password,database

async def get_data(args, data=()):
        """Connects to the database and returns data"""
        conn = await aiomysql.connect(
            host=host,
            port=3306,
            user=db_user,
            password=db_password,
            db=database,
            )

        cur = await conn.cursor()
        await cur.execute(args, data)
        r = await cur.fetchall()
        
        await cur.close()
        conn.close()
        return r

async def insert_data(args, data=()):
        """Connects to the database and inserts data"""
        conn = await aiomysql.connect(
            host=host,
            port=3306,
            user=db_user,
            password=db_password,
            db=database,
            )

        cur = await conn.cursor()
        async with conn.cursor() as cur:
            await cur.execute(args, data)
            await conn.commit()

        conn.close()