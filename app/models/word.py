from sqlalchemy import Column, BIGINT, TIMESTAMP, Text
from app.db.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(BIGINT, primary_key=True, index=True,comment="帖子ID")
    user_id = Column(BIGINT, unique=True, nullable=False, index=True, comment="发帖用户ID")
    content = Column(Text, nullable=False, comment="帖子内容")
    like_cnt = Column(BIGINT, nullable=False, default=0, comment="帖子点赞数")
    follow_cnt = Column(BIGINT, nullable=False, default=0, comment="帖子关注数")
    comment_cnt = Column(BIGINT, nullable=False, default=0, comment="帖子评论数")
    create_at = Column(TIMESTAMP, nullable=False, comment="帖子创建时间")
    update_at = Column(TIMESTAMP, nullable=False, comment="帖子最后修改时间")

