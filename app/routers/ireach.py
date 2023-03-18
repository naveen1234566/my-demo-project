"""
File: ireach.py
Path: /app/routers/ireac.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 13/03/2023
"""
from fastapi import APIRouter, status, Response
from ..database import iReach
from ..models.ireach import Ireach
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid

router = APIRouter()

""" Create a new ireach profile in the database """
@router.post('/IReach', status_code=status.HTTP_201_CREATED, summary="Create an iReach", response_description="Create an ireach with all the information")
def create(ireach:Ireach):
    try:
        
        ireach  = ireach.dict()
        ireach["created"] = ireach["updated"] = get_time()
        ireach["_id"] = get_uuid()
        
        if (iReach.find_one({"ireachId":ireach["ireachId"]})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Ireach Id already exists"}))
        
        unitid = []
        wannetwork = []
        ip4address = []
        private = []
        for val in ireach["wanConnection"]:
            for value in val["unitInfoList"]:
                unitid.append(value["unitId"])
                wannetwork.append(value["wanNetwork"])
                ip4address.append(value["privateIpv4Address"])
                private.append(value["privateGatewayIp"])
            
            if len(unitid) != len(set(unitid)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch unitId unitinfolist - ({value["unitId"]})'}))

            if len(wannetwork) != len(set(wannetwork)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch wannetwork unitinfolist - ({value["wanNetwork"]})'}))

            if len(ip4address) != len(set(ip4address)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch privateIpv4Address unitinfolist - ({value["privateIpv4Address"]})'}))

            if len(private) != len(set(private)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch privateGatewayIp unitinfolist - ({value["privateGatewayIp"]})'}))
        
        if (ireach["location"]["address1"]) == ireach["location"]["address2"]:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch address1 and address2 - ({ireach["location"]["address1"]})'}))

        try:
            results = iReach.insert_one(ireach)
            if results.acknowledged == True:
                 return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"IReach has been created successfully"}))
            
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Retrive all ireach profile in the database """
@router.get('/IReach/ireach', status_code=status.HTTP_200_OK, summary="Get all iReach")
def get_all(page:int = 1, limit:int = 10):
    try:
        
        if not list(iReach.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"NO DATA FOUND", "ireach":list(iReach.find())}))
        
        page = (page - 1)* limit
        getireach = list(iReach.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total":iReach.count_documents({}), "ireach":getireach}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
""" Retrieve a user profile with a matching ID. """
@router.get('/IReach/{ireachId}', status_code=status.HTTP_200_OK, summary="Get an ireach")
def get_an_ireach(ireachId: str):
    try:
        if (ireachId := iReach.find_one({"_id":ireachId})) is not None:
            return JSONResponse(content=jsonable_encoder({"ireach":ireachId}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"iReach with Id ({ireachId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
"""Update a person by giving only the fields to update"""
@router.put('/IReach/{ireachId}', status_code=status.HTTP_200_OK, summary="Update an ireach")
def update_an(ireach:Ireach, ireachId: str):
    
    try:
        ireach = ireach.dict()
        ireach["updated"] = get_time()
        
        unitid = []
        wannetwork = []
        ip4address = []
        private = []
        for val in ireach["wanConnection"]:
            for value in val["unitInfoList"]:
                unitid.append(value["unitId"])
                wannetwork.append(value["wanNetwork"])
                ip4address.append(value["privateIpv4Address"])
                private.append(value["privateGatewayIp"])
            
            if len(unitid) != len(set(unitid)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch unitId unitinfolist - ({value["unitId"]})'}))

            if len(wannetwork) != len(set(wannetwork)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch wannetwork unitinfolist - ({value["wanNetwork"]})'}))

            if len(ip4address) != len(set(ip4address)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch privateIpv4Address unitinfolist - ({value["privateIpv4Address"]})'}))

            if len(private) != len(set(private)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch privateGatewayIp unitinfolist - ({value["privateGatewayIp"]})'}))
        
        if (ireach["location"]["address1"]) == ireach["location"]["address2"]:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch address1 and address2 - ({ireach["location"]["address1"]})'}))
        
        if len(ireach) >= 1:
            update_result = iReach.update_one({"_id":ireachId}, {"$set":ireach})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"iReach with Id ({ireachId}) not found"}))

        if (existing_ireach := iReach.find_one({"_id":ireachId})) is not None:
            return JSONResponse(content=jsonable_encoder({"ireach":existing_ireach}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"iReach with Id ({ireachId}) not found"}))

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
""" Delete a interface given its a templeteId """
@router.delete("/IReach/{ireachId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interface(ireachId: str, response:Response):
    try:
        ireach = iReach.delete_one({"_id":ireachId})
        
        if ireach.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"Templete has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Templete with ID ({ireachId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))  
