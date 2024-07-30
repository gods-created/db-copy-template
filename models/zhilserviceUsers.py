from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class ZhilserviceUsers(Base):
    __tablename__ = 'zhilservice_users'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    e: Mapped[str] = mapped_column(String(256), unique=True)
    f: Mapped[str] = mapped_column(String())
    p: Mapped[str] = mapped_column(String())
    r: Mapped[int] = mapped_column(nullable=False)
    avatar: Mapped[str] = mapped_column(String(), default='https://zhylservice-prod-dfcc31fdb708.herokuapp.com/user/avatar/1722333603441.jpg')
    phone: Mapped[str] = mapped_column(String(256))

    def to_json(self):
        return {
            'id': self.id,
            'e': self.e,
            'f': self.f,
            'p': self.p,
            'r': self.r,
            'avatar': self.avatar,
            'phone': self.phone
        }
    

