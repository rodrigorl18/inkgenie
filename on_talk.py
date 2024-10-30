import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen(word):

    with microphone as source:
        print("Todo funciona, iniciando a inkgenie...")
        while True:
            try:
                audio_data = recognizer.listen(source,timeout=10,phrase_time_limit=10)
                text = recognizer.recognize_google(audio_data)
                print(f"Heard: {text.lower()}")
                if word in text.lower():
                    return True
                else:
                    return False
            except sr.WaitTimeoutError:
                print("Se acabo el tiempo, intente de nuevo")
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print(f"Error con el sitema de reconocimiento")

listen()
