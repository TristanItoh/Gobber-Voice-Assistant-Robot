from google import genai
from elevenlabs import ElevenLabs
import whisper
import time
import random
from pydub.utils import mediainfo

# === ElevenLabs Setup ===
tts_client = ElevenLabs(api_key="sk_60694c8c75fa90f0c697c124d0f4d5446b689b4d31aa3b58")

# === Gemini Function ===
def ask_gemini(prompt: str) -> str:
    client = genai.Client(api_key="AIzaSyCP67kbJyehaJrCnv99X0RlJQ3SR6HsPhk")
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

def play_idle_animations():
    idle_actions = ["smile", "look", "blink"]
    action = random.choice(idle_actions)
    print(f"🎭 Face: {action}")
    time.sleep(random.uniform(0.5, 2))  # simulate idle timing

def play_talking_animation(duration_sec):
    print("🎭 Face: open mouth")  # Open mouth once before talking
    end_time = time.time() + duration_sec
    while time.time() < end_time:
        print("🎭 Face: talk")    # Repeat talk animation
        time.sleep(0.15)
    print("🎭 Face: close mouth") # Close mouth once after talking
    print("🎭 Face: neutral")


# === Idle Animation Simulation ===
print("🤖 Bot is idle...")
for _ in range(3):
    play_idle_animations()

print("🔊 Loading MP3 for transcription...")


# === Whisper Speech-to-Text ===
print("🔊 Loading MP3 for transcription...")
model = whisper.load_model("base")
result = model.transcribe("prompt.mp3")

print("Whisper result:", result)  # Debug output

raw_text = result.get("text", "")
if isinstance(raw_text, list):
    input_text = " ".join(str(x) for x in raw_text)
elif isinstance(raw_text, str):
    input_text = raw_text.strip()
else:
    input_text = "Sorry, I didn't hear anything."

print(f"🧠 You said: {input_text}")

# === Append Prompt Style ===
default_prompt = (
    " You are an ai chatbot designed to assist in tasks. "
    "Keep your responses short and concise. "
    "You are a pirate named Captain Willy, so try to talk like a pirate. "
    "Strip your responses to not include any special characters such as asterisks."
)
full_prompt = input_text + default_prompt

# === Ask Gemini ===
print("🤖 Thinking...")
ai_response = ask_gemini(full_prompt)
print(f"🤖 Bot says: {ai_response}")

# === Animation Placeholder ===
print("🎭 Face: talking")
print("🎭 Face: neutral")

# === TTS with ElevenLabs ===
audio = tts_client.text_to_speech.convert(
    text=ai_response,
    voice_id="2rwOA0PJmS0KagZBMbZF",
    model_id="eleven_monolingual_v1"
)

# === Save MP3 Output ===
with open("response.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
print("🔊 MP3 saved as response.mp3")

# === Get Duration and Animate During Speech ===
info = mediainfo("response.mp3")
duration = float(info['duration'])

play_talking_animation(duration)

