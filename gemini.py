import os
import google.generativeai as genai

# Ajustando gemini para autenticar 
API_KEY = "AIzaSyAAHYK0uNyFD13ecy-glUbhI8kUR85CpVU"
genai.configure(api_key=API_KEY)

# Creando la instancia de que contendrá nuestro modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicializar una lista para recordar las consultas anteriores
historial = []

# Función para generar contenido con memoria
def generar_con_memoria(consulta, historial):
    contexto = " ".join(historial) + " " + consulta
    result = model.generate_content(contexto)
    return result


model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = model.start_chat(
    history=[]
)


while True:
    consulta = input("Ingrese su pregunta a Gemini (o 'salir' para finalizar): ")
    result = chat_session.send_message(consulta)
    
    # Condición para salir del ciclo
    if consulta.lower() == 'salir':
        print("Saliendo del programa.")
        break
    
    # Agregar la consulta actual al historial
    historial.append(consulta)
    
    # Generar la respuesta basada en el historial
    result = generar_con_memoria(consulta, historial)
    
    # Mostrar la respuesta generada
    print(result.text)

    # Agregar la respuesta generada al historial para que también sea parte del contexto
    historial.append(result.text)

