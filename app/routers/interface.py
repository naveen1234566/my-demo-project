"""
File: interface.py
Path: /app/models/interface.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 01/03/2023
"""

from fastapi import APIRouter, status, Response
from ..database import interfaces
from ..models.interface import InterfaceSchemas
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid


router = APIRouter()

""" Create a new user profile in the database."""
@router.post('/etherNet/interface', status_code=status.HTTP_201_CREATED, summary="Create an interface", response_description="Create an interface with all the information")
def create(interface:InterfaceSchemas):
    try:
        # interfaces(database name)
        if (interfaces.find_one({"name":interface.name})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Name already exists"}))
        
        interface = interface.dict()
        interface["created"] = get_time()
        interface["_id"] = get_uuid()
        
        try:
            results = interfaces.insert_one(interface)
            if results.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"Interface has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))


""" Retrieve all interface profiles in the database."""       
@router.get('/etherNet/interface', status_code=status.HTTP_200_OK)
def get_all_interface(page: int=1, limit:int=25):
    try:
        # interfaces(database name)
        if not list(interfaces.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"No Data Found", "interface":list(interfaces.find())}))
        
        page =(page - 1)* limit
        getInterface = list(interfaces.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total":interfaces.count_documents({}), "interface":getInterface}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))


""" Retrieve a interface profile with a matching ID. """    
@router.get('/etherNet/{interfaceId}', status_code=status.HTTP_200_OK)
def get_interface(interfaceId: str):
    try:
        if (interfaceId := interfaces.find_one({"_id":interfaceId})) is not None:
            return JSONResponse(content=jsonable_encoder({"interface":interfaceId}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Interface with Id ({interfaceId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))


"""Update a person by giving only the fields to update"""    
@router.put('/etherNet/{interfaceId}', status_code=status.HTTP_200_OK)
def update_interface(interface:InterfaceSchemas, interfaceId: str):
    try:
        interface = interface.dict()
        interface["updated"] = get_time()
        if len(interface) >= 1:
            update_result = interfaces.update_one({"_id":interfaceId}, {"$set": interface})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Interface with ID ({interfaceId}) not found"}))
        
        if(existing_interface := interfaces.find_one({"_id":interfaceId})) is not None:
            return JSONResponse(content=jsonable_encoder({"interface": existing_interface}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail":f"Interface with ID ({interfaceId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(({"detail":str(e)})))
    

"""Delete a interface given its interface id"""
@router.delete('/etherNet/{interfaceId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_interface(interfaceId:str, response:Response):
    try:
        delete_interface = interfaces.delete_one({"_id":interfaceId})
        if delete_interface.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"Interface has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Interface with ID ({interfaceId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    