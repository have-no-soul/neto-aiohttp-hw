from datetime import datetime
from asyncpg import UniqueViolationError
from gino import Gino
from aiohttp import web

db = Gino()


class BaseModelMixin:

    @classmethod
    async def by_id(cls, obj_id):
        obj = await cls.get(obj_id)
        if obj:
            return obj
        else:
            raise web.HTTPNotFound()

    @classmethod
    async def create_model(cls, **kwargs):
        try:
            obj = await cls.create(**kwargs)
            return obj

        except UniqueViolationError:
            raise web.HTTPBadRequest()

    @classmethod
    async def update_model(cls, obj_id, **kwargs):
        get = await cls.by_id(obj_id)
        await get.update(**kwargs).apply()
        response = await cls.by_id(obj_id)
        return response


class Users(db.Model, BaseModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)

    _idx1 = db.Index("users_user_username", "username", unique=True)

    def to_dict(self):
        dict_user = super().to_dict()
        dict_user.pop("password")
        return dict_user


class Posts(db.Model, BaseModelMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    header = db.Column(db.String(50))
    text = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime, default=datetime.today)
    owner_id = db.Column(db.Integer(), db.ForeignKey(Users.id))

    def to_dict(self):
        posts = {
            "id": self.id,
            "header": self.header,
            "text": self.text,
            "created_date": str(self.created_date),
            "owner_id": self.owner_id
        }
        return posts


async def return_all_posts():
    get = await Posts.query.gino.all()
    some_list = []
    for post in get:
        some_list.append({"id": post.id, "header": post.header, "text": post.text,
                          "created_date": str(post.created_date), "owner_id": str(post.owner_id)})
    return some_list