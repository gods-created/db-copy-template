from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class PersonalAccounts(Base):
    __tablename__ = 'personal_accounts'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(String(50))
    service: Mapped[str] = mapped_column(String(50))
    account: Mapped[int] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(50))

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'city': self.city,
            'service': self.service,
            'account': self.account,
            'address': self.address,
        }
    

