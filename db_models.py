from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    s3_folder_key = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uq_name'),
    )
