"""
File: ireach.py
Path: /app/models/ireach.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 14/03/2023
"""

import re
from pydantic import BaseModel, validator
from typing import List, Dict, Optional

class Location(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    zip: str
    latitude: float
    longitude: float
    
    @validator('address1')
    def address1_check(cls, v):
        if not re.match("^\w[a-z A-Z 0-9_\-:,]{3,32}$", v):
            raise ValueError("address1 must cotain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("address1 first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("address1 last one is not coming for (- or _)")
        return v
    
    @validator('address2')
    def address2_check(cls, v):
        if not re.match("^\w[a-z A-Z 0-9_\-:,]{3,32}$", v):
            raise ValueError("address2 must cotain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("address2 first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("address2 last one is not coming for (- or _)")
        return v
    
    @validator('city')
    def city_check(cls, v):
        if not re.match("^\w[a-zA-Z\-,]{3,32}$", v):
            raise ValueError("city must cotain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("city first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("city last one is not coming for (- or _)")
        return v
    
    @validator('state')
    def state_check(cls, v):
        if not re.match("^\w[a-z A-Z\-]{3,32}$", v):
            raise ValueError("state must cotain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("state first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("state last one is not coming for (- or _)")
        return v
    
    @validator('country')
    def country_check(cls, v):
        if not re.match("^\w[a-zA-Z\-,]{3,32}$", v):
            raise ValueError("country must cotain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("country first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("country last one is not coming for (- or _)")
        return v
    
    @validator('zip')
    def zip_check(cls, v):
        if not re.match("^\d[0-9]{1,6}$", v):
            raise ValueError("zip number is required")
        return v
    
    @validator('latitude')
    def latitude_check(cls, v):
        if not ("^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?[0-8]\d((\.)|\.\d{1,6})?)|(0*?90((\.)|\.0{1,6})?))$", v):
            raise ValueError("Latitude is required.")
        return v
    
    @validator('longitude')
    def longitude_vheck(cls, v):
        if not ("^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?[0-8]\d((\.)|\.\d{1,6})?)|(0*?90((\.)|\.0{1,6})?))$", v):
            raise ValueError("Longitude is required.")
        return v

class UnitInfoList(BaseModel):
    unitId: int
    wanNetwork: str
    privateIpv4Address: str
    privateGatewayIp: str
    coo: bool
    primary: Optional[bool]
    vlanId: Optional[int]
    
    @validator('unitId')
    def unitId_check(cls, v):
        if not v > 0 or v >= 100:
            raise ValueError("unitId must contain 0 to 200 range.")
        return v
    
    @validator('wanNetwork')
    def wannetwork_check(cls, v):
        if not re.match("^\w[A-Z0-9]{3,15}$", v):
            raise ValueError("Wannetwork must cotain 3 to 15 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Wannetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Wannetwork last one is not coming for (- or _)")
        return v
    
    @validator('privateIpv4Address')
    def privateIpv4Address_check(cls, v):
        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/([0-2){1}|0[0-9]|1[0-9]|2[0-4]{0,1})$", v):
            raise ValueError("privateIpv4Address is required")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("privateIpv4Address first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("privateIpv4Address last one is not coming for (- or _)")
        return v
    
    @validator('privateGatewayIp')
    def privateGatewayIp_check(cls, v):
        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", v):
            raise ValueError("privateGatewayIp is required")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("privateGatewayIp first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("privateGatewayIp last one is not coming for (- or _)")
        return v
    
    @validator('coo')
    def coo_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('primary')
    def primary_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('vlanId')
    def vlanId_check(cls, v):
        if not v > 0 or v >= 100:
            raise ValueError("vlanId must contain 0 to 200 range.")
        return v
    
class WANConnection(BaseModel):
    interface: str
    unitInfoList: List[UnitInfoList]
    
    @validator('interface')
    def interface_check(cls, v):
        if not re.match("^pni-([0-0]{1})/([0-9]{1,3})$", v):
            raise ValueError("Invalid interface".format(v))
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Interface first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Interface last one is not coming for (- or _)")
        return v

class Ireach(BaseModel):
    
    _id: str
    name: str
    description: str
    ireachId: int
    parentOrganization: str
    ireachPeer: List[str]
    analytics: str
    onboardingIp: str
    onboardingOtp: str
    wanConnection: List[WANConnection]
    location: Optional[Location]
    status: str
    
    @validator('name')
    def name_check(cls, v):
        if not re.match("^\w[a-zA-Z0-9]{3,14}$", v):
            raise ValueError("Name value  must cotain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Name first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Name last one is not coming for (- or _)")
        return v
    
    @validator('description')
    def description_check(cls, v):
        if not re.match("^\w[a-z A-Z]{3,36}$", v):
            raise ValueError("Description  must cotain 3 to 36 characters.")
        return v
    
    @validator('ireachId')
    def ireachId_check(cls, v):
        if not v >= 0 or v > 32:
            raise ValueError("ireachId must contain 0 to 32 range.")
        return v
    
    @validator('parentOrganization')
    def parentOrganization_check(cls, v):
        if not re.match("^\w[a-zA-Z0-9]{3,36}$", v):
            raise ValueError("parentOrganization  must cotain 3 to 36 characters.")
        return v
    
    @validator('ireachPeer')
    def ireachPeer_check(cls, v):
        if not range(len(v) <= 2):
            raise ValueError("Suborganization must contain two values.")
        return v
    
    @validator('onboardingIp')
    def onboardingIp_check(cls, v):
        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", v):
            raise ValueError("onboardingIp  must cotain 3 to 36 characters.")
        return v
    
    @validator('onboardingOtp')
    def onboardingOtp_check(cls, v):
        if not re.match("^\d[0-9]{1,6}$", v):
            raise ValueError("onboardingOtp number is required")
        return v
    
    @validator('status')
    def status_check(cls, v):
        if not re.match("^\w[a-zA-Z]{0,36}$", v):
            raise ValueError("status  must cotain 3 to 36 characters.")
        return v
    
    
    class Config:
        schema_extra= {
            "example":{
                "name": "iReach1",
                "description": "ireach device",
                "ireachId": 2,
                "parentOrganization": "parentOrg1",
                "ireachPeer": [
                    "prodVc1"
                ],
                "analytics": "prodAnalytics",
                "onboardingIp": "10.234.0.103",
                "onboardingOtp": "673788",
                "wanConnection": [
                    {
                    "interface": "pni-0/1",
                    "unitInfoList": [
                        {
                        "unitId": 1,
                        "wanNetwork": "WAN2",
                        "privateIpv4Address": "10.234.1.103/24",
                        "privateGatewayIp": "10.234.1.1",
                        "coo": "true",
                        "primary": "true"
                        },
                        {
                        "unitId": 1,
                        "vlanId": 4,
                        "wanNetwork": "WAN1",
                        "privateIpv4Address": "10.234.1.103/24",
                        "privateGatewayIp": "10.234.1.1",
                        "coo": "true"
                        }
                    ]
                    }
                ],
                "location": {
                    "address1": "No: 123, ABCD street",
                    "address2": "No: 123, ABCD street",
                    "city": "Chennai",
                    "state": "Tamil Nadu",
                    "country": "India",
                    "zip": "600001",
                    "latitude": 13.08268,
                    "longitude": 80.270718
                },
                "status": "svd"
                }
                            }
        