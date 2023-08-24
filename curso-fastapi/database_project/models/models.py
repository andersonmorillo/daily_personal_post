from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from config.database import Base
from sqlalchemy.orm import relationship
"""
            Dueño: {

        id: Optional[int] = None

        name: str = “Anderson”

        mail: str

        mascotas: list[mascota] = []
        
        is_active: str

        }

        Mascotas:{

        id: Optional[int] = None

        name: str 

        race: Optional[str]

        }
"""


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    name = Column(String, index=True)
    mail = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    pets = relationship("Pet", back_populates="owner")


class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    race = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pets")
