from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    id : int = Field(default=None, primary_key=True)
    username : str = Field(default=None, index=True, unique=True)

class User(UserBase, table = True):
    password_hashed : str = Field(default=None)

class UserAuth(UserBase):
    token : str

class UserPost(UserBase):
    password : str #this feild is given by the client when creating a new user OBJ