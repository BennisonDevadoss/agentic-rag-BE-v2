from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserSignupParams(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str | None = Field(None, min_length=2)
    email: EmailStr
    mobile_no: PhoneNumber | None = Field(None, min_length=10)

    @field_validator("mobile_no")
    def clean_phone_number(cls, v: str) -> str | None:
        if not v:
            return None
        return v.replace("tel:", "").replace(":", "")


class UserSigninParams(BaseModel):
    email: EmailStr
    password: str
    ip_address: str | None = None


class UserSigninResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    mobile_no: str | None = None
    role: str
