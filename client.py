import asyncio
from aiohttp import ClientSession

async def get_posts():
    async with ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/posts") as resp:
            return await resp.json()


async def get_post(post_id):
    async with ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8080/post/{post_id}") as resp:
            return await resp.text()


async def post_posts():
    async with ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/post", json={

            "header": "me",
            "text": "data",
            "owner_id": 1
        }) as resp:
            if resp.status != 201:
                return await resp.text()
            return await resp.json()


async def patch_posts(owner_id, text, header, post_id):
    async with ClientSession() as session:
        async with session.patch(f"http://127.0.0.1:8080/post/{post_id}", json={
            "header": header,
            "text": text,
            "owner_id": owner_id
        }) as resp:
            if resp.status != 200:
                return await resp.text()
            return await resp.json()


async def delete_post(post_id):
    async with ClientSession() as session:
        async with session.delete(f"http://127.0.0.1:8080/post/{post_id}") as resp:
            return {"status": resp.status}


async def main():
    response1 = await get_posts()
    print(response1)
    # response2 = await get_post(34)
    # print(response2)
    # response3 = await post_posts()
    # print(response3)
    # response4 = await patch_posts(1, "data", "mine header", 36)
    # print(response4)
    # response5 = await delete_post(33)
    # print(response5)


asyncio.run(main())