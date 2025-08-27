from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # SQLite数据库配置（用于快速测试）
    database_url: str = "sqlite:///./finance_athena.db"
    
    # JWT配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 应用配置
    app_name: str = "银行投资风险审核系统"
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
