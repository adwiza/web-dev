from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base, relationship, session, sessionmaker, scoped_session

engine = create_engine('sqlite:///blog.db')
metadata = MetaData()

Base = declarative_base()

tags_posts_table = Table('tag_posts', metadata,
                         Column('post_id', Integer, ForeignKey('posts.id')),
                         Column('tag_id', Integer, ForeignKey('tags.id')),

                         )


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(Integer, nullable=False)
    text = Column(String(16), nullable=False)
    is_published = Column(Boolean, default=False)
    user = relationship('User', back_populates='posts', lazy='joined')
    tags = relationship('Tag', secondary=tags_posts_table, back_populates='posts')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)


posts = relationship('Post', secondary=tags_posts_table, back_populates='tags')

# Добавление Many2Many

post = session.query(Post).first()
tag = session.query(Tag).first()

post.tags.append(tag)
session.add(post)
session.commit()

post = session.query(Post).filter(Post.id == 1).first()
print(post.tags[0].name)

# Сессии
session_factory = sessionmaker(bind=some_engine)
Session = scoped_session(session_factory)
session = Session()
session2 = Session()
print(session is session2)

#  Получение данных
q = session.query(Post.id).filter(Post.id == 1)
print(type(q))  # <class 'sqlalchemy.orm.query.Query'>
print(list(q))  # [(1, )]
print(q.all())  # [(1, )] # аналог list
print(q.one())  # (1, ) берет все результаты и выбрасывает ошибку, если их не 1
print(q.first())  # (1, ) делает щапрос с Limit 1 и возвращает объект или None
print(q.scalar())  # 1 аналог one()[0]

# Создание
posts = [
    {'id': 1, 'title': 'foo post'},
    {'id': 2, 'title': 'bar post'},
]
for post_info in posts:
    session.add(Post(**post_info))
    session.commit()

for post_info in posts:
    session.add(Post(**post_info))
session.commit()


conn.execute(Post.__table__.insert(), posts)  # запрос

# Join
p = session.query(Post).join(User, Post.user_id == User.id).first()
# p = session.query(Post).join(User).first()
print(p.user.username)  # john

p = session.query(Tag).join(User, Tag.id == User.id).first()
print(p)  # <__main__.Tag object at 0x103471630>

p = session.query(Tag, User).join(User, Tag.id == User.id).first()
print(p)  # <__main__.Tag object at 0x1036aea58>, <__main__.User object at 0x1036aec50>


# У нас есть 2 тега и 2 пользователя
print(session.query(Tag, User).count())
print(p)  # ???

# filter fk (foreign key)
# Посты пользователя с юзернеймом john
session.query(Post).join(User).filter(User.username == 'john').all()
# если убрать join(User) то запрос будет аналогичен этому и БД приляжет
session.query(Post, User).filter(User.username == 'john').all()  # получится декартово произведение

# filter m2m
# Посты с тегом  python
tag_id = session.query(Tag.id).filter(Tag.name == 'python').scalar()
posts = session.query(Post).join(tags_posts_table).filter(
    tags_posts_table.c.tag_id == tag_id,
)
