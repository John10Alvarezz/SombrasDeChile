from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase


class NavBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(80)  # Aumentado de 65 a 80
        self.screen_manager = None
        self.spacing = 0
        self.padding = [0, 0, 0, 0]

        with self.canvas.before:
            Color(0.1, 0.1, 0.14, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.create_nav_buttons()

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def create_nav_buttons(self):
        buttons = [
            ('[color=#FFD700]🏠[/color]\nInicio', 'feed'),
            ('[color=#FFD700]🔍[/color]\nBuscar', 'search'),
            ('[color=#FFD700]+[/color]\nCrear', 'create'),
            ('[color=#FFD700]👤[/color]\nPerfil', 'profile')
        ]

        for text, screen_name in buttons:
            btn = Button(
                text=text,
                background_color=(0, 0, 0, 0),
                background_normal='',
                color=(0.7, 0.7, 0.7, 1),
                font_size=sp(16),  # Aumentado de 11 a 16
                halign='center',
                valign='middle',
                markup=True,
                font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
            )
            btn.bind(on_press=lambda x, s=screen_name: self.change_screen(s))
            self.add_widget(btn)

    def set_screen_manager(self, screen_manager):
        self.screen_manager = screen_manager

    def change_screen(self, screen_name):
        if self.screen_manager:
            try:
                self.screen_manager.current = screen_name
                print(f"Cambiando a pantalla: {screen_name}")
            except Exception as e:
                print(f"Error cambiando a pantalla {screen_name}: {e}")
        else:
            print(f"Screen manager no disponible para cambiar a {screen_name}")


