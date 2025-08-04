import os
import re
import serial
from pydub.utils import mediainfo
from google import genai
from elevenlabs import ElevenLabs
import whisper
import time
import random
import socket
from pydub import AudioSegment
from gtts import gTTS

ELEVENLABS_API_KEY = "sk_60694c8c75fa90f0c697c124d0f4d5446b689b4d31aa3b58"
GOOGLE_API_KEY = "AIzaSyCP67kbJyehaJrCnv99X0RlJQ3SR6HsPhk"

TEST_MODE = True  # ← Set to False for normal behavior

# === ElevenLabs Setup ===
tts_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# === Gemini Function ===
def ask_gemini(prompt: str) -> str:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    if response and hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if candidate and hasattr(candidate, 'content') and candidate.content:
            content = candidate.content
            if hasattr(content, 'parts') and content.parts:
                part = content.parts[0]
                if part and hasattr(part, 'text') and part.text:
                    return part.text.strip()
    elif response and hasattr(response, 'text') and response.text:
        return response.text.strip()
    return "Sorry, I couldn't generate a response."

# === Text Cleaning Function ===
def clean_text(text: str) -> str:
    pattern = r"[^a-zA-Z0-9\s.,'\"?!-]"
    return re.sub(pattern, "", text)

def play_idle_animations():
    idle_actions = ["smile", "look", "blink"]
    action = random.choice(idle_actions)
    print(f"🎭 Face: {action}")
    time.sleep(random.uniform(0.5, 2))

def play_talking_animation(duration_sec):
    print("🎭 Face: open mouth")
    end_time = time.time() + duration_sec
    while time.time() < end_time:
        print("🎭 Face: talk")
        time.sleep(0.15)
    print("🎭 Face: close mouth")
    print("🎭 Face: neutral")

def tts_fallback(text: str, filename="response_fallback.mp3"):
    print("⚠️ Falling back to gTTS free TTS service...")
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

# === Main ===
if TEST_MODE:
    print("🧪 TEST MODE ENABLED: Skipping generation, using existing response.wav")
    wav_audio = AudioSegment.from_file("response.wav", format="wav")
    louder_audio = wav_audio + 10
    louder_audio.export("response.wav", format="wav")
    info = mediainfo("response.wav")
    duration = float(info['duration'])
else:
    print("🤖 Bot is idle...")
    for _ in range(3):
        play_idle_animations()

    print("🔊 Loading MP3 for transcription...")
    model = whisper.load_model("base")
    result = model.transcribe("promptskib.mp3")
    print("Whisper result:", result)

    raw_text = result.get("text", "")
    if isinstance(raw_text, list):
        input_text = " ".join(str(x) for x in raw_text)
    elif isinstance(raw_text, str):
        input_text = raw_text.strip()
    else:
        input_text = "Sorry, I didn't hear anything."

    print(f"🧠 You said: {input_text}")

    default_prompt = (
        "You are a helpful AI assistant named Captain Willy. "
        "You speak like a pirate from the high seas, using pirate slang and sea-faring expressions. "
        "Keep your answers short and focused, but every so often, ramble mid-sentence about something irrelevant like lost treasure, parrots, or your peg leg — just for a moment. "
        "Occasionally refer to yourself by your full name, even if it makes no sense. "
        "Avoid using special characters like asterisks or emojis. Plain text only. "
        "Stay in character no matter what, even if the question is serious. Be funny, not formal."
    )
    full_prompt = input_text + default_prompt

    print("🤖 Thinking...")
    ai_response = ask_gemini(full_prompt)

    cleaned_response = clean_text(ai_response)
    print(f"🤖 Bot says: {cleaned_response}")

    try:
        audio = tts_client.text_to_speech.convert(
            text=cleaned_response,
            voice_id="2rwOA0PJmS0KagZBMbZF",
            model_id="eleven_monolingual_v1"
        )
        with open("response.mp3", "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print("🔊 MP3 saved as response.mp3")
    except Exception as e:
        print(f"⚠️ ElevenLabs TTS failed: {e}")
        tts_fallback(cleaned_response, filename="response.mp3")

    mp3_audio = AudioSegment.from_file("response.mp3", format="mp3")
    louder_audio = mp3_audio + 0
    wav_audio = louder_audio.set_channels(1).set_sample_width(2).set_frame_rate(22050)
    wav_audio.export("response.wav", format="wav")
    print("🔊 WAV saved as response.wav (louder, ready for ESP32 playback)")

    info = mediainfo("response.wav")
    duration = float(info['duration'])


# play_talking_animation(duration)

def send_wav_over_wifi(ip, port, wav_path="response.wav"):
    print(f"📡 Connecting to ESP32 at {ip}:{port}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            print("✅ Connected to ESP32!")

            with open(wav_path, "rb") as f:
                while True:
                    chunk = f.read(1024)  # send 1024 bytes per chunk
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    # Optional tiny delay to avoid flooding
                    # time.sleep(0.001)
            print("✅ Finished sending WAV file over Wi-Fi.")
    except Exception as e:
        print(f"❌ Error sending WAV over Wi-Fi: {e}")

ESP32_IP = "192.168.1.47"   # <-- Replace with your ESP32's IP address from Serial Monitor
ESP32_PORT = 12345         # <-- This matches the port in your ESP32 sketch

send_wav_over_wifi(ESP32_IP, ESP32_PORT, "response.wav")
