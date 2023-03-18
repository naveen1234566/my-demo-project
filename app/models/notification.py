"""
File: notification.py
Path: /app/models/notification.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 13/03/2023
"""

import re
from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional

class ConditionValue(BaseModel):
    attribute: str
    operator: str
    value: str
    
    @validator('attribute')
    def attribute_check(cls, v):
        if not re.match("^\w[a-zA-Z]{3,14}$", v):
            raise ValueError("Attribute must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Attribute first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Attribute last one is not coming for (- or _)")
        return v
    
    @validator('operator')
    def operator_check(cls, v):
        if not re.match("^\w[A-Z]{3,14}$", v):
            raise ValueError("Operator must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Operator first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Operator last one is not coming for (- or _)")
        return v
    
    @validator('value')
    def value_check(cls, v):
        if not re.match("^\w[a-z-]{3,20}$", v):
            raise ValueError("Value must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Value first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Value last one is not coming for (- or _)")
        return v
    
class Conditions(BaseModel):
    conditionName: str
    conditionValue: List[ConditionValue]
    
    @validator('conditionName')
    def conditionName_check(cls, v):
        if not re.match("^\w[a-zA-Z]{3,14}$", v):
            raise ValueError("ConditionName must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("ConditionName first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("ConditionName last one is not coming for (- or _)")
        return v

class SMSConfiguration(BaseModel):
    phone: str
    text : str
    
    @validator('phone')
    def phone_check(cls, v):
        if not re.match("^[+][0-9]{12}$", v):
            raise ValueError("Phone number is required")
        return v
    
    @validator('text')
    def text_check(cls, v):
        if not re.match("^\w[a-zA-Z-]{3,14}$", v):
            raise ValueError("Text must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Text first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Text last one is not coming for (- or _)")
        return v
        

class EmailConfiguration(BaseModel):
    subject: str
    toAddress: List[str]
    ccAddress: List[str]
    message: str
    
    @validator('subject')
    def subject_check(cls, v):
        if not re.match("^\w[a-zA-Z]{3,14}$", v):
            raise ValueError("Subject must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Subject first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Subject last one is not coming for (- or _)")
        return v
    
    @validator('toAddress')
    def toAddress_check(cls, v):
        
        if not re.match(r'\b[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Z|a-z]{2,7}\b', v):
            raise ValueError("Email is required")
        return v
    
    # @validator('ccAddress')
    # def ccAddress_check(cls, v):
    #     if not re.match("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,6}$", v):
    #         raise ValueError("ccAddress email is required")
    #     return v
    
    @validator('message')
    def message_check(cls, v):
        if not re.match("^\w[a-zA-Z]{3,14}$", v):
            raise ValueError("Message must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Message first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Message last one is not coming for (- or _)")
        return v

class CommunicationDetails(BaseModel):
    emailConfiguration: EmailConfiguration
    smsConfiguration: SMSConfiguration


class Notification(BaseModel):
    _id: str
    rulename: str
    template: str
    organization: List[str]
    communicationDetails: CommunicationDetails
    conditions: List[Conditions]
    
    @validator('rulename')
    def rulename_check(cls, v):
        if not re.match("^\w[a-zA-Z]{3,14}$", v):
            raise ValueError("Rulename must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Rulename first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Rulename last one is not coming for (- or _)")
        return v
    
    @validator('template')
    def templete_check(cls, v):
        if not re.match("^\w[a-z]{3,14}$", v):
            raise ValueError("template must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("template first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("template last one is not coming for (- or _)")
        return v
    
    @validator('organization')
    def organization_check(cls, v):
        if not range(len(v) <= 2):
            raise ValueError("Suborganization must contain two values.")
        return v
    
    class Config:
        schema_extra={
            "example": {
                "rulename": "TestRule",
                "template": "testtemp",
                "organization": [
                "Ticvic",
                "Infoquick"
                ],
                "communicationDetails": {
                "emailConfiguration": {
                    "subject": "TestSubject",
                    "toAddress": [
                    "sam@ticvic.com", "raju@ticvic.com", "guru@ticvic.com"
                    ],
                    "ccAddress": [
                    "santhosh@ticvic.com",
                    "jayakkumar@ticvic.com",
                    "aravinth@ticvic.com"
                    ],
                    "message": "TestMessage"
                },
                "smsConfiguration": {
                    "phone": "+919980800502",
                    "text": "Test-SMS"
                }
                },
                "conditions": [
                {
                    "conditionName": "testone",
                    "conditionValue": [
                    {
                        "attribute": "alarmtype",
                        "operator": "EQUALS",
                        "value": "login-auth-failed"   
                    },
                    {
                        "attribute": "alarmText",
                        "operator": "EQUALS",
                        "value": "login-auth-failed" 
                    }
                    ] 
                },
                {
                    "conditionName": "newTest",
                    "conditionValue": [
                    {
                        "attribute": "deviceName",
                        "operator": "NOLIKE",
                        "value": "config-change"
                    },
                    {
                        "attribute": "deviceType",
                        "operator": "NOLIKE",
                        "value": "config-change"
                    }
                    ]
                }
                ]
            }
                        }
                    