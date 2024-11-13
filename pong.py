from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class Tablita(GridLayout):
    def __init__(self, **kwargs):
        super(Tablita, self).__init__(**kwargs)
        self.cols = 2
        
        # Crear campos de entrada para nombre, apellido y comida
        self.add_widget(Label(text="Nombre:"))
        self.nombre = TextInput(multiline=False)
        self.add_widget(self.nombre)

        self.add_widget(Label(text="Apellido:"))
        self.apellido = TextInput(multiline=False)
        self.add_widget(self.apellido)

        self.add_widget(Label(text="Comida favorita:"))
        self.comida = TextInput(multiline=False)
        self.add_widget(self.comida)
        
        # Botón para procesar
        self.boton = Button(text="Enviar")
        self.boton.bind(on_press=self.press)
        self.add_widget(self.boton)
        
        # Etiqueta para mostrar el resultado
        self.resultado = Label(text="")
        self.add_widget(self.resultado)

    def press(self, instance):
        name = self.nombre.text
        last_name = self.apellido.text
        food = self.comida.text
        
        if name and last_name and food:
            mensaje = f"Hola {name} {last_name}, tu comida favorita es {food}"
            self.resultado.text = mensaje
            print(mensaje)
        
        # Limpiar los campos de entrada
        self.nombre.text = ""
        self.apellido.text = ""
        self.comida.text = ""

class PongApp(App):
    def build(self):
        return Tablita()

if __name__ == "__main__":
    PongApp().run()


