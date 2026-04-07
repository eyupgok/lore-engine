# ingest.py
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("1. RAG Sistemi Başlatılıyor: Lore dosyası okunuyor...")
# 1. VERİYİ YÜKLE: data klasöründeki txt dosyamızı okuyoruz.
loader = TextLoader("data/lore.txt", encoding="utf-8")
documents = loader.load()

print("2. Metin işlenebilir küçük parçalara (chunk) bölünüyor...")
# 2. METNİ PARÇALA: Yapay zekaya koca kitabı tek seferde yut diyemeyiz boğulur. 
# Metni 300 harflik mantıklı paragraflara (chunk) bölüyoruz. Kelimeler kesilmesin diye 50 harf üst üste bindiriyoruz (overlap).
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

print("3. Embedding Modeli yükleniyor (Bu işlem ilk seferde 1-2 dakika sürebilir)...")
# 3. ÇEVİRMEN MODEL (Embedding): Cümleleri matematiksel uzay koordinatlarına çeviren model.
# "all-MiniLM-L6-v2" endüstri standardı, çok hızlı ve hafif bir yerel çevirmendir.
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("4. Vektör Veritabanı oluşturuluyor ve diske kaydediliyor...")
# 4. VERİTABANI: Parçalanan metinleri ve koordinatları alıp 'chroma_db' adında bir klasöre kalıcı olarak yazıyoruz.
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("\n--- İŞLEM TAMAM! ---")
print("Orta Dünya tarihi başarıyla vektör veritabanına kazındı.")