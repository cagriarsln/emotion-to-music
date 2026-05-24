Emotion to Music

Türkçe metin girişinden duygu analizi yaparak müzik üreten bir uygulama.

Nasıl çalışır:



Kullanıcı Türkçe bir metin veya şiir girer

Gemini API metni analiz edip müzik promptu oluşturur

MusicGen modeli bu prompttan müzik üretir



Kullanılan teknolojiler: Python, Gemini API, MusicGen, Gradio



\## Kurulum



1\. Repoyu klonla:

git clone https://github.com/cagriarsln/emotion-to-music.git



2\. Kütüphaneleri yükle:

pip install transformers scipy torch google-generativeai gradio python-dotenv



3\. Gemini API anahtarı al:

\- https://aistudio.google.com adresine git

\- "Get API Key" butonuna tıkla

\- Ücretsiz anahtar oluştur



4\. Klasörde .env dosyası oluştur, içine şunu yaz:

GEMINI\_API\_KEY=senin\_anahtarın



5\. Çalıştır:

python main.py

