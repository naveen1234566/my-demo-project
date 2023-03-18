from fastapi import APIRouter, status, Response
from ..database import templete
from ..models.templete import Templete
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid

router = APIRouter()


""" Create a new templete profile in the database."""
@router.post('/Templete', status_code=status.HTTP_201_CREATED, summary="Create an templete", response_description="Create an templete with all the information")
def create(templetes:Templete):
    try:

        templetes = templetes.dict()
        templetes["created"] = templetes["updated"] = get_time()
        templetes["_id"] = get_uuid()
        
        if (templete.find_one({"tempId":templetes["tempId"]})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Temp Id already exists"}))
        
        """ WanInterface with data """
        wan_interface = []
        for wanVal in templetes["wanInterface"]:
            wan_interface.append(wanVal["interface"])
       
        wan_unitId = []
        wan_network = []
            
        for Interface in templetes["wanInterface"]:
            # print(Interface["interface"].split('/')[1])
            for unitInfo in Interface["unitInfo"]:
                wan_unitId.append(unitInfo["unitId"])
                
            for wannetwork in Interface["unitInfo"]:
                wan_network.append(wannetwork["wannetwork"])
            
            if len(wan_network) != len(set(wan_network)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface WanNetwork - ({Interface["interface"]})'}))
               
            if len(wan_unitId) != len(set(wan_unitId)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface unitId - ({Interface["interface"]})'}))
            
            if int(Interface["interface"].split('/')[1]) != Interface["portNumber"]:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Portnumber and WANinterface - ({Interface["portNumber"]})'}))
            
            if len(wan_interface) != len(set(wan_interface)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Invalid WANinterface({wanVal["interface"]}) name Types'}))
        
        """ LanInterface with data """
        lan_interface = []
        for lanVal in templetes["lanInterface"]:
            lan_interface.append(lanVal["interface"]) 
        
        lan_unitId = []
        lan_network = []
        lan_organization = []
        
        for Interface_name in templetes["lanInterface"]:
            for unit_lan in Interface_name["unitInfo"]:
                lan_unitId.append(unit_lan["unitId"])
            
            for lannet_works in Interface_name["unitInfo"]:
                lan_network.append(lannet_works["lannetwork"])
            
            for organization_name in Interface_name["unitInfo"]:
                lan_organization.append(organization_name["organization"])
            
            for laninterface in lan_organization:
                print(laninterface)
                if templetes["Organization"] != laninterface:
                    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Organizatio and Lan_organization -({Interface_name["interface"]})'}))
            
            if len(lan_network) != len(set(lan_network)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface LanNetwork - ({Interface_name["interface"]})'}))
                
            if len(lan_unitId) != len(set(lan_unitId)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LANInterface unitId - ({Interface_name["interface"]})'}))
                
            if int(Interface_name["interface"].split('/')[1]) != Interface_name["portNumber"]:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch portnumber and LANinterface - ({Interface_name["interface"]})'}))

            if len(lan_interface) != len(set(lan_interface)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Invalid LANinterface ({lanVal["interface"]}) name Types'}))
                
        if templetes["portType"]["wan"] != len(templetes["wanInterface"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WAN interface and WAN - ({templetes["portType"]["wan"]}) values'}))
        
        if templetes["portType"]["lan"] != len(templetes["lanInterface"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LAN interface and LAN - ({templetes["portType"]["lan"]}) values'}))
        
        if templetes["numberOfPort"] != (sum(templetes["portType"].values())):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Numberofport and PortType - ({templetes["numberOfPort"]}) values'}))

        # return templetes
        
        try:
            results = templete.insert_one(templetes)
            if results.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"templete has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
        # print(templetes["lanInterface"])
        # print(templetes["wanInterface"])
        # print(templetes["wanInterface"][-1].values())
        # print(templetes["numberOfPort"])
        # print(sum(templetes["portType"].values()))
        # print(len(templetes["wanInterface"]))
        # print(len(templetes["lanInterface"]))
        # return templetes["wanInterface"]
        # print(templetes["portType"]["wan"])
        # return templetes["portType"]
        # print(templetes["portType"])
    
""" Retrieve all templete profiles in the database """    
@router.get('/Templete', status_code=status.HTTP_200_OK, summary= "Get all templete")
def read_all(page: int=1, limit: int = 10):
    try:
        
        if not list(templete.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"NO DATA FOUND", "templete":list(templete.find())}))
        
        page = (page - 1) * limit
        getTemplete = list(templete.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total": templete.count_documents({}), "templete":getTemplete}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
@router.get('/{templeteId}', status_code=status.HTTP_200_OK, summary="Get an templete")
def get_an_templete(templeteId: str):
    try:
        if (templeteId := templete.find_one({"_id":templeteId})) is not None:
            return JSONResponse(content=jsonable_encoder({'templete':templeteId}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Templete with Id ({templeteId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))

"""Update a person by giving only the fields to update"""
@router.put('Templete/{templeteId}', status_code=status.HTTP_200_OK, summary="Update an templete")
def update_an(user:Templete, templeteId: str):
    try:
        
        user = user.dict()
        user["updated"] = get_time()
        if len(user) >= 1:
            update_result = templete.update_one({"_id": templeteId}, {"$set": user})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Interface with ID ({templeteId}) not found"}))

        if (
            existing_interface := templete.find_one({"_id": templeteId})
        ) is not None:
            
            return JSONResponse(content=jsonable_encoder({"user": existing_interface}))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Interface with ID ({templeteId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Delete a interface given its a templeteId """
@router.delete("/Templete/{templeteId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interface(templeteId: str, response:Response):
    try:
        interface = templete.delete_one({"_id":templeteId})
        if interface.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"Templete has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Templete with ID ({templeteId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))  


    