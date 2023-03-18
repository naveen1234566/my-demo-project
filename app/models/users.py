import re
from pydantic import BaseModel, validator, EmailStr


class usermanegement(BaseModel):
    _id: str
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    password: str
    # confirmpassword: str

    @validator('firstname')
    def validate_firstname(cls, v):
        
        if not re.match("^\S[A-Za-z@#&$%]{2,9}$", v):
            raise ValueError("Name must be contian 3 to 10 chars")
        return v
    
    @validator('lastname')
    def validate_lastname(cls, v):
        
        if not re.match("^\S[A-Za-z@#&+-]{2,9}$", v):
            raise ValueError("Name must be contian 3 to 10 chars")
        return v
    
    @validator('email')
    def validate_email(cls, v):
        
        if not re.match("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,6}$", v):
            raise ValueError("Email is required")
        return v
    
    # "^\\+?[1-9][0-9]{7,14}$"
    # r"(\+420)?(\s*)?(\d{3})(\s*)?\(d{3})(\s*)?\(d{3})"
    
    @validator('phone')
    def validate_phone(cls, v):
        
        if not re.match("^[+][0-9]{12}$", v):
            raise ValueError("Phone number is required")
        return v

    @validator('password')
    def validate_password(cls, v):
        
        if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,12}$", v):
            raise ValueError("Password is required")
        return v
    
    # @validator('confirmpassword')
    # def validate_confirm_password(cls, v):
        
    #     if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,12}$", v):
    #         raise ValueError("Password is required")
    #     return v
    
    class Config:
        schema_extra = {
            "example":{
                "firstname":"naveen",
                "lastname":"naveen",
                "email":"naveen@gmail.com",
                "phone":"+917904602269",
                "password":"Naveen@31",
                
            }
        }
# class Login(BaseModel):
#     username: str
#     password: str
    
# class Token(BaseModel):
#     access_token: str
#     token_type: str
    
# class TokenData(BaseModel):
#     username: Optional[str] = None