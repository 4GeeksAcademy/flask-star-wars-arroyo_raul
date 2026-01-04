from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    fecha_subscripcion: Mapped[datetime] = mapped_column(nullable=False)
    favourites: Mapped[List["Favorito"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "frcha_subscripcion": self.fecha_subscripcion
            # do not serialize the password, its a security breach
        }

class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    favorito: Mapped["Favorito"] = relationship(back_populates="planeta")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }
    
class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    favorito: Mapped["Favorito"] = relationship(back_populates="personaje")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }
    
class Favorito(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favourites")
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=True)
    planeta: Mapped["Planeta"] = relationship(back_populates="favorito")
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=True)
    personaje: Mapped["Personaje"] = relationship(back_populates="favorito")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id
        }