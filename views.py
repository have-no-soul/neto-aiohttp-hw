from aiohttp import web
from models import return_all_posts, Posts


class PostsView(web.View):

    async def get(self):
        get_all = await return_all_posts()
        return web.json_response(get_all)


class PostView(web.View):

    async def get(self):
        post = int(self.request.match_info["post_id"])
        get_post = await Posts.by_id(post)
        return web.json_response(get_post.to_dict())

    async def post(self):
        data = await self.request.json()
        if bool("header" and "text" and "owner_id" not in data.keys()):
            raise web.HTTPBadRequest()
        create = await Posts.create_model(**data)
        return web.json_response(create.to_dict())

    async def patch(self):
        data = await self.request.json()
        post = int(self.request.match_info["post_id"])
        updated_data = await Posts.update_model(post, **data)
        return web.json_response(updated_data.to_dict())

    async def delete(self):
        post = int(self.request.match_info["post_id"])
        get_post = await Posts.by_id(post)
        if not get_post:
            return web.HTTPNotFound()
        await get_post.delete()
        return web.HTTPNoContent()