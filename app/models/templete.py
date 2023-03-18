"""
File: templete.py
Path: /app/models/templete.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 02/03/2023
"""

from typing import Optional, List, Any
from pydantic import BaseModel, validator
import re


class SSID(BaseModel):
    port: int
    networkname: str
    name: str
    broadcastSSID: bool
    frequency: str
    securityMode: str
    password: str

class Ghz5(BaseModel):
    protocol: str
    channel: str
    country: str 

class Ghz24(BaseModel):
    country: str
    protocol: str
    channel: str
    channelWidth: str

class WifiConfig(BaseModel):
    ghz24: Optional[Ghz24]
    ghz5: Optional[Ghz5]
    ssid: List[Optional[SSID]]

class LdapServer(BaseModel):
    interface: str
    ipAddress: str
    domain: str
    base: str
    bindDn: str
    bindPassword: str

class SyslogServer(BaseModel):
    interface: str
    ipAddrFqdn: str

class NtpServer(BaseModel):
    interface: str
    ipAddrFqdn: str
        

class InboundNat(BaseModel):
    externalAddress: str
    externalPort: str
    internalAddress: str
    internalPort: str
    lanRoutingInstance: str
    name: str
    protocol: str
    wanNetwork: str

class SplitTunnel(BaseModel):
    vrfName: str
    wanNetwork: str
    diaEnabled: bool
    gatwayEnabled: bool

class LANInterfaceUnitInfo(BaseModel):
    unitId: int
    vlanId: str
    lannetwork: str
    organization: str
    ipv4AssignmentMethod: str
    ipv6AssignmentMethod: str
    routingInstance: str

class LANInterface(BaseModel):
    interface: str
    portNumber: int
    unitInfo: List[Optional[LANInterfaceUnitInfo]]

class WANInterfaceUnitInfo(BaseModel):
    unitId: int
    vlanId: str
    wannetwork: str
    ipv4AssignmentMethod: str
    ipv6AssignmentMethod: str
    monitorIp: str
    priority: int

"^pni-([0-1]{1}|0[0-9]|1[0-2]{1})/([0-3]{1}|0[0-9]|1[0-9]|2[0-9]|3[0-2]{0,1})$"

class WANInterface(BaseModel):
    interface: str
    portNumber: int
    unitInfo: List[Optional[WANInterfaceUnitInfo]]
    
    # @validator('')

class PortType(BaseModel):
    wan: int
    lan: int
    wanLan: int
    lte: int
    wifi: int
    
    @validator('wan')
    def wan_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('lan')
    def lan_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('wanLan')
    def wanlan_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('lte')
    def lte_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('wifi')
    def wifi_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v

