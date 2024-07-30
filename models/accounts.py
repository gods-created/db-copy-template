from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Accounts(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    city: Mapped[str] = mapped_column(String(256))
    account: Mapped[int] = mapped_column(nullable=False)
    trash: Mapped[float] = mapped_column(nullable=True, default=float(0))
    flat: Mapped[float] = mapped_column(nullable=True, default=float(0))
    warming: Mapped[float] = mapped_column(nullable=True, default=float(0))

    def to_json(self):
        return {
            'id': self.id,
            'city': self.city,
            'account': self.account,
            'trash': self.trash,
            'flat': self.flat,
            'warming': self.warming,
        }
    

