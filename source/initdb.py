import os
from sqlmodel import create_engine
from models.invoice import *
from models.user import *

if input("Delete all data? ") == "":
	try:
		os.remove("./data.db")
	except:
		pass
	sql_url = "sqlite:///./data.db"
	args = {"check_same_thread": False}
	engine = create_engine(sql_url, connect_args=args)
	SQLModel.metadata.create_all(engine)
	print("db reinitiated")
else:
	print("abort")
