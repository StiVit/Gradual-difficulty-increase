from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    x_plane: int
    y_plane: int
    food_count: int
    n_agents: int
    default_speed: int
    default_sense: int 
    default_energy: int
    
    class Config:
        env_file = '.env' 

load_dotenv()
settings = Settings()