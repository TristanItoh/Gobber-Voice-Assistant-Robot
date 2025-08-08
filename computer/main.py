import socket
import time
import numpy as np
import pvporcupine
import whisper
from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import re
import google.generativeai as genai
from gtts import gTTS
import random

# === Configuration ===
# --- Network ---
ESP32_IP = "192.168.1.47"  # <-- IMPORTANT: Set to your ESP32's IP address
PORT = 12345

# --- Audio ---
SAMPLE_RATE = 16000  # Porcupine's required sample rate
CHANNELS = 1
BYTES_PER_SAMPLE_I2S = 4 # 32-bit audio from I2S mic
BYTES_PER_SAMPLE_PCM = 2 # 16-bit audio for Porcupine/Whisper

# --- API Keys ---
PORCUPINE_ACCESS_KEY = "oops im not leaking that" # Replace with your key
# ELEVENLABS_API_KEY = "oops im not leaking that" # Not needed for gTTS
GOOGLE_API_KEY = "oops im not leaking that"      # Replace with your key

# --- File Paths ---
WAKE_WORD_PATH = "Hey-Gobber.ppn"
PROMPT_WAV_PATH = "prompt.wav"
RESPONSE_WAV_PATH = "response.wav"

# === Initialization ===
# --- Porcupine Wake Word Engine ---
try:
    porcupine = pvporcupine.create(
        access_key=PORCUPINE_ACCESS_KEY,
        keyword_paths=[WAKE_WORD_PATH]
    )
    BUFFER_SIZE_PORCUPINE_FRAME = porcupine.frame_length * BYTES_PER_SAMPLE_I2S
    print("✅ Porcupine wake word engine initialized.")
except Exception as e:
    print(f"❌ Error initializing Porcupine: {e}")
    porcupine = None

# --- Whisper Speech-to-Text ---
try:
    whisper_model = whisper.load_model("base")
    print("✅ Whisper model loaded.")
except Exception as e:
    print(f"❌ Error loading Whisper model: {e}")
    whisper_model = None


# --- Gemini AI ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("✅ Gemini client initialized.")
except Exception as e:
    print(f"❌ Error initializing Gemini client: {e}")
    gemini_model = None


# === Core Functions ===

def convert_i2s_to_pcm(raw_data):
    """Converts 32-bit I2S audio data (bytes) to a 16-bit PCM numpy array."""
    int32_data = np.frombuffer(raw_data, dtype=np.int32)
    int16_data = (int32_data >> 14).astype(np.int16)
    return int16_data

def save_pcm_to_wav(pcm_data, filename, sample_rate, channels):
    """Saves a 16-bit PCM numpy array to a WAV file."""
    audio = AudioSegment(
        pcm_data.tobytes(),
        frame_rate=sample_rate,
        sample_width=BYTES_PER_SAMPLE_PCM,
        channels=channels
    )
    audio.export(filename, format="wav")
    print(f"✅ Audio saved to {filename}")

def ask_gemini(prompt: str) -> str:
    """Sends a prompt to Gemini and returns the text response."""
    if not gemini_model:
        return "Sorry, the AI model is not available."
    try:
        print("🤖 Thinking...")
        # Your custom pirate prompt
        pirate_prompt = (
            
            f"Keep your answers short and focused. "
            f"Here is the user's question: {prompt}"
        )
        response = gemini_model.generate_content(pirate_prompt)
        ai_response = response.text.strip()
        print(f"🤖 Bot says: {ai_response}")
        return ai_response
    except Exception as e:
        print(f"❌ Error with Gemini: {e}")
        return "Sorry, I be havin' trouble thinkin' right now."

def generate_tts(text: str, output_path: str):
    """Generates audio from text using gTTS and saves it as a WAV file."""
    try:
        print("🔊 Generating speech with gTTS...")
        tts = gTTS(text=text, lang='en')
        # Save to a temporary mp3 file
        tts.save("response.mp3")

        # Convert MP3 to WAV for the ESP32
        mp3_audio = AudioSegment.from_file("response.mp3", format="mp3")
        wav_audio = mp3_audio.set_channels(1).set_sample_width(2).set_frame_rate(22050) # ESP speaker likes 22050Hz
        wav_audio.export(output_path, format="wav")

        print(f"✅ Speech audio saved to {output_path}")

    except Exception as e:
        print(f"❌ Error generating TTS with gTTS: {e}")


