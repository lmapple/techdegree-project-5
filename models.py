import datetime

from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


DATABASE = SqliteDatabase('journal.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    email = CharField(unique=True)
    is_admin = BooleanField(default=False)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, username, email, password, is_admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=is_admin)
        except IntegrityError:
            raise ValueError("User already exists.")

    def validate_password(User, password):
        if check_password_hash(User.password, password):
            return True
        else:
            return False

"""    def get_entries(self):
        return Entry.select().where(Entry.username == self)

    def get_tagged_entries(self):
        pass
        """
"""
        return (
            User.select().join(
                Tag, on=Tag.to_user
            ).where(
                Tag.from_user == self)
        )                
        """

class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    username = ForeignKeyField(
        User,
        related_name='entries'
    )
    title = TextField(unique=True)
    date = DateField()
    time_spent = TextField()
    what_i_learned = TextField()
    resources_to_remember = TextField()
    last_updated = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


    @classmethod
    def create_entry(cls, username, title, date, time_spent, what_i_learned,
                  resources_to_remember):
        cls.create(
            username=username,
            title=title,
            date=date,
            time_spent=time_spent,
            what_i_learned=what_i_learned,
            resources_to_remember=resources_to_remember
        )

"""    def edit_entry(self, title, date, time_spent, what_i_learned,
                  resources_to_remember):
        self.update(
            title=title,
            date=date,
            time_spent=time_spent,
            what_i_learned=what_i_learned,
            resources_to_remember=resources_to_remember
        )

    def delete_entry(self):
        pass"""


"""class Tag(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True)
        )"""



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    #DATABASE.create_tables([User,Entry,Tag], safe=True)
    DATABASE.close()

    try:
        User.create_user(
            username='user1',
            email='user1@treehouse.com',
            password='password',
        )
    except ValueError:
        pass
    try:
        Entry.create_entry(username=1,
                     title='Hello',
                     date='2020-12-27',
                     time_spent=100,
                     what_i_learned='Hello World',
                     resources_to_remember='python.org'
                     )
    except IntegrityError:
        pass