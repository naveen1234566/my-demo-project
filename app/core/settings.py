import pydantic

__all__ = ("api_settings", "mongo_setting")

class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        
class APISettings(pydantic.BaseSettings): 
    title:str
    description:str
    version: str
    docs_url: str
    redocs_url:str
    openapi_url:str
    
    class Config(BaseSettings.Config):
        env_prefix = "API_"
        
class MongoSettings(pydantic.BaseSettings):
    uri: str
    database: str
    
    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"
        
api_settings = APISettings()
mongo_settings = MongoSettings()