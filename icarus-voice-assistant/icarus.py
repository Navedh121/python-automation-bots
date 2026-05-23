import os
import asyncio
import tempfile
import threading
import webbrowser
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import edge_tts
from playsound import playsound
from flask import Flask, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = Flask(__name__)

SAMPLE_RATE = 44100
conversation_history = []

VOICE = "en-US-AndrewNeural"

SYSTEM_PROMPT = """
You are Icarus, a brilliant AI assistant inspired by Jarvis from Iron Man.
You speak in a calm, composed, slightly formal British tone.
You are sharp, helpful, and occasionally witty.
Keep every response to 2-3 sentences maximum — be concise.
You are talking to Naved, a 2nd year electronics engineering student from Kerala, India.
"""

async def _speak_async(text):
    temp_file = tempfile.mktemp(suffix=".mp3")
    communicate = edge_tts.Communicate(text, VOICE, rate="+5%", volume="+10%")
    await communicate.save(temp_file)
    return temp_file

def speak(text):
    print(f"🤖 Icarus: {text}")
    temp_file = asyncio.run(_speak_async(text))
    try:
        playsound(temp_file)
    except Exception as e:
        print(f"Audio playback error: {e}")
    finally:
        try:
            os.remove(temp_file)
        except Exception:
            pass

recording = False
recorded_chunks = []
stream = None
stream_lock = threading.Lock()

@app.route("/")
def index():
    return send_from_directory(".", "icarus.html")

@app.route("/start", methods=["POST"])
def start_recording():
    global recording, recorded_chunks, stream

    with stream_lock:
        if stream is not None:
            try:
                stream.stop()
                stream.close()
            except Exception:
                pass
            stream = None

        recorded_chunks = []
        recording = True

        def callback(indata, frames, time, status):
            if recording:
                recorded_chunks.append(indata.copy())

        stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            callback=callback,
            blocksize=4096
        )
        stream.start()

    print("🎤 Recording started...")
    return jsonify({"status": "recording"})

@app.route("/stop", methods=["POST"])
def stop_recording():
    global recording, stream, recorded_chunks

    with stream_lock:
        recording = False
        if stream is not None:
            try:
                stream.stop()
                stream.close()
            except Exception:
                pass
            stream = None

    print("⏹️  Recording stopped.")

    if not recorded_chunks:
        return jsonify({"error": "No audio recorded"}), 400

    audio_data = np.concatenate(recorded_chunks, axis=0)
    recorded_chunks = []

    temp_file = tempfile.mktemp(suffix=".wav")
    wav.write(temp_file, SAMPLE_RATE, audio_data)

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 200
    recognizer.pause_threshold = 0.8

    try:
        with sr.AudioFile(temp_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.record(source)
        user_text = recognizer.recognize_google(audio)
        print(f"👤 You said: {user_text}")
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand. Please speak clearly and try again."}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech service error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(temp_file)
        except Exception:
            pass

    if any(w in user_text.lower() for w in ["exit", "quit", "goodbye", "shut down", "power off"]):
        reply = "Goodbye, Naved. Icarus signing off. It has been a pleasure."
        threading.Thread(target=speak, args=(reply,), daemon=True).start()
        return jsonify({"user": user_text, "icarus": reply, "exit": True})

    conversation_history.append({"role": "user", "content": user_text})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            max_tokens=150,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        print(f"✅ Groq reply: {reply}")
    except Exception as e:
        print(f"❌ GROQ ERROR: {type(e).__name__}: {e}")
        conversation_history.pop()
        return jsonify({"error": f"AI error: {str(e)}"}), 500

    conversation_history.append({"role": "assistant", "content": reply})
    threading.Thread(target=speak, args=(reply,), daemon=True).start()

    return jsonify({"user": user_text, "icarus": reply})

@app.route("/greet", methods=["POST"])
def greet():
    msg = "Icarus online. All systems nominal. How may I assist you, Naved?"
    threading.Thread(target=speak, args=(msg,), daemon=True).start()
    return jsonify({"icarus": msg})

def open_browser():
    import time
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 45)
    print("         ICARUS — AI ASSISTANT v1.0")
    print("=" * 45)
    print("🚀 Starting server...")
    print("🌐 Browser will open automatically.")
    print("=" * 45)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(debug=False, port=5000)