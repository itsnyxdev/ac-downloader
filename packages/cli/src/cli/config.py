from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dir_name: str = ".acdl"
