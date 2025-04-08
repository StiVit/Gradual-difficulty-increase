from pydantic_settings import BaseSettings

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


settings = Settings()