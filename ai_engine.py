# ai_engine.py  # Bu dosya AI motoru sınıfını içerir
import torch  # PyTorch kütüphanesi, tensör ve GPU hesaplama desteği sağlar
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline  # HuggingFace model/tokenizer araçları

class AIEngine:  # AI motorunu sarmalayan sınıf
    def __init__(self, model_path: str):  # Yapıcı, model yolunu parametre olarak alır
        print("AIEngine: Sistem başlatılıyor, model GPU'ya yükleniyor (4-bit)...")  # Başlangıç mesajı
        
        quant_config = BitsAndBytesConfig(  # Model kuantizasyon ayarları oluşturulur
            load_in_4bit=True,  # 4-bit düşük bellekli model yükleme
            bnb_4bit_compute_dtype=torch.float16,  # Hesaplama için float16 kullan
            bnb_4bit_quant_type="nf4"  # Nf4 kuantizasyon tipini seç
        )
        
        try:  # Model yükleme işlemini dene
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)  # Tokenizer'ı model yolundan yükle
            self.model = AutoModelForCausalLM.from_pretrained(  # Dil modelini yükle
                model_path,
                quantization_config=quant_config,  # Kuantizasyon ayarını uygula
                device_map="auto"  # Mümkünse GPU'ya otomatik dağıtım
            )
            
            self.ai_pipeline = pipeline(  # Text generation pipeline'ı oluştur
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer
            )
            print("AIEngine: Model başarıyla servise entegre edildi!")  # Başarılı yükleme mesajı
            
        except Exception as e:  # Hata durumunu yakala
            print(f"Kritik Hata! Model yüklenemedi: {e}")  # Hata mesajı yaz
            raise e  # Hatanın yükseltilmesi

    def generate_answer(self, prompt: str, max_tokens: int, temperature: float) -> str:  # Cevap üretme fonksiyonu
        # 1. STANDART CHAT FORMATI
        # Modele bir sistem kişiliği (System Prompt) ve kullanıcının sorusunu veriyoruz.
        messages = [  # Konuşma dizisi oluşturulur
            {"role": "system", "content": "Sen yardımsever ve Türkçe konuşan bir asistansın. Kısa, net ve öz cevaplar verirsin."},  # Sistem rolü
            {"role": "user", "content": prompt}  # Kullanıcı rolü
        ]
        
        # 2. TOKENIZER TEMPLATE UYGULAMASI (Kritik Çözüm)
        # Modelin kendi özel etiketlerini otomatik olarak ekler (Örn: <|im_start|>, <|im_end|>)
        formatted_prompt = self.tokenizer.apply_chat_template(  # Prompta model formatı uygula
            messages,
            tokenize=False,  # Özel tokenizasyon devre dışı bırakıldı
            add_generation_prompt=True  # Üretim kısmı için gerekli eklemeyi yap
        )
        
        # 3. ÜRETİM VE DURMA SİNYALİ (EOS TOKEN)
        result = self.ai_pipeline(  # Metin üretimini çalıştır
            formatted_prompt,
            max_new_tokens=max_tokens,  # Üretilecek maksimum yeni token
            temperature=temperature,  # Rastgelelik sıcaklığı
            do_sample=True,  # Örnekleme modu
            truncation=True,  # Uzunluk sınırını uygula
            eos_token_id=self.tokenizer.eos_token_id, # Modele "Cevabın bitince DUR" emri
            pad_token_id=self.tokenizer.eos_token_id  # Dolgu tokenı olarak EOS kullan
        )
        
        # 4. ÇIKTIYI TEMİZLEME
        generated_text = result[0]["generated_text"]  # Üretilen tam metin
        answer_only = generated_text[len(formatted_prompt):].strip()  # Sadece yeni cevap kısmını ayıkla
        
        return answer_only  # Temizlenmiş cevabı döndür
