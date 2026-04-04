# main.py  # Ana uygulama dosyası, FastAPI tabanlı REST API sunucusunu başlatır ve yönetir
import uvicorn  # ASGI web sunucusu, FastAPI uygulamalarını yüksek performansla çalıştırmak için kullanılır
from fastapi import FastAPI, HTTPException  # FastAPI framework'ü ve HTTP hata yönetimi için gerekli sınıflar

# Kendi yazdığımız modülleri (katmanları) içe aktarıyoruz  # Proje içi modüllerin import edilmesi
from schemas import AIRequest, AIResponse  # İstek ve yanıt veri modelleri (Pydantic schemas)
from ai_engine import AIEngine  # AI motoru sınıfı, model yükleme ve metin üretimi için

# DİKKAT: Test dosyasında kullandığın çalışan model yolunu buraya yapıştır!  # Model dosya yolunun tanımlanması, test ortamından kopyalanmalı
MODEL_PATH = r"E:\LLM\Qwen2.5-7B-Instruct"  # HuggingFace modelinin yerel diskteki yolu

# 1. FastAPI Uygulamasını Başlat (@RestController mantığı)  # FastAPI uygulamasının başlatılması, Spring MVC'deki Controller gibi
app = FastAPI(title="Yerel AI Mikroservisi", version="2.0 - Clean Architecture")  # FastAPI uygulaması oluşturulur, başlık ve sürüm belirtilir

# 2. Service Katmanını Başlat (Spring'deki @Autowired / Dependency Injection mantığı)  # Servis katmanının başlatılması, bağımlılık enjeksiyonu gibi
# Uygulama ayağa kalkarken model bir kere VRAM'e yüklenir ve istekleri bekler.  # Uygulama başlangıcında model bir kez yüklenir, performans için
print("Controller: AI Servisi ayağa kaldırılıyor...")  # Başlatma mesajı, kullanıcıya bilgi verir
ai_service = AIEngine(model_path=MODEL_PATH)  # AIEngine sınıfından örnek oluşturulur, model yüklenir

# --- UÇ NOKTALAR (ENDPOINTS) ---  # API uç noktalarının tanımlanması bölümü

@app.get("/health")  # Sağlık kontrolü için GET endpoint'i tanımlanır
def health_check():  # Sağlık kontrol fonksiyonu
    """Sistemin ayakta olup olmadığını kontrol eder."""  # Fonksiyon dokümantasyonu
    return {"status": "UP", "message": "Yapay Zeka Servisi Çalışıyor ve İstek Bekliyor."}  # Sağlık durumu yanıtı

@app.post("/api/ask", response_model=AIResponse)  # Soru sorma için POST endpoint'i, yanıt modeli belirtilir
def ask_question(request: AIRequest):  # Soru sorma fonksiyonu, istek modelini alır
    """
    Java'dan gelen JSON isteğini (AIRequest) alır, 
    İş Mantığına (AIEngine) iletir ve cevabı (AIResponse) döner.
    """  # Fonksiyon açıklaması
    try:  # Hata yakalama bloğu
        # Controller'ın tek işi yönlendirmektir, modelin nasıl çalıştığını bilmez!  # Controller sorumluluğu, iş mantığını bilmez
        answer = ai_service.generate_answer(  # AI servisi üzerinden cevap üretilir
            prompt=request.prompt,  # Kullanıcı sorusu
            max_tokens=request.max_tokens,  # Maksimum token sayısı
            temperature=request.temperature  # Rastgelelik parametresi
        )
        
        # Üretilen cevabı DTO formatına sokup dışarı dön  # Cevap DTO'ya dönüştürülür
        return AIResponse(answer=answer)  # Yanıt döndürülür
        
    except Exception as e:  # Genel hata yakalama
        # İşler ters giderse HTTP 500 dön (Exception Handling)  # Hata durumunda 500 hatası döndürülür
        raise HTTPException(status_code=500, detail=f"Model işleme hatası: {str(e)}")  # HTTP exception fırlatılır

# Sunucuyu başlat  # Ana blok, sunucu başlatma
if __name__ == "__main__":  # Dosya doğrudan çalıştırılırsa
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Uvicorn ile sunucu başlatılır, localhost 8000 portunda