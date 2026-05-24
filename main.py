import os
import time
import google.generativeai as genai
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model_gemini = genai.GenerativeModel("gemini-2.5-flash")
model_music = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")

def analyze_emotion(text):
    prompt = f"""
    You are a music prompt engineer. Analyze the emotional content of the following text and generate a detailed MusicGen prompt.

    Rules:
    - Be specific: include tempo (slow/medium/fast), key (minor/major), instruments, mood descriptors
    - Good example: "melancholic piano, slow tempo, minor key, soft strings, rain ambiance, lonely and introspective"
    - Bad example: "ambient background music"
    - Only output the music prompt, nothing else, no explanation

    
    Text to analyze: {text}
    """
    
    # 2. Kota aşıldığında programın çökmemesi için Try-Except bloğu
    try:
        response = model_gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
     if "429" in str(e) or "ResourceExhausted" in str(e):
        print("Limit aşıldı, 35 saniye bekleniyor...")
        time.sleep(35)
        return analyze_emotion(text)
     print(f"HATA: {e}")
     return "ambient background music"

def generate_music(text):
    music_prompt = analyze_emotion(text)
    print(f"Müzik promptu: {music_prompt}")
    
    inputs = processor(
        text=[music_prompt],
        padding=True,
        return_tensors="pt",
    )
    
    audio_values = model_music.generate(**inputs, max_new_tokens=1024)
    zaman_damgasi = time.strftime("%Y%m%d_%H%M%S")
    output_path = f"output_{zaman_damgasi}.wav"
    scipy.io.wavfile.write(output_path, rate=64000, data=audio_values[0, 0].numpy())
    return output_path, music_prompt

# Test
if __name__ == "__main__":
    def arayuz(metin):
        path, prompt = generate_music(metin)
        return path, prompt

    gr.Interface(
    fn=arayuz,
    inputs=gr.Textbox(label="Duygunu yaz"),
    outputs=[gr.Audio(label="Müzik"), gr.Textbox(label="Müzik promptu")]
    ).launch()