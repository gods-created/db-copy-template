from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Articles(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    title: Mapped[str] = mapped_column(String(256))
    text: Mapped[str] = mapped_column(String())
    articleType: Mapped[int] = mapped_column(nullable=True)
    images: Mapped[str] = mapped_column(String(256))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'articleType': self.articleType,
            'images': self.images
        }
    

