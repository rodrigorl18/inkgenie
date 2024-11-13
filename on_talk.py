import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen(word="inkgenie"):
    print("Iniciando Inkgenie...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Escuchando...")
        while True:
            try:
                audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                text = recognizer.recognize_google(audio_data)
                print(f"Escuchado: {text.lower()}")

                if word in text.lower():
                    print("Palabra clave detectada. Ejecutando acción...")
                    return True
                elif "salir" in text.lower():
                    print("Saliendo...")
                    break
            except sr.WaitTimeoutError:
                print("Se acabó el tiempo, intente de nuevo")
            except sr.UnknownValueError:
                print("No se entendió el audio, intente de nuevo")
            except sr.RequestError:
                print("Error con el sistema de reconocimiento de voz")
    return False

if __name__ == "__main__":
    listen()
