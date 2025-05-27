from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    id : int = Field(default=None, primary_key=True)
    username : str = Field(default=None, index=True, unique=True)
    full_name : str = Field(default=None)
    email : str = Field(default=None)

class User(UserBase, table = True):
    password_hashed : str = Field(default=None)

class UserAuth(UserBase):
    token : str

class UserPost(UserBase):
    password : str #this feild is given by the client when creating a new user OBJ

class UserLogin(SQLModel):
    username : str
    password : str