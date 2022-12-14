from playhouse.db_url import connect
from peewee import Model
from peewee import IntegerField
from peewee import CharField
from flask_login import UserMixin

db = connect("sqlite:///peewee_db.sqlite")


if not db.connect():
    print("接続NG")
    exit()
print("接続OK")


class User(UserMixin, Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    age = IntegerField()
    gender = CharField()
    address = CharField()
    tel = IntegerField()
    email = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = "user"


db.create_tables([User])


class Offer(Model):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    date = IntegerField()
    time = IntegerField()
    example = CharField()
    place = CharField()
    photo1 = CharField()
    photo2 = CharField()
    photo3 = CharField()
    detail = CharField()

    class Meta:
        database = db
        table_name = "offer"


# 作り直し
# db.drop_tables([Offer])
db.create_tables([Offer])
