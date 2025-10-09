# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.metrics import dp, sp
from database import Database
import os

Window.clearcolor = (0.08, 0.08, 0.12, 1)
Window.size = (400, 700)

# Configurar la fuente para mejor soporte de emojis
from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel
from kivy.core.text import DEFAULT_FONT

# Configurar fuente para mejor soporte de emojis
def configure_font():
    """Configura la fuente para mejor soporte de emojis"""
    try:
        # Configurar fuente por defecto
        from kivy.core.text import DEFAULT_FONT
        print(f"Fuente por defecto: {DEFAULT_FONT}")
        
        # Configurar el proveedor de texto para mejor soporte de emojis
        from kivy.core.text import Label as CoreLabel
        print("Configuración de fuente completada")
        
    except Exception as e:
        print(f"Error configurando fuente: {e}")

# Configurar la fuente al inicio
configure_font()

class NavBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(65)
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
            ('[color=#FFD700]⌂[/color]\nInicio', 'feed'),
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
                font_size=sp(11),
                halign='center',
                valign='middle',
                markup=True
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

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)

        layout.bind(pos=self.update_bg, size=self.update_bg)

        content = BoxLayout(
            orientation='vertical',
            size_hint=(0.85, None),
            height=dp(450),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=dp(20),
            padding=[dp(20), dp(20)]
        )

        title = Label(
            text='[color=#9966CC]●[/color]',
            font_size=sp(80),
            color=(0.6, 0.3, 0.7, 1),
            size_hint_y=None,
            height=dp(100),
            markup=True
        )

        app_title = Label(
            text='Historias Paranormales\nde Chile',
            font_size=sp(28),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='center',
            size_hint_y=None,
            height=dp(80)
        )
        app_title.bind(size=app_title.setter('text_size'))

        subtitle = Label(
            text='Comparte tus experiencias sobrenaturales',
            font_size=sp(15),
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        subtitle.bind(size=subtitle.setter('text_size'))

        btn_guest = Button(
            text='Continuar como Invitado',
            size_hint=(1, None),
            height=dp(55),
            background_normal='',
            background_color=(0.25, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16)
        )
        btn_guest.bind(on_press=self.go_to_feed)

        btn_login = Button(
            text='Iniciar Sesión',
            size_hint=(1, None),
            height=dp(55),
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            bold=True
        )
        btn_login.bind(on_press=self.go_to_login)

        content.add_widget(title)
        content.add_widget(app_title)
        content.add_widget(subtitle)
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))
        content.add_widget(btn_guest)
        content.add_widget(btn_login)

        layout.add_widget(content)
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def go_to_feed(self, instance):
        self.manager.get_screen('feed').is_guest = True
        self.manager.current = 'feed'

    def go_to_login(self, instance):
        self.manager.current = 'login'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)

        layout.bind(pos=self.update_bg, size=self.update_bg)

        form_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.85, None),
            height=dp(450),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=dp(15),
            padding=[dp(20), dp(20)]
        )

        title = Label(
            text='Iniciar Sesión',
            font_size=sp(32),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            size_hint_y=None,
            height=dp(60)
        )

        self.username_input = TextInput(
            hint_text='Nombre de usuario',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(15)
        )

        self.password_input = TextInput(
            hint_text='Contraseña',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(15)
        )

        btn_login = Button(
            text='Ingresar',
            size_hint_y=None,
            height=dp(55),
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            bold=True
        )
        btn_login.bind(on_press=self.login)

        btn_register = Button(
            text='Crear Cuenta',
            size_hint_y=None,
            height=dp(55),
            background_normal='',
            background_color=(0.25, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16)
        )
        btn_register.bind(on_press=self.go_to_register)

        btn_back = Button(
            text='← Volver',
            size_hint_y=None,
            height=dp(45),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(14)
        )
        btn_back.bind(on_press=self.go_back)

        form_layout.add_widget(title)
        form_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        form_layout.add_widget(btn_login)
        form_layout.add_widget(btn_register)
        form_layout.add_widget(btn_back)

        layout.add_widget(form_layout)
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.show_popup('Error', 'Por favor completa todos los campos')
            return

        user = self.db.login_user(username, password)
        if user:
            app = App.get_running_app()
            app.current_user = user
            self.manager.get_screen('feed').is_guest = False
            self.manager.current = 'feed'
            self.username_input.text = ''
            self.password_input.text = ''
        else:
            self.show_popup('Error', 'Usuario o contraseña incorrectos')

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_back(self, instance):
        self.manager.current = 'welcome'

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, color=(0.9, 0.9, 0.9, 1)))
        btn_close = Button(text='OK', size_hint_y=None, height=dp(40))

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3),
            background_color=(0.15, 0.15, 0.2, 1)
        )
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)
        popup.open()

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            self.bg = Rectangle(pos=layout.pos, size=layout.size)

        layout.bind(pos=self.update_bg, size=self.update_bg)

        scroll = ScrollView()
        form_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.85, None),
            height=dp(600),
            pos_hint={'center_x': 0.5},
            spacing=dp(15),
            padding=[dp(20), dp(40)]
        )

        title = Label(
            text='Crear Cuenta',
            font_size=sp(32),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            size_hint_y=None,
            height=dp(60)
        )

        self.username_input = TextInput(
            hint_text='Nombre de usuario',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(15)
        )

        self.email_input = TextInput(
            hint_text='Correo electrónico',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(15)
        )

        self.password_input = TextInput(
            hint_text='Contraseña',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(15)
        )

        self.confirm_password_input = TextInput(
            hint_text='Confirmar contraseña',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(15)
        )

        btn_register = Button(
            text='Registrarse',
            size_hint_y=None,
            height=dp(55),
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            bold=True
        )
        btn_register.bind(on_press=self.register)

        btn_back = Button(
            text='← Volver',
            size_hint_y=None,
            height=dp(45),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(14)
        )
        btn_back.bind(on_press=self.go_back)

        form_layout.add_widget(title)
        form_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.email_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(self.confirm_password_input)
        form_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        form_layout.add_widget(btn_register)
        form_layout.add_widget(btn_back)

        scroll.add_widget(form_layout)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def register(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        if not username or not email or not password:
            self.show_popup('Error', 'Por favor completa todos los campos')
            return

        if password != confirm_password:
            self.show_popup('Error', 'Las contraseñas no coinciden')
            return

        if len(password) < 6:
            self.show_popup('Error', 'La contraseña debe tener al menos 6 caracteres')
            return

        if self.db.create_user(username, email, password):
            self.show_popup('Éxito', 'Cuenta creada exitosamente')
            self.username_input.text = ''
            self.email_input.text = ''
            self.password_input.text = ''
            self.confirm_password_input.text = ''
            self.manager.current = 'login'
        else:
            self.show_popup('Error', 'El usuario o correo ya existe')

    def go_back(self, instance):
        self.manager.current = 'login'

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, color=(0.9, 0.9, 0.9, 1)))
        btn_close = Button(text='OK', size_hint_y=None, height=dp(40))

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3),
            background_color=(0.15, 0.15, 0.2, 1)
        )
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)
        popup.open()


