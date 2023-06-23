from sqlalchemy import ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import mapped_column, relationship

from app.db.main import Base


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    phone = mapped_column(Text, nullable=False, unique=True)


# example
# class Specialty(Base):
#     __tablename__ = "specialty"
#
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(Text, nullable=False, unique=True)
#
#
# class DoctorAccount(Base):
#     __tablename__ = "doctor_account"
#
#     id = mapped_column(Integer, primary_key=True)
#     phone = mapped_column(Text, nullable=False, unique=True)
#     password_hash = mapped_column(Text, nullable=False, unique=True)
#     full_name = mapped_column(Text, nullable=False)
#     specialty_id = mapped_column(Integer, ForeignKey("specialty.id"), nullable=False)
#     specialty = relationship(Specialty)
#
#
# class SpecialItem(Base):
#     __tablename__ = "special_item"
#
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(Text, nullable=False)
#     amount = mapped_column(Integer, nullable=False)
#     price = mapped_column(Numeric(precision=8, scale=2))
#     dosage_form = mapped_column(Text, nullable=False)
#     manufacturer = mapped_column(Text, nullable=False)
#     barcode = mapped_column(Text, nullable=False, unique=True)
#     specialty_id = mapped_column(Integer, ForeignKey("specialty.id"), nullable=False)
#     specialty = relationship(Specialty)
