from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User') # returns info about user but not in the table, i think
    comments = relationship('Comment', cascade='all,delete') # the last bit makes sure comments are deleted when its parent post is deleted

    votes = relationship('Vote', cascade='all,delete')

    vote_count = column_property(
        select([func.count(Vote.id)]).where(Vote.post_id == id) # counts the votes on a specific post
    )