# schemas.py
from pydantic import BaseModel, Field

# Java'dan bize gelecek olan isteğin (Request) şablonu
class AIRequest(BaseModel):
    prompt: str = Field(..., description="Kullanıcının modele soracağı soru")
    max_tokens: int = Field(256, description="Üretilecek maksimum kelime/token sayısı")
    temperature: float = Field(0.7, description="Cevabın yaratıcılık seviyesi (0.0 - 1.0)")

# Bizim Java'ya döneceğimiz cevabın (Response) şablonu
class AIResponse(BaseModel):
    answer: str
    status: str = "SUCCESS"