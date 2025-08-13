from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    # s3_prefix = Column(String, nullable=False)

    files = relationship("S3File", back_populates="play")

    __table_args__ = (
        UniqueConstraint('name', name='uq_name'),
    )

class S3File(Base):
    __tablename__ = "s3_files"

    id = Column(Integer, primary_key=True)
    play_id = Column(Integer, ForeignKey("plays.id"), nullable=False)
    type = Column(String, nullable=False)
    s3_prefix = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)

    play = relationship("Play", back_populates="files")

    __table_args__ = (
        UniqueConstraint('s3_key', name='uq_s3_key'),
    )


class PlayInfo(Base):
    __tablename__ = "play_infos"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    main_cover = Column(String)
    alt_main_cover = Column(String)
    covers = Column(String)
    author = Column(String)
    year = Column(Integer)
    description = Column(String)
    # s3_prefix = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uq_info_name'),
    )