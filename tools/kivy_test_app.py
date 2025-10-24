from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

Window.clearcolor = (1, 0, 0, 1)  # fondo rojo
Window.size = (400, 300)

class TestWidget(Widget):
    pass

class TestApp(App):
    def build(self):
        return TestWidget()

if __name__ == '__main__':
    TestApp().run()
