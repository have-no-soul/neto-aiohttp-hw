import sys
import asyncio
import aiopg

from aiohttp import web
from models import db
from views import PostsView, PostView

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = web.Application()

DB_DSN = "postgres://admin:1234@127.0.0.1:5432/aiohttp"


async def orm_context(app):
    await db.set_bind(DB_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


async def register_pg_pool(app):
    async with aiopg.pool.create_pool(DB_DSN) as pool:
        app['pg_pool'] = pool
        yield
        pool.close()
    print("end")


if __name__ == "__main__":
    app.add_routes([
        web.get("/posts", PostsView)
    ])
    app.add_routes([
        web.get("/post/{post_id:\d+}", PostView),
        web.post("/post", PostView),
        web.patch("/post/{post_id:\d+}", PostView),
        web.delete("/post/{post_id:\d+}", PostView)
    ])
    app.cleanup_ctx.append(register_pg_pool)
    app.cleanup_ctx.append(orm_context)
    web.run_app(app)
