from sqlalchemy import Column, BIGINT, String, TIMESTAMP, Text
from app.db.database import Base
from app.core.snowflake import generate_snowflake_id

class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, index=True, default=generate_snowflake_id, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    phone = Column(String(20), unique=True, nullable=True, index=True, comment="用户手机号")
    hashed_password = Column(String(200), nullable=False, comment="加密后的密码")
    create_at = Column(TIMESTAMP, nullable=False, comment="用户创建时间")  

class Ward(Base):
    __tablename__ = "wards"

    id = Column(BIGINT, primary_key=True, index=True, default=generate_snowflake_id, comment="帖子ID")
    user_id = Column(BIGINT, unique=True, nullable=False, index=True, comment="发帖用户ID")
    content = Column(Text, nullable=False, comment="帖子内容")
    like_cnt = Column(BIGINT, nullable=False, default=0, comment="帖子点赞数")
    follow_cnt = Column(BIGINT, nullable=False, default=0, comment="帖子关注数")
    comment_cnt = Column(BIGINT, nullable=False, default=0, comment="帖子评论数")       # TODO 评论相关内容
    create_at = Column(TIMESTAMP, nullable=False, comment="帖子创建时间")
    update_at = Column(TIMESTAMP, nullable=False, comment="帖子最后修改时间")

