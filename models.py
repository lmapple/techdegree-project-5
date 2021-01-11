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
    def create_entry(cls, username, title, date, time_spent,
                     what_i_learned, resources_to_remember
                     ):
        cls.create(
            username=username,
            title=title,
            date=date,
            time_spent=time_spent,
            what_i_learned=what_i_learned,
            resources_to_remember=resources_to_remember,
        )

    def get_tag_names(self):
        return (
            Tag.select().join(
                TagEntry_Relationship,
                on=TagEntry_Relationship.entry_tags
            ).where(
                TagEntry_Relationship.tagged_entries == self
            )

        )


class Tag(Model):
    tag_name = TextField(unique=True)

    @classmethod
    def create_tag(cls, tag_name):
        cls.create(
            tag_name=tag_name
        )

    def get_tagged_entries(self):
        return (
            Entry.select().join(
                TagEntry_Relationship,
                on=TagEntry_Relationship.tagged_entries
            ).where(
                TagEntry_Relationship.entry_tags == self
            )
        )

    class Meta:
        database = DATABASE


class TagEntry_Relationship(Model):
    #Tags attached to a certain entry
    entry_tags = ForeignKeyField(Tag, to_field="id",
                                 related_name='entries'
                                 )
    #Entries with a certain tag
    tagged_entries = ForeignKeyField(Entry, to_field="id",
                                     related_name='tags'
                                     )

    class Meta:
        database = DATABASE
        indexes = (
            (('entry_tags', 'tagged_entries'), True),
        )

    @classmethod
    def create_relationship(cls, tag, entry):
        tag = (Tag.get(Tag.tag_name == tag)
               )
        entry = (Entry.get(Entry.title == entry)
                 )

        cls.create(
            entry_tags=tag.id,
            tagged_entries=entry.id
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables(
        [User,Entry,Tag,TagEntry_Relationship],
        safe=True
    )
    DATABASE.close()

#Fulfills requirement to have an existing entry when the database is
#first initialized. Also adds an initial user.
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
                     date='2021-01-01',
                     time_spent=100,
                     what_i_learned='Hello World',
                     resources_to_remember='python.org',
                     )
        for tag in ['python','world','hello']:
            try:
                Tag.create_tag(tag_name=tag)
                TagEntry_Relationship.create_relationship(tag, 'Hello')
            except IntegrityError:
                TagEntry_Relationship.create_relationship(tag,'Hello')

    except IntegrityError:
        pass