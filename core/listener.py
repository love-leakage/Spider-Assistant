# core/listener.py
import json
from vosk import Model, KaldiRecognizer
import pyaudio

MODEL_PATH = 'models/vosk-model-small-en-us'


def start_listener():
    print('[Spider] Loading Vosk model...')
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print('[Spider] Listening... Say "hey spider" to trigger')

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            j = json.loads(rec.Result())
            text = j.get('text','')
            if text:
                print('[ASR]', text)
                # simple hotword check
                if 'hey spider' in text.lower():
                    # here call processor to take action
                    from core.processor import handle_command
                    handle_command(text)