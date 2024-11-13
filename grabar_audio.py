import pyaudio
import wave
import json
import numpy as np
from vosk import Model, KaldiRecognizer

# Parámetros de grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 500  # Ajusta este valor según pruebas
MAX_SILENCE_BLOCKS = 30  # Número de bloques consecutivos de silencio antes de detener

audio = pyaudio.PyAudio()

# Ruta al modelo de Vosk (asegúrate de que sea la correcta)
MODEL_PATH = "vosk-model-small-es-0.42"
model = Model(MODEL_PATH)

def record_prompt(filename):
    """Graba audio y lo guarda en un archivo, deteniéndose si hay silencio prolongado."""
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Grabando...")

    frames = []
    silence_blocks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Convertir a array de numpy para procesar el volumen
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()

        # Comprobar si el volumen está bajo el umbral
        if volume < SILENCE_THRESHOLD:
            silence_blocks += 1
            if silence_blocks >= MAX_SILENCE_BLOCKS:
                print("Silencio detectado, deteniendo la grabación.")
                break
        else:
            silence_blocks = 0  # Reinicia el contador si no hay silencio

    stream.stop_stream()
    stream.close()

    # Guardar la grabación en un archivo WAV
    wavefile = wave.open(filename, 'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setframerate(RATE)
    wavefile.setsampwidth(audio.get_sample_size(FORMAT))
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    print(f"Audio grabado y guardado como: {filename}")

def transcribe_audio(filename):
    """Transcribe un archivo de audio usando Vosk."""
    wf = wave.open(filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 44100:
        print("El archivo de audio debe ser en mono y 44.1 kHz")
        return

    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    print("Transcribiendo...")

    while True:
        data = wf.readframes(CHUNK)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print("Transcripción parcial:", json.loads(result).get('text'))

    # Resultado final de la transcripción
    final_result = json.loads(recognizer.FinalResult()).get('text')
    print("\nTranscripción completa:", final_result)
    wf.close()

# Ejecución del programa
nombre_archivo = input("Introduce el nombre del archivo (sin extensión): ")
nombre_archivo += ".wav"

# Grabar audio
record_prompt(nombre_archivo)

# Transcribir el audio grabado
transcribe_audio(nombre_archivo)
            