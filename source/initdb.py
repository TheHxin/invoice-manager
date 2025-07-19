import os
from sqlmodel import create_engine, Session
from models.invoice import *
from models.user import *
from auth import hashPassword

if input("Delete all data? ") == "":
	try:
		os.remove("./data.db")
	except:
		pass
	sql_url = "sqlite:///./data.db"
	args = {"check_same_thread": False}
	engine = create_engine(sql_url, connect_args=args)
	SQLModel.metadata.create_all(engine)

	with Session(engine) as session:
		root_user = User(
			username="root",
			full_name="root",
			email="root",
			password_hashed=hashPassword("root1234")
		)
		session.add(root_user)
		session.commit()
		session.refresh(root_user)

		print("Root user created: ")
		print(root_user.dict())

	print("db reinitiated")
else:
	print("abort")
