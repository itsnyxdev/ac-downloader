from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dir_name: str = ".acdl"
    ffmpeg_path: str | None = None
    default_quality: str = "medium"
    default_output_dir: str = "./output"