def send_audio_to_esp32(sock, wav_path):
    """Sends a command and then a WAV file to the ESP32 over the given socket."""
    try:
        # 1. Send the command to switch to PLAY mode
        print(" commanding ESP32 to play audio...")
        sock.sendall(b"PLAY\n")
        time.sleep(0.1) # Give ESP32 a moment to switch modes

        # 2. Send the WAV file
        print(f"📡 Streaming {wav_path} to ESP32...")
        with open(wav_path, "rb") as f:
            # Larger chunks reduce syscalls and pacing gaps
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                sock.sendall(chunk)
        print("✅ Finished sending audio.")
    except Exception as e:
        print(f"❌ Error sending audio to ESP32: {e}")

# === Main Application Loop ===

def main_loop():
    """The main loop that connects, listens, and interacts."""
    while True:
        audio_buffer = bytearray()
        try:
            # --- 1. Connect to ESP32 ---
            print(f"📡 Trying to connect to ESP32 at {ESP32_IP}:{PORT}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Reduce Nagle-induced delays
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.connect((ESP32_IP, PORT))
                print("✅ Connected to ESP32! Listening for wake word...")

                # --- 2. Listen for Wake Word ---
                wake_word_detected = False
                while not wake_word_detected:
                    data = s.recv(1024)
                    if not data:
                        print("Connection lost.")
                        break
                    audio_buffer += data

                    while len(audio_buffer) >= BUFFER_SIZE_PORCUPINE_FRAME:
                        frame_data = audio_buffer[:BUFFER_SIZE_PORCUPINE_FRAME]
                        audio_buffer = audio_buffer[BUFFER_SIZE_PORCUPINE_FRAME:]
                        
                        pcm_frame = convert_i2s_to_pcm(frame_data)
                        
                        if porcupine and porcupine.process(pcm_frame) >= 0:
                            print("🟢 Wake word detected!")
                            wake_word_detected = True
                            break
                
                if not wake_word_detected:
                    continue # Loop back to reconnect if connection was lost

                # --- 3. Record Prompt ---
                print("🎤 Recording prompt for 5 seconds...")
                prompt_audio_data = bytearray()
                start_time = time.time()
                while time.time() - start_time < 5.0:
                    # Keep draining the socket
                    chunk = s.recv(2048)
                    if not chunk:
                        break
                    prompt_audio_data += chunk
                
                print("✅ Finished recording prompt.")
                full_pcm_data = convert_i2s_to_pcm(prompt_audio_data)
                save_pcm_to_wav(full_pcm_data, PROMPT_WAV_PATH, SAMPLE_RATE, CHANNELS)

                # --- 4. Process and Respond ---
                if whisper_model:
                    result = whisper_model.transcribe(PROMPT_WAV_PATH)
                    user_prompt = result.get("text", "").strip()
                    print(f"💬 You said: {user_prompt}")

                    if user_prompt:
                        ai_response = ask_gemini(user_prompt)
                        generate_tts(ai_response, RESPONSE_WAV_PATH)
                        
                        # --- 5. Send Audio for Playback ---
                        if os.path.exists(RESPONSE_WAV_PATH):
                            send_audio_to_esp32(s, RESPONSE_WAV_PATH)
                    else:
                        print("No clear prompt detected.")

            # The 'with socket' block closes the connection here, signaling the ESP32
            # to reset to listening mode.

        except (ConnectionRefusedError, TimeoutError):
            print(f"Connection to {ESP32_IP} failed. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Restarting loop in 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    if not all([porcupine, whisper_model, gemini_model]):
        print(" A critical component failed to initialize. Please check API keys and configurations. Exiting.")
    else:
        try:
            main_loop()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down.")
        finally:
            if porcupine:
                porcupine.delete()
