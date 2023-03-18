from fastapi import APIRouter, status, Response
from ..database import notification
from ..models.notification import Notification
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid


router = APIRouter()

""" Create a new templete profile in the database."""
@router.post('/Notification', status_code=status.HTTP_201_CREATED, summary="Create an Notifications", response_description="Create an Notifications with all the information")
def create(notifications:Notification):
    # try:

        notifications = notifications.dict()
        notifications["created"] = notifications["updated"] = get_time()
        notifications["_id"] = get_uuid()
        
        if (notification.find_one({"rulename":notifications["rulename"]})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Notifications name already exists"}))
        return notifications
        
        try:
            results = notification.insert_one(notifications)
            if results.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"Notifications has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    # except Exception as e:
    #     return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    