from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    skip: int = Field(default=0, ge=0, description='Number of items to skip')
    limit: int = Field(
        default=10, ge=1, description='Maximum number of items to return'
    )
    sort: str | None = Field(default=None, description='Field to sort by')
    order: str | None = Field(
        default=None, description='Order of sorting (asc/desc)'
    )
