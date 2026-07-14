from sqlalchemy import Column, Integer, String
from app.database.base import Base

class ProductType(Base):
    __tablename__ = "product_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

class ProductMotif(Base):
    __tablename__ = "product_motifs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

class ProductSubMotif(Base):
    __tablename__ = "product_sub_motifs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

class ProductColor(Base):
    __tablename__ = "product_colors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
