# ai_engine.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
# --- YENİ EKLENEN KÜTÜPHANELER ---
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class AIEngine:
    def __init__(self, model_path: str):
        print("AIEngine: Sistem başlatılıyor...")
        
        # 1. LLM MODELİNİ YÜKLEME (Aşçıyı mutfağa alma - Eski kod)
        print("AIEngine: Model GPU'ya yükleniyor (4-bit)...")
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4"
        )
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quant_config,
                device_map="auto"
            )
            
            self.ai_pipeline = pipeline(
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer
            )
            print("AIEngine: LLM Modeli başarıyla yüklendi!")

            # 2. RAG VERİTABANINI YÜKLEME (Kütüphaneyi mutfağa getirme - YENİ KOD)
            print("AIEngine: ChromaDB Vektör Veritabanı bağlanıyor...")
            # Çevirmeni tekrar çağırıyoruz çünkü gelen soruyu da koordinata çevireceğiz
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            # Diskteki chroma_db klasörünü okuma modunda açıyoruz
            self.db = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
            print("AIEngine: Tüm sistemler servise hazır! Lore Uzmanı aktif.")
            
        except Exception as e:
            print(f"Kritik Hata! Sistem yüklenemedi: {e}")
            raise e

    def generate_answer(self, prompt: str, max_tokens: int, temperature: float) -> str:
        # --- 1. AŞAMA: KOPYA ÇEKME (RETRIEVAL) ---
        # Kullanıcının sorusuna en çok benzeyen (matematiksel olarak en yakın) 2 paragrafı veritabanından getir.
        search_results = self.db.similarity_search(prompt, k=2)
        
        # Gelen paragrafları alt alta ekleyerek bir "Kopya Kağıdı" metni oluştur.
        context_text = ""
        for doc in search_results:
            context_text += doc.page_content + "\n\n"
            
        # --- 2. AŞAMA: PROMPT MÜHENDİSLİĞİ (AUGMENTATION) ---
        # Modele yeni ve çok katı bir anayasa (System Prompt) veriyoruz.
        system_message = f"""Sen Orta Dünya tarihi konusunda uzman bir bilgesin.
Kullanıcının sorusunu SADECE aşağıdaki 'KOPYA KAĞIDI' bölümünde verilen bilgilere dayanarak cevapla.
Eğer sorunun cevabı bu bilgilerde yoksa kesinlikle uydurma ve "Bu bilgi kadim kitaplarda yer almıyor" de.

KOPYA KAĞIDI:
{context_text}"""

        # --- 3. AŞAMA: ÜRETİM (GENERATION) ---
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        result = self.ai_pipeline(
            formatted_prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            truncation=True,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        generated_text = result[0]["generated_text"]
        answer_only = generated_text[len(formatted_prompt):].strip()
        
        return answer_only