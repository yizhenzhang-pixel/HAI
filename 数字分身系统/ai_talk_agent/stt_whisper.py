import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import tempfile

def record_audio(duration=5, fs=16000):
    print("🎙️ 正在录音... 请开始讲话")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("✅ 录音结束，识别中...")
    return audio, fs

def transcribe_audio(audio, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        write(f.name, fs, audio)
        model = whisper.load_model("tiny")
        result = model.transcribe(f.name, language="zh")
        return result["text"]