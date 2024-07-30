from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    filename: Mapped[str] = mapped_column(String(256))

    def to_json(self):
        return {
            'id': self.id,
            'filename': self.filename,
        }
    

