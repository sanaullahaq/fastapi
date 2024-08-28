from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from . database import Base

class Post(Base):
	__tablename__ = 'posts'
	id = Column(Integer, primary_key=True, nullable=False)
	title = Column(String, nullable=False)
	content = Column(String, nullable=False)
	published = Column(Boolean, server_default='True', nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	#									__tablename__.field
	owner = relationship("User")
	#setting relationship is not mandatory for ForeignKey, it will not take any effect to the DB as well.
	#setting the relationship will also fetch the data based on the schema by itself 



class User(Base):
	__tablename__="users"
	id = Column(Integer, primary_key=True, nullable=False)
	email = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))