class StoryCard(BoxLayout):
    def __init__(self, story, on_like=None, on_reaction=None, show_actions=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(240)
        self.spacing = dp(8)
        self.padding = [dp(12), dp(12)]
        self.story = story
        self.on_like = on_like
        self.on_reaction = on_reaction

        with self.canvas.before:
            Color(0.12, 0.12, 0.17, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        self.bind(pos=self.update_bg, size=self.update_bg)

        header = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(8))

        username_text = story.get('username', 'Anónimo') if not story.get('is_anonymous') else '[color=#FFD700]👤[/color] Anónimo'
        username = Label(
            text=username_text,
            font_size=sp(14),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_x=0.5,
            halign='left',
            valign='middle',
            markup=True
        )
        username.bind(size=username.setter('text_size'))

        category_color = self.get_category_color(story.get('category', 'Aparición'))
        category = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('category', 'Aparición')}",
            font_size=sp(11),
            color=category_color,
            size_hint_x=0.5,
            halign='right',
            valign='middle',
            markup=True
        )
        category.bind(size=category.setter('text_size'))

        header.add_widget(username)
        header.add_widget(category)

        location = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('location', 'Sin ubicación')}",
            font_size=sp(12),
            color=(0.6, 0.6, 0.7, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            valign='middle',
            markup=True
        )
        location.bind(size=location.setter('text_size'))

        content_text = story.get('content', '')
        if len(content_text) > 180:
            content_text = content_text[:180] + '...'

        content = Label(
            text=content_text,
            font_size=sp(13),
            color=(0.85, 0.85, 0.85, 1),
            size_hint_y=None,
            height=dp(90),
            text_size=(Window.width - dp(50), None),
            halign='left',
            valign='top'
        )

        if show_actions:
            actions = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))

            like_btn = Button(
                text=f"[color=#FFD700]●[/color] {story.get('likes', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.3, 0.2, 0.4, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True
            )
            if self.on_like:
                like_btn.bind(on_press=lambda x: self.on_like(story))

            miedo_btn = Button(
                text=f"[color=#FF6B6B]![/color] {story.get('miedo', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.35, 0.15, 0.25, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True
            )
            if self.on_reaction:
                miedo_btn.bind(on_press=lambda x: self.on_reaction(story, 'miedo'))

            sorpresa_btn = Button(
                text=f"[color=#4ECDC4]?[/color] {story.get('sorpresa', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.25, 0.25, 0.35, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True
            )
            if self.on_reaction:
                sorpresa_btn.bind(on_press=lambda x: self.on_reaction(story, 'sorpresa'))

            incredulidad_btn = Button(
                text=f"[color=#FFE66D]~[/color] {story.get('incredulidad', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.3, 0.3, 0.25, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True
            )
            if self.on_reaction:
                incredulidad_btn.bind(on_press=lambda x: self.on_reaction(story, 'incredulidad'))

            actions.add_widget(like_btn)
            actions.add_widget(miedo_btn)
            actions.add_widget(sorpresa_btn)
            actions.add_widget(incredulidad_btn)

            date = Label(
                text=story.get('created_at', ''),
                font_size=sp(10),
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(20),
                halign='right',
                valign='middle'
            )
            date.bind(size=date.setter('text_size'))

            self.add_widget(header)
            self.add_widget(location)
            self.add_widget(content)
            self.add_widget(actions)
            self.add_widget(date)
        else:
            self.add_widget(header)
            self.add_widget(location)
            self.add_widget(content)

    def get_category_color(self, category):
        colors = {
            'Aparición': (0.6, 0.4, 0.8, 1),
            'Fantasma': (0.5, 0.5, 0.7, 1),
            'OVNI': (0.4, 0.6, 0.8, 1),
            'Leyenda': (0.7, 0.5, 0.3, 1),
            'Psicofonía': (0.8, 0.4, 0.4, 1),
            'Criatura': (0.5, 0.7, 0.4, 1)
        }
        return colors.get(category, (0.6, 0.6, 0.6, 1))

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

class FeedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.is_guest = False

        layout = BoxLayout(orientation='vertical')

        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(65),
            padding=[dp(15), dp(10)]
        )

        with header.canvas.before:
            Color(0.1, 0.1, 0.14, 1)
            self.header_bg = Rectangle(pos=header.pos, size=header.size)

        header.bind(pos=self.update_header_bg, size=self.update_header_bg)

        title = Label(
            text='[color=#9966CC]●[/color] Historias',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            markup=True
        )
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)

        scroll = ScrollView()
        self.stories_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(12), dp(12)]
        )
        self.stories_layout.bind(minimum_height=self.stories_layout.setter('height'))

        scroll.add_widget(self.stories_layout)

        navbar = NavBar()

        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(navbar)

        self.add_widget(layout)

    def update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def on_enter(self):
        self.load_stories()

    def load_stories(self):
        self.stories_layout.clear_widgets()
        stories = self.db.get_all_stories()

        if not stories:
            no_stories = Label(
                text='No hay historias aún.\n¡Sé el primero en compartir!',
                font_size=sp(16),
                color=(0.6, 0.6, 0.6, 1),
                halign='center'
            )
            self.stories_layout.add_widget(no_stories)
        else:
            for story in stories:
                card = StoryCard(
                    story,
                    on_like=self.like_story if not self.is_guest else None,
                    on_reaction=self.add_reaction if not self.is_guest else None,
                    show_actions=not self.is_guest
                )
                self.stories_layout.add_widget(card)

    def like_story(self, story):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.add_like(story['id'], app.current_user['id'])
            self.load_stories()

    def add_reaction(self, story, tipo):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.add_reaction(story['id'], app.current_user['id'], tipo)
            self.load_stories()

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = BoxLayout(orientation='vertical')

        search_bar = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[dp(12), dp(10)],
            spacing=dp(8)
        )

        with search_bar.canvas.before:
            Color(0.1, 0.1, 0.14, 1)
            self.search_bg = Rectangle(pos=search_bar.pos, size=search_bar.size)

        search_bar.bind(pos=self.update_search_bg, size=self.update_search_bg)

        title = Label(
            text='[color=#FFD700]🔍[/color] Buscar Historias',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            size_hint_y=None,
            height=dp(40),
            halign='left',
            valign='middle',
            markup=True
        )
        title.bind(size=title.setter('text_size'))

        search_input_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        self.search_input = TextInput(
            hint_text='Buscar por contenido, ubicación o categoría...',
            multiline=False,
            size_hint_x=0.75,
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(14)
        )

        search_btn = Button(
            text='[color=#FFFFFF]🔍[/color]',
            size_hint_x=0.25,
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(20),
            markup=True
        )
        search_btn.bind(on_press=self.search_stories)

        search_input_box.add_widget(self.search_input)
        search_input_box.add_widget(search_btn)

        search_bar.add_widget(title)
        search_bar.add_widget(search_input_box)

        scroll = ScrollView()
        self.results_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(12), dp(12)]
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))

        scroll.add_widget(self.results_layout)

        navbar = NavBar()

        layout.add_widget(search_bar)
        layout.add_widget(scroll)
        layout.add_widget(navbar)

        self.add_widget(layout)

    def update_search_bg(self, instance, value):
        self.search_bg.pos = instance.pos
        self.search_bg.size = instance.size

    def search_stories(self, instance):
        query = self.search_input.text.strip()
        self.results_layout.clear_widgets()

        if not query:
            info = Label(
                text='Escribe algo para buscar',
                font_size=sp(14),
                color=(0.6, 0.6, 0.6, 1)
            )
            self.results_layout.add_widget(info)
            return

        stories = self.db.search_stories(query)

        if not stories:
            no_results = Label(
                text=f'No se encontraron historias para "{query}"',
                font_size=sp(14),
                color=(0.6, 0.6, 0.6, 1),
                halign='center'
            )
            no_results.bind(size=no_results.setter('text_size'))
            self.results_layout.add_widget(no_results)
        else:
            results_count = Label(
                text=f'Se encontraron {len(stories)} historias',
                font_size=sp(13),
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=dp(30)
            )
            self.results_layout.add_widget(results_count)

            for story in stories:
                card = StoryCard(story, show_actions=False)
                self.results_layout.add_widget(card)

class CreateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = BoxLayout(orientation='vertical')

        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(65),
            padding=[dp(15), dp(10)]
        )

        with header.canvas.before:
            Color(0.1, 0.1, 0.14, 1)
            self.header_bg = Rectangle(pos=header.pos, size=header.size)

        header.bind(pos=self.update_header_bg, size=self.update_header_bg)

        title = Label(
            text='[color=#FFD700]✍[/color] Crear Historia',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            markup=True
        )
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)

        scroll = ScrollView()
        form_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(12), dp(12)]
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))

        self.content_input = TextInput(
            hint_text='Cuéntanos tu historia paranormal...',
            multiline=True,
            size_hint_y=None,
            height=dp(220),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(14)
        )

        self.location_input = TextInput(
            hint_text='📍 Ubicación (ej: Valparaíso, Chile)',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(14)
        )

        category_label = Label(
            text='Categoría:',
            font_size=sp(14),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        )
        category_label.bind(size=category_label.setter('text_size'))

        self.category_spinner = Spinner(
            text='Aparición',
            values=('Aparición', 'Fantasma', 'OVNI', 'Leyenda', 'Psicofonía', 'Criatura'),
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(14)
        )

        options_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        self.anonymous_toggle = ToggleButton(
            text='[color=#FFD700]👤[/color] Modo Incógnito',
            size_hint_x=0.6,
            background_normal='',
            background_color=(0.25, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=sp(13),
            markup=True
        )

        photo_btn = Button(
            text='[color=#FFD700]📷[/color]',
            size_hint_x=0.4,
            background_normal='',
            background_color=(0.25, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=sp(20),
            markup=True
        )

        options_layout.add_widget(self.anonymous_toggle)
        options_layout.add_widget(photo_btn)

        publish_btn = Button(
            text='Publicar Historia',
            size_hint_y=None,
            height=dp(55),
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            bold=True
        )
        publish_btn.bind(on_press=self.publish_story)

        form_layout.add_widget(self.content_input)
        form_layout.add_widget(self.location_input)
        form_layout.add_widget(category_label)
        form_layout.add_widget(self.category_spinner)
        form_layout.add_widget(options_layout)
        form_layout.add_widget(publish_btn)

        scroll.add_widget(form_layout)

        navbar = NavBar()

        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(navbar)

        self.add_widget(layout)

    def update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def publish_story(self, instance):
        app = App.get_running_app()

        if not hasattr(app, 'current_user'):
            self.show_popup('Error', 'Debes iniciar sesión para publicar')
            return

        content = self.content_input.text.strip()
        location = self.location_input.text.strip()
        category = self.category_spinner.text
        is_anonymous = self.anonymous_toggle.state == 'down'

        if not content:
            self.show_popup('Error', 'Por favor escribe tu historia')
            return

        if self.db.create_story(
            user_id=app.current_user['id'],
            content=content,
            location=location if location else 'Chile',
            category=category,
            is_anonymous=is_anonymous
        ):
            self.show_popup('Éxito', 'Historia publicada exitosamente')
            self.content_input.text = ''
            self.location_input.text = ''
            self.category_spinner.text = 'Aparición'
            self.anonymous_toggle.state = 'normal'
            self.manager.current = 'feed'
        else:
            self.show_popup('Error', 'No se pudo publicar la historia')

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, color=(0.9, 0.9, 0.9, 1)))
        btn_close = Button(text='OK', size_hint_y=None, height=dp(40))

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3),
            background_color=(0.15, 0.15, 0.2, 1)
        )
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)
        popup.open()

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = BoxLayout(orientation='vertical')

        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(65),
            padding=[dp(15), dp(10)]
        )

        with header.canvas.before:
            Color(0.1, 0.1, 0.14, 1)
            self.header_bg = Rectangle(pos=header.pos, size=header.size)

        header.bind(pos=self.update_header_bg, size=self.update_header_bg)

        title = Label(
            text='[color=#FFD700]👤[/color] Mi Perfil',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            markup=True
        )
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)

        scroll = ScrollView()
        self.content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(12), dp(12)]
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        scroll.add_widget(self.content_layout)

        navbar = NavBar()

        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(navbar)

        self.add_widget(layout)

    def update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def on_enter(self):
        self.load_profile()

    def load_profile(self):
        self.content_layout.clear_widgets()
        app = App.get_running_app()

        if not hasattr(app, 'current_user'):
            guest_message = Label(
                text='Inicia sesión para ver tu perfil',
                font_size=sp(16),
                color=(0.6, 0.6, 0.6, 1),
                size_hint_y=None,
                height=dp(60)
            )

            login_btn = Button(
                text='Iniciar Sesión',
                size_hint=(None, None),
                size=(dp(200), dp(55)),
                pos_hint={'center_x': 0.5},
                background_normal='',
                background_color=(0.5, 0.2, 0.6, 1),
                color=(1, 1, 1, 1),
                font_size=sp(16),
                bold=True
            )
            login_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))

            self.content_layout.add_widget(guest_message)
            self.content_layout.add_widget(login_btn)
            return

        user = app.current_user
        stories = self.db.get_user_stories(user['id'])

        profile_info = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=dp(10),
            padding=[dp(20), dp(20)]
        )

        with profile_info.canvas.before:
            Color(0.12, 0.12, 0.17, 1)
            self.profile_bg = RoundedRectangle(
                pos=profile_info.pos,
                size=profile_info.size,
                radius=[dp(15)]
            )

        profile_info.bind(pos=self.update_profile_bg, size=self.update_profile_bg)

        username_label = Label(
            text=f"[color=#FFD700]👤[/color] {user['username']}",
            font_size=sp(26),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            size_hint_y=None,
            height=dp(40),
            markup=True
        )

        email_label = Label(
            text=f"[color=#FFD700]@[/color] {user['email']}",
            font_size=sp(14),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
            markup=True
        )

        stats_label = Label(
            text=f"[color=#FFD700]📖[/color] {len(stories)} historias publicadas",
            font_size=sp(16),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(35),
            markup=True
        )

        profile_info.add_widget(username_label)
        profile_info.add_widget(email_label)
        profile_info.add_widget(stats_label)

        logout_btn = Button(
            text='Cerrar Sesión',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(15)
        )
        logout_btn.bind(on_press=self.logout)

        stories_title = Label(
            text='[color=#FFD700]📚[/color] Mis Historias',
            font_size=sp(18),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=None,
            height=dp(45),
            halign='left',
            valign='middle',
            markup=True
        )
        stories_title.bind(size=stories_title.setter('text_size'))

        self.content_layout.add_widget(profile_info)
        self.content_layout.add_widget(logout_btn)
        self.content_layout.add_widget(stories_title)

        if stories:
            for story in stories:
                card = StoryCard(story, show_actions=False)
                self.content_layout.add_widget(card)
        else:
            no_stories = Label(
                text='Aún no has publicado historias\n\n¡Comparte tu experiencia paranormal!',
                font_size=sp(14),
                color=(0.6, 0.6, 0.6, 1),
                halign='center',
                size_hint_y=None,
                height=dp(80)
            )
            no_stories.bind(size=no_stories.setter('text_size'))
            self.content_layout.add_widget(no_stories)

    def update_profile_bg(self, instance, value):
        self.profile_bg.pos = instance.pos
        self.profile_bg.size = instance.size

    def logout(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            delattr(app, 'current_user')
        self.manager.current = 'welcome'

class ParanormalApp(App):
    def build(self):
        self.title = 'Historias Paranormales de Chile'

        db = Database()
        all_stories = db.get_all_stories()
        if len(all_stories) == 0:
            db.create_sample_data()

        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(FeedScreen(name='feed'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(CreateScreen(name='create'))
        sm.add_widget(ProfileScreen(name='profile'))

        # Configurar el screen manager en todas las barras de navegación
        self.setup_navbars(sm)

        return sm

    def setup_navbars(self, screen_manager):
        """Configura el screen manager en todas las barras de navegación"""
        for screen in screen_manager.screens:
            if hasattr(screen, 'children'):
                for child in screen.children:
                    if isinstance(child, BoxLayout):
                        for grandchild in child.children:
                            if isinstance(grandchild, NavBar):
                                grandchild.set_screen_manager(screen_manager)

if __name__ == '__main__':
    ParanormalApp().run()
