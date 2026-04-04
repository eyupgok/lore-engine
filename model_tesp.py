import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# DİKKAT: Buraya kendi indirdiğin modelin (örneğin Qwen) klasör yolunu yaz.
# Windows yollarında hata almamak için başına 'r' (raw string) koyuyoruz.
MODEL_PATH = r"E:\LLM\Qwen2.5-7B-Instruct"

print("1. Quantization (Sıkıştırma) ayarları yapılıyor...")
# 8GB VRAM'in kahramanı olan ayar bloğu:
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,                    # 4-bit sıkıştırmayı aç
    bnb_4bit_compute_dtype=torch.float16, # Hesaplamalar hız için 16-bit kalsın
    bnb_4bit_quant_type="nf4"             # En verimli sıkıştırma algoritması (Normalized Float 4)
)

print("2. Model GPU'ya yükleniyor. Bu işlem diskin hızına göre 1-2 dakika sürebilir...")
try:
    # 1. Adım: Tokenizer'ı (Metin-Sayı dönüştürücü) yükle
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    
    # 2. Adım: Modeli 4-bit sıkıştırarak yükle
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        quantization_config=quant_config,
        device_map="auto" # PyTorch'a modeli doğrudan ekran kartına atmasını söyler
    )
    
    print("\n--- BAŞARILI! ---")
    print("Model 8GB VRAM'e sığdırıldı ve başarıyla yüklendi.")
    
    # Ne kadar VRAM harcadığımızı görelim
    allocated_vram = torch.cuda.memory_allocated() / (1024**3)
    print(f"Kullanılan VRAM: {allocated_vram:.2f} GB")
    
except Exception as e:
    print(f"\nHATA! Yükleme başarısız oldu:\n{e}")