import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.slider import Slider
from kivy.properties import StringProperty, NumericProperty, ListProperty
import os

# Removido o uso de SQLite e banco de dados


class EtiquetaForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text='Nome do Produto:'))
        self.nome_input = TextInput(multiline=False)
        self.add_widget(self.nome_input)

        self.add_widget(Label(text='Descrição:'))
        self.desc_input = TextInput(multiline=True)
        self.add_widget(self.desc_input)

        self.add_widget(Label(text='Preço:'))
        self.preco_input = TextInput(multiline=False, input_filter='float')
        self.add_widget(self.preco_input)

        self.add_widget(Label(text='Fonte:'))
        self.fonte_spinner = Spinner(
            text='Arial', values=['Arial', 'Verdana', 'Courier', 'Times'])
        self.add_widget(self.fonte_spinner)

        self.add_widget(Label(text='Tamanho da Fonte:'))
        self.tamanho_slider = Slider(min=8, max=48, value=12, step=1)
        self.add_widget(self.tamanho_slider)

        self.add_widget(Label(text='Cor:'))
        self.cor_picker = ColorPicker()
        self.add_widget(self.cor_picker)

        self.add_widget(Label(text='Protocolo de Impressão:'))
        self.protocolo_spinner = Spinner(
            text='RAW', values=['RAW', 'ZPL', 'EPL'])
        self.add_widget(self.protocolo_spinner)

        self.btn_salvar = Button(text='Salvar Etiqueta')
        self.btn_salvar.bind(on_press=self.salvar_etiqueta)
        self.add_widget(self.btn_salvar)

        self.btn_imprimir = Button(text='Imprimir Etiqueta')
        self.btn_imprimir.bind(on_press=self.imprimir_etiqueta)
        self.add_widget(self.btn_imprimir)

    def salvar_etiqueta(self, instance):
        # Apenas exibe popup, não salva mais no banco
        popup = Popup(title='Info', content=Label(
            text='Função de salvar desabilitada (sem banco de dados).'), size_hint=(0.5, 0.5))
        popup.open()

    def imprimir_etiqueta(self, instance):
        protocolo = self.protocolo_spinner.text
        nome = self.nome_input.text
        desc = self.desc_input.text
        preco = self.preco_input.text
        fonte = self.fonte_spinner.text
        tamanho = int(self.tamanho_slider.value)
        cor = self.cor_picker.color
        if protocolo == 'RAW':
            comando = f"RAW: {nome} - {desc} - R${preco}"
        elif protocolo == 'ZPL':
            comando = f"^XA^FO50,50^A0N,{tamanho},{tamanho}^FD{nome} - {desc} - R${preco}^FS^XZ"
        elif protocolo == 'EPL':
            comando = f'N\nA50,50,0,4,{tamanho},{tamanho},N,"{nome} - {desc} - R${preco}"\nP1\n'
        else:
            comando = 'Protocolo não suportado.'
        popup = Popup(title='Comando de Impressão', content=Label(
            text=comando), size_hint=(0.8, 0.5))
        popup.open()


class EtiquetaApp(App):
    def build(self):
        return EtiquetaForm()


if __name__ == '__main__':
    EtiquetaApp().run()
