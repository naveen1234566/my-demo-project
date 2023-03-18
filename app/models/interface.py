import re
from pydantic import BaseModel, validator
from typing import Optional, List


class ReachabilityMonitor(BaseModel):
    icmp: bool
    interval: int
    thershold: int
    
    @validator('icmp')
    def validate_icmp(cls, v):
        if v == None:
            raise ValueError("None is not allowed value")
        return v
    
    @validator('interval')
    def validate_interval(cls, v):
        if not v > 0 or v > 60:
            raise ValueError("Interval  vlaue is required")
        return v
    
    @validator('thershold')
    def validate_thershold(cls, v):
        if not v > 0 or v > 60:
            raise ValueError("Thershold value is required")
        return v 
    
    
class DHCPAddress(BaseModel):
    routePreference: int
    vendorClassIdentifier: str
    reachabilityMonitor: Optional[ReachabilityMonitor]
    
    @validator('routePreference')
    def validate_routePreference(cls, v):
        if not v > 0 or v > 255:
            raise ValueError('routepreference is invalid requirement')
        return v
    
    @validator('vendorClassIdentifier')
    def validate_venderClassIdentifier(cls, v):
        
        regex_name="^\w[a-z 0-9]{0,255}$"  
        
        res=re.match(regex_name, v, flags=0)
         
        if res == None:
            raise ValueError("Network must cotain space.")
        return v
    
    
class StaticArp(BaseModel):
    subnetAddressMask: str
    macAddress: str
    
    @validator('subnetAddressMask')
    def validate_subnetAddressMask(cls, v):

        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/([0-2]{1}|0[0-9]|1[0-9]|2[0-4]|2[0-4]{0,1})$", v):
            raise ValueError("Invalid IP4SubnetAddress".format(v))
        return v
     
    @validator('macAddress')
    def validate_macAddress(cls, v):
        
        if not re.match("((([0-9a-fA-F]){2})\\:){5}"\
             "([0-9a-fA-F]){2}", v):
            raise ValueError("Invalid Mac_Address".format(v))
        return v
    
class StaticAddress(BaseModel):
    ipAddressMask: List[str]
    staticArp: Optional[List[StaticArp]]
    
    @validator('ipAddressMask')
    def validate_ipAddressMask(cls, v):
        
        if not re.sub("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/([0-2]{1}|0[0-9]|1[0-9]|2[0-4]|2[0-4]{0,1})$", "", str(v)):
                raise ValueError("Invalid IpAddress".format(v))
        return v
    
class Ipv4(BaseModel):
    addressType: str
    staticAddress: Optional[StaticAddress]
    
    @validator('addressType')
    def validate_addressType(cls, v):
        value = ["Static", "DHCP"]
        if not v in value:
            raise ValueError("Address only given a list")
        return v

class Bandwith2(BaseModel):
    uplink: int
    downlink: int
    
    @validator('uplink')
    def uplink_validate(cls, v):
        if not v > 1 or v > 10000000:
            raise ValueError('mtu is invalid requirement')
        return v
    
    @validator('downlink')
    def downlink_downlink(cls, v):
        if not v > 1 or v > 10000000:
            raise ValueError('mtu is invalid requirement')
        return v
    
class SubInterface(BaseModel):
    unitId: int
    description: str
    vlanId: int
    networkType: str
    networkName: str
    mtu: int
    bandwith: Optional[Bandwith2]
    ipv4: Optional[Ipv4]
    dhcpAddress: Optional[DHCPAddress]
    
    @validator('unitId')
    def validate_unitId(cls, v):
        if not v > 0 or v > 4095:
            raise ValueError('value is required')
        return v
    
    @validator('description')
    def validate_description(cls, v):
        
        regex_name="^\w[a-zA-Z_\.-]{2,33}$"  
        
        res=re.match(regex_name, v, flags=0)
         
        if res == None:
            raise ValueError("Description must be contian 3 to 32 chars.")
        return v
    
    @validator('vlanId')
    def validate_VlanId(cls, v):
        if not v > 0 or v > 4094:
            raise ValueError(" VlanId above the unitId")
        return v
    
    @validator('networkType')
    def networkType_check(cls, v):
        value = ["WAN", "LAN"]
        if not v in value:
            raise ValueError("Address only given a list")
        return v
    
    @validator('networkName')
    def validate_networkName(cls, v):
        
        regex_name="^\w[a-z A-Z\.-]{2,33}$"  
        
        res=re.match(regex_name, v, flags=0)
         
        if res == None:
            raise ValueError("Network must cotain space.")
        return v
    
    @validator('mtu')
    def validate_mtu(cls, v):
        if not v > 71 or v > 9000:
            raise ValueError('mtu is invalid requirement')
        return v
    
class Bandwith(BaseModel):
    uplink: int
    downlink: int
    
    @validator('uplink')
    def validate_uplink(cls, v):
        if not v > 0 or v > 10000000:
            raise ValueError('Uplink is invalid requirement')
        return v
    
    @validator('downlink')
    def validate_downlink(cls, v):
        if not v > 0 or v > 10000000:
            raise ValueError('Downlink is invalid requirement')
        return v
    
class InterfaceSchemas(BaseModel):
    _id: str
    name: str
    admin: bool
    description: str
    nativeVlanId: int
    mtu: int
    bandwith:Optional[Bandwith]
    subInterface: Optional[List[SubInterface]]
    
    @validator('name')
    def validate_name(cls, v):

        if not re.match("^pni-([0-1]{1}|0[0-9]|1[0-2]{1})/([0-3]{1}|0[0-9]|1[0-9]|2[0-9]|3[0-2]{0,1})$", v):
            raise ValueError("Invalid name".format(v))
        return v
       
    @validator('admin')
    def validate_admin(cls, v):
        if v == None:
            raise ValueError("None is not allowed vlaue")
        return v
       
    @validator('description')
    def validate_description(cls, v):
         
        if not re.match("^\w[a-zA-Z_\.-]{2,33}$", v):
            raise ValueError("Description must be contian 3 to 32 chars.")
        return v   
    
    @validator('nativeVlanId')
    def validate_nativeVlanId(cls, v):
        if not v > 0 or v > 4094:
            raise ValueError('value is invalid')
        return v
    
    @validator('mtu')
    def validate_mtu(cls, v):
        if not v > 71 or v > 9000:
            raise ValueError('mtu is invalid requirement')
        return v
    
    
    
    
    class Config:
        schema_extra = {
            "example": {
  "name": "pni-1/2",
  "admin": "true",
  "description": "Ethernet-interface",
  "nativeVlanId": 1,
  "mtu": 80,
  "bandwidth": {
    "uplink": 10,
    "downlink": 20
  },
  "subInterface": [
    {
      "unitId": 1,
      "description": "Sub-interface",
      "vlanId": 22,
      "networkType": "WAN",
      "networkName": "WAN networks",
      "mtu": 72,
      "bandwidth": {
        "uplink": 800,
        "downlink": 900
      },
      "ipv4": {
        "addressType": "Static",
        "staticAddress": {
          "ipAddressMask": [
            "1.2.3.4/24"
          ],
          "staticArp": [
            {
              "subnetAddressMask": "1.2.3.4/24",
              "macAddress": "aa:bb:cc:34:e5:44"
            }
          ]
        }
      },
      "dhcpAddress": {
        "routePreference": 3,
        "vendorClassIdentifier": "aaa 1212 bbbb",
        "reachabilityMonitor": {
          "icmp": "true",
          "interval": 1,
          "threshold": 2
        }
        
      }
    }
  ]
}
}
    