class Templete(BaseModel):
    name: str
    tempId: int
    organization: str
    subOrganization: List[Any]
    deviceType: str
    ireach: List[str]
    analytics: str
    numberOfPort: int
    portType: Optional[PortType]
    # status: str
    # wanInterface: List[WANInterface]
    # lanInterface: List[LANInterface]
    # splitTunnel: List[SplitTunnel]
    # inboundNat: List[InboundNat]
    # ntpServer: List[NtpServer]
    # syslogServer: List[SyslogServer]
    # ldapServer: List[LdapServer]
    # wifiConfig: Optional[WifiConfig]
    
    
    @validator('name')
    def name_check(cls, v):
        if not re.match("^\S[a-z0-9_-]{3,14}$", v):
            raise ValueError("Name is not valid.")
        return v
    
    @validator('tempId')
    def tempId_check(cls, v):
        if not v >= 5000 or v > 10000:
            raise ValueError("TempId is not valid.")
        return v
    
    @validator('organization')
    def organization_check(cls, v):
        if not re.match("^\S[a-z0-9_-]{3,14}$", v):
            raise ValueError("Organization is not valid.")
        return v
    
    # @validator('subOrganization')
    # def suborganization_check(cls, v):
        
        
    
    @validator('deviceType')
    def devicetype_check(cls, v):
        if not re.match("^\S[a-z0-9_-]{3,14}$", v):
            raise ValueError("Devicetype is not valid.")
        return v
    
    @validator('ireach')
    def ireach_check(cls, v):
        if not re.sub("^\w[a-zA-Z0-9]{3,14}$","", str(v)):
            raise ValueError("Ireach is not valid.".format(v))
        return v
    
    @validator('analytics')
    def analytics_check(cls, v):
        if not re.match("^\w[a-z]{3,14}$", v):
            raise ValueError("Analytics is not valid.")
        return v
    
    @validator('numberOfPort')
    def port_check(cls, v):
        if not v >= 6 or v > 32:
            raise ValueError("NumberOfPort is not valid.")
        return v
    

    class config:
        schema_extra = {
            "example":{
    "name": "test-temp-04",
    "tempId": 5501,
    "organization": "Ticvic",
    "subOrganization": [
    ],
    "deviceType": "full-mesh",
    "ireach": [
    "iReach1"
    ],
    "analytics": "clusetr",
    "numberOfPort": 6,
    "portType": {
    "WAN": 2,
    "LAN": 2,
    "WANLAN": 0,
    "LTE": 1,
    "WIFI": 1
    },
    "status": "svd",
    "wanInterface": [
        {
            "interface": "pni-0/0",
            "portNumber": "0",
            "unitInfo": [
                {
                    "unitId": 0,
                    "vlanId": "{$il_pni-0_0_test__vlanId}",
                    "wannetwork": "Internet",
                    "ipv4AssignmentMethod": "Static",
                    "ipv6AssignmentMethod": "DHCP",
                    "monitorIp": "192.168.4.4",
                    "priority": "4"
                }
            ]
        }
    ],
    "lanInterface": [
        {
            "interface": "pni-0/1",
            "portNumber": "1",
            "unitInfo": [
                {
                    "unitId": 0,
                    "vlanId": "0",
                    "lannetwork": "lan1",
                    "organization": "test-uv",
                    "ipv4Assignment_method": "Static",
                    "ipv6Assignment_method": "DHCP",
                    "routingInstance": "Ticvic-LAN-VR"
                }
            ]
        }
    ],
    "splitTunnel" : [
        {
            "vrfName": "Ticvic-LAN-VR",
            "wanNetwork": "test-uv-mpls",
            "diaEnabled": "false",
            "gatewayEnabled": "false"
        }
    ],
    "inboundNat": [
        {
            "externalAddress": "{$il_One_InboundExternalAddress}",
            "externalPort": "13-14",
            "internalAddress": "{$il_One_InboundInternalAddress}",
            "internalPort": "13-14",
            "lanRoutingInstance": "Ticvic-LAN-VR",
            "name": "test1",
            "protocol": "TCP",
            "wanNetwork": "test-uv-mpls"
        }
    ],
    "ntpServer": [
        {
            "interface": "lan4",
            "ipAddrFqdn": "4.3.3.3"
        }
    ],
    "syslogServer": [
        {
            "interface": "lan1",
            "ipAddrFqdn": "1.1.1.1"
        }
    ],
    "ldapServer": [
        {
            "interface": "lan4",
            "ipAddress": "192.168.5.10",
            "domain": "testntp.local.com",
            "base": "testbasedn",
            "bindDn": "testbinddn",
            "bindPassword": "ticvic@1234"
        },
    ],
    "wifiConfig": {
            "ghz24": {
                "country": "AZ-Azerbaijan",
                "protocol": "b-2.4GHz",
                "channel": "auto",
                "channelWidth": "40MHz"
            },
            "ghz5": {
                "protocol": "n-5GHz",
                "channel": "36",
                "country": "AZ-Azerbaijan"
            },
            "ssid": [
                {
                    "port": 200,
                    "networkname": "lanwifi",
                    "name": "wifi",
                    "broadcastSSID": "true",
                    "frequency": "2.4-GHz",
                    "securityMode": "wpa2-psk",
                    "password": "wifipassword"
                }
            ]
        }
    }
}      

    
