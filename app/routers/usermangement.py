from fastapi import APIRouter, status, Response
from ..database import users
from ..models.users import usermanegement
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid

router = APIRouter()

""" Create a new user profile in the database."""
@router.post('/user', status_code=status.HTTP_201_CREATED, summary="Create an user", response_description="Create an user with all the information")
def create(user:usermanegement):
    try:
        if (users.find_one({"email":user.email})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Email already exists"}))
        
        user = user.dict()
        user["created"] = get_time()
        user["_id"] = get_uuid()
        
        try:
            results = users.insert_one(user)
            if results.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"User has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
    
""" Retrieve all user profiles in the database."""   
@router.get('/user', status_code=status.HTTP_200_OK)
def get_all_user(page: int=1, limit:int=25):
    try:
        if not list(users.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"No Data Found", "user":list(users.find())}))
        
        page =(page - 1)* limit
        user= list(users.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total":users.count_documents({}), "user":user}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    

""" Retrieve a user profile with a matching ID. """    
@router.get('/{userId}', status_code=status.HTTP_200_OK)
def get_user(userId: str):
    try:
        if (user := users.find_one({"_id":userId})) is not None:
            return JSONResponse(content=jsonable_encoder({"user":user}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail":f"user with Id ({userId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail":str(e)}))
    
    
"""Update a person by giving only the fields to update"""    
@router.put('/{userId}', status_code=status.HTTP_200_OK)
def update_user(user:usermanegement, userId:str):
    try:
        user = user.dict()
        user["updated"] = get_time()
        if len(user)>= 1:
            update_result = users.update_one({"_id":userId},{"$set":user})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"user with ID ({userId}) not found"}))
        
        if (existing_user := users.find_one({"_id":userId})) is not None:
            return JSONResponse(content=jsonable_encoder({"user":existing_user}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"User with ID ({userId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))


"""Delete a user given its user id"""
@router.delete('/{userId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(userId:str, response: Response):
    try:
        delete_user = users.delete_one({"_id":userId})
        if delete_user.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"user had been deleted successfully"}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"User with ID ({userId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))
