import sqlalchemy as db
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

engine = db.create_engine('sqlite:///blog.db')
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

tags_posts_table = db.Table('tag_posts',
    Base.metadata,
    db.Column('tag_of_post', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('post_tagged', db.Integer, db.ForeignKey('posts.id'), primary_key=True))




class User (Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = relationship('Post', backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post (Base):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = relationship('Tag', secondary=tags_posts_table, back_populates='posts', lazy='dynamic')

    def ___repr__(self):
        return f"Post('{self.id}', '{self.title}')"


class Tag(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    posts = relationship('Post', secondary=tags_posts_table, back_populates='tags')

    def __repr__(self):
        return f"Tag('{self.id}', '{self.name}')"

def fill_data():#to fill the db with data
    Base.metadata.create_all(engine)
    session = Session()
    user = User(username='liza', email='liza@example.com')
    user2=User(username='anna', email='anna@example.com')
    session.add(user)
    session.add(user2)
    session.flush()
    tag1 = Tag(name='my_story')
    tag2 = Tag(name='programming')
    post1 = Post(user_id=user.id, title='Why Python?', content='why python is the first programming language you should learn')
    post2 = Post(user_id=user2.id, title='Can you find a job with python nowadays?', content='the answer to this question is ambiguous')
    post3 = Post(user_id=user.id, title='Why have you decided to learn coding',content='My road to coding was long. Literally')
    session.add(tag1)
    session.add(tag2)
    session.add(post1)
    session.add(post2)
    session.add(post3)
    session.flush()
    taggs = session.query(Tag)[:2]
    post1.tags.extend(taggs)
    post3.tags.extend(taggs)
    post2.tags.append(tag1)
    session.commit()


if __name__ ==  '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    fill_data()
    user1 = session.query(User).first()
    print(user1.username)
    tag1 = session.query(Tag).first()
    print(tag1.name)
    tag2 = session.query(Tag).filter(Tag.id==2).first()
    print(tag2.name)
    #Выбрать все посты конкретного пользователя с 2-мя любыми тегами
    qqq = session.query(Post).join(User).filter(User.id == user1.id).filter(Post.tags.contains(tag1)).filter(Post.tags.contains(tag2)).all()
    for q in qqq:
        print(q.title)

