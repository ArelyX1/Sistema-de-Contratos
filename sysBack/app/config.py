from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    RW_URL: str = ""
    RO_URL: str = ""
    
    class Config:
        env_file = ".env.local"  # ✅ Lee automáticamente
    
    @property
    def primary_url(self) -> str:  # RW + Local fallback
        return self.RW_URL or self.DATABASE_URL
    
    @property
    def readonly_url(self) -> str:  # RO + Local fallback
        return self.RO_URL or self.DATABASE_URL

settings = Settings()
