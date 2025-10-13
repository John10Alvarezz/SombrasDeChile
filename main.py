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
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.metrics import dp, sp
from database import Database
from widgets.navbar import NavBar
from widgets.story_card import StoryCard
import os

Window.clearcolor = (0.08, 0.08, 0.12, 1)
Window.size = (400, 700)

# Configurar la fuente para mejor soporte de emojis
from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel
from kivy.core.text import DEFAULT_FONT
from kivy.core.text import LabelBase
from kivy.uix.carousel import Carousel

# Configurar fuente para mejor soporte de emojis
def configure_font():
    """Configura la fuente para mejor soporte de emojis"""
    try:
        # Configurar fuente por defecto
        from kivy.core.text import DEFAULT_FONT
        print(f"Fuente por defecto: {DEFAULT_FONT}")

        # Lista ampliada de rutas de fuentes emoji para Windows
        potential_paths = [
            r"C:\\Windows\\Fonts\\seguiemj.ttf",  # Segoe UI Emoji
            r"C:\\Windows\\Fonts\\SegoeUIEmoji.ttf",
            r"C:\\Windows\\Fonts\\seguisym.ttf",    # Segoe UI Symbol (contiene algunos emojis)
            r"C:\\Windows\\Fonts\\arial.ttf",       # Arial (soporte Unicode)
            r"C:\\Windows\\Fonts\\calibri.ttf",     # Calibri
            r"C:\\Windows\\Fonts\\tahoma.ttf",      # Tahoma
        ]

        emoji_font_registered = False
        for p in potential_paths:
            if os.path.exists(p):
                try:
                    LabelBase.register(name='EmojiFont', fn_regular=p)
                    emoji_font_registered = True
                    print(f"Fuente emoji registrada desde: {p}")
                    break
                except Exception as e:
                    print(f"Error registrando fuente {p}: {e}")
                    continue

        # Si no se encontró fuente específica, intentar usar defaults
        if not emoji_font_registered:
            try:
                LabelBase.register_defaults()
                print("Usando fuentes por defecto del sistema")
            except Exception as e:
                print(f"Error registrando defaults: {e}")

        # Forzar registro de Segoe UI Emoji si existe
        try:
            import ctypes
            # Intentar acceder a fuentes del sistema
            font_path = r"C:\\Windows\\Fonts\\seguiemj.ttf"
            if os.path.exists(font_path):
                LabelBase.register(name='SegoeUIEmoji', fn_regular=font_path)
                print("Segoe UI Emoji registrado exitosamente")
        except Exception as e:
            print(f"No se pudo registrar Segoe UI Emoji: {e}")

        print("Configuración de fuente completada")

    except Exception as e:
        print(f"Error configurando fuente: {e}")

# Configurar la fuente al inicio
configure_font()


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
            text='[color=#9966CC]👻[/color]',
            font_size=sp(80),
            color=(0.6, 0.3, 0.7, 1),
            size_hint_y=None,
            height=dp(100),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
            text='⬅ Volver',
            size_hint_y=None,
            height=dp(45),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(16)
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
            text='⬅ Volver',
            size_hint_y=None,
            height=dp(45),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(16)
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



class FeedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.is_guest = False
        self.page_size = 10
        self.offset = 0

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
            markup=True,
            font_name='SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
        self.reset_and_load()

    def reset_and_load(self):
        self.offset = 0
        self.stories_layout.clear_widgets()
        self.load_stories()

    def load_stories(self):
        stories = self.db.get_all_stories(limit=self.page_size, offset=self.offset)

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
                    on_comment=self.open_story_detail if not self.is_guest else None,
                    show_actions=not self.is_guest
                )
                # Al tocar header, location o content de la tarjeta, abrir detalle
                card.header.bind(on_touch_down=lambda w, t, s=story: self.open_story_detail(s) if w.collide_point(*t.pos) else None)
                card.location.bind(on_touch_down=lambda w, t, s=story: self.open_story_detail(s) if w.collide_point(*t.pos) else None)
                card.content.bind(on_touch_down=lambda w, t, s=story: self.open_story_detail(s) if w.collide_point(*t.pos) else None)
                self.stories_layout.add_widget(card)

            # Mostrar botón "Cargar más" si podría haber más resultados
            if len(stories) == self.page_size:
                load_more_btn = Button(
                    text='Cargar más',
                    size_hint_y=None,
                    height=dp(50),
                    background_normal='',
                    background_color=(0.2, 0.2, 0.25, 1),
                    color=(1, 1, 1, 1),
                    font_size=sp(16)
                )
                load_more_btn.bind(on_press=self.load_more)
                self.stories_layout.add_widget(load_more_btn)

    def like_story(self, story):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.add_like(story['id'], app.current_user['id'])
            self.reset_and_load()

    def add_reaction(self, story, tipo):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.add_reaction(story['id'], app.current_user['id'], tipo)
            self.reset_and_load()

    def load_more(self, instance):
        # Remover el botón "Cargar más" actual antes de añadir nuevos elementos
        if instance in self.stories_layout.children:
            self.stories_layout.remove_widget(instance)
        self.offset += self.page_size
        self.load_stories()

    def open_story_detail(self, story):
        # Navegar a la pantalla de detalle de historia
        detail_screen = self.manager.get_screen('story_detail')
        detail_screen.load_story_detail(story)
        self.manager.current = 'story_detail'

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
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
            font_size=sp(16)
        )

        search_btn = Button(
            text='[color=#FFFFFF]🔍[/color]',
            size_hint_x=0.25,
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(20),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
                font_size=sp(16),
                color=(0.6, 0.6, 0.6, 1)
            )
            self.results_layout.add_widget(info)
            return

        stories = self.db.search_stories(query)

        if not stories:
            no_results = Label(
                text=f'No se encontraron historias para "{query}"',
                font_size=sp(16),
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
        self.selected_images = []  # rutas locales guardadas

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
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
            font_size=sp(16)
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
            font_size=sp(16)
        )

        category_label = Label(
            text='Categoría:',
            font_size=sp(16),
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
            font_size=sp(16)
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
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )

        photo_btn = Button(
            text='[color=#FFD700]📷[/color]',
            size_hint_x=0.4,
            background_normal='',
            background_color=(0.25, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=sp(20),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        photo_btn.bind(on_press=self.open_file_chooser)

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
        # Preview de imágenes seleccionadas
        self.images_preview = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100), spacing=dp(6))
        form_layout.add_widget(self.images_preview)
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
            # Obtener el último story insertado por el usuario para asociar imágenes
            stories = self.db.get_user_stories(app.current_user['id'])
            new_story_id = stories[0]['id'] if stories else None
            if new_story_id and self.selected_images:
                self.db.add_story_images(new_story_id, self.selected_images)
            self.show_popup('Éxito', 'Historia publicada exitosamente')
            self.content_input.text = ''
            self.location_input.text = ''
            self.category_spinner.text = 'Aparición'
            self.anonymous_toggle.state = 'normal'
            self.selected_images = []
            self.images_preview.clear_widgets()
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

    def open_file_chooser(self, instance):
        chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.webp'], multiselect=True)
        chooser.path = os.path.expanduser('~')

        def on_select(_instance, selection):
            # Limitar a 4 y copiar a carpeta media local
            target_dir = os.path.join(os.getcwd(), 'media')
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            chosen = selection[:4]
            saved_paths = []
            for src in chosen:
                try:
                    filename = os.path.basename(src)
                    # evitar colisiones
                    base, ext = os.path.splitext(filename)
                    unique_name = f"{base}_{int(Window._get_window()._counter if hasattr(Window, '_get_window') else 0)}{ext}"
                    dest = os.path.join(target_dir, unique_name)
                    with open(src, 'rb') as fsrc, open(dest, 'wb') as fdst:
                        fdst.write(fsrc.read())
                    # Usar ruta relativa para Kivy
                    saved_paths.append(dest)
                except Exception as e:
                    print(f"Error copiando imagen: {e}")

            self.selected_images = saved_paths
            self.refresh_images_preview()
            popup.dismiss()

        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(chooser)
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10), padding=[dp(10), dp(10)])
        btn_ok = Button(text='Seleccionar')
        btn_cancel = Button(text='Cancelar')
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_ok)
        popup_content.add_widget(btns)
        popup = Popup(title='Selecciona hasta 4 imágenes', content=popup_content, size_hint=(0.9, 0.9))
        btn_cancel.bind(on_press=popup.dismiss)
        btn_ok.bind(on_press=lambda x: on_select(chooser, chooser.selection))
        popup.open()

    def refresh_images_preview(self):
        self.images_preview.clear_widgets()
        for path in self.selected_images[:4]:
            try:
                img = Image(source=path, allow_stretch=True, keep_ratio=True)
                self.images_preview.add_widget(img)
            except Exception as e:
                print(f"Error cargando preview: {e}")

class StoryDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_story = None

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

        back_btn = Button(
            text='[color=#FFD700]⬅[/color] Volver',
            size_hint_x=None,
            width=dp(120),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(16),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        back_btn.bind(on_press=self.go_back)

        title = Label(
            text='[color=#FFD700]📖[/color] Detalle de Historia',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        title.bind(size=title.setter('text_size'))

        header.add_widget(back_btn)
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

        layout.add_widget(header)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'feed'

    def load_story_detail(self, story):
        self.current_story = story
        self.content_layout.clear_widgets()

        # Información del autor y ubicación
        author_info = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        username_text = story.get('username', 'Anónimo') if not story.get('is_anonymous') else '[color=#FFD700]👤[/color] Anónimo'
        username = Label(
            text=username_text,
            font_size=sp(18),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_x=0.6,
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        username.bind(size=username.setter('text_size'))

        location = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('location', 'Sin ubicación')}",
            font_size=sp(14),
            color=(0.6, 0.6, 0.7, 1),
            size_hint_x=0.4,
            halign='right',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        location.bind(size=location.setter('text_size'))

        author_info.add_widget(username)
        author_info.add_widget(location)

        # Contenido completo de la historia
        content = Label(
            text=story.get('content', ''),
            font_size=sp(16),
            color=(0.85, 0.85, 0.85, 1),
            size_hint_y=None,
            text_size=(Window.width - dp(50), None),
            halign='left',
            valign='top'
        )
        content.bind(size=content.setter('text_size'))
        content.bind(text_size=content.setter('size'))

        # Imágenes si existen
        images = story.get('images') or []
        if images:
            from kivy.uix.carousel import Carousel
            carousel = Carousel(direction='right', loop=True, size_hint_y=None, height=dp(260))
            for path in images:
                try:
                    img = Image(source=path, allow_stretch=True, keep_ratio=True)
                    carousel.add_widget(img)
                except Exception as e:
                    print(f"Error cargando imagen: {e}")

        # Botones de interacción
        actions = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        like_btn = Button(
            text=f"[color=#FFD700]❤️[/color] {story.get('likes', 0)}",
            size_hint_x=0.2,
            background_normal='',
            background_color=(0.3, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size=sp(14),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        like_btn.bind(on_press=lambda x: self.like_story())

        report_btn = Button(
            text=f"[color=#FF6B6B]🚨[/color] Reportar",
            size_hint_x=0.2,
            background_normal='',
            background_color=(0.4, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(12),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        report_btn.bind(on_press=lambda x: self.report_story())

        miedo_btn = Button(
            text=f"[color=#FF6B6B]😱[/color] {story.get('miedo', 0)}",
            size_hint_x=0.2,
            background_normal='',
            background_color=(0.35, 0.15, 0.25, 1),
            color=(1, 1, 1, 1),
            font_size=sp(14),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        miedo_btn.bind(on_press=lambda x: self.add_reaction('miedo'))

        sorpresa_btn = Button(
            text=f"[color=#4ECDC4]😮[/color] {story.get('sorpresa', 0)}",
            size_hint_x=0.2,
            background_normal='',
            background_color=(0.25, 0.25, 0.35, 1),
            color=(1, 1, 1, 1),
            font_size=sp(14),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        sorpresa_btn.bind(on_press=lambda x: self.add_reaction('sorpresa'))

        incredulidad_btn = Button(
            text=f"[color=#FFE66D]🙄[/color] {story.get('incredulidad', 0)}",
            size_hint_x=0.2,
            background_normal='',
            background_color=(0.3, 0.3, 0.25, 1),
            color=(1, 1, 1, 1),
            font_size=sp(14),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        incredulidad_btn.bind(on_press=lambda x: self.add_reaction('incredulidad'))

        actions.add_widget(like_btn)
        actions.add_widget(report_btn)
        actions.add_widget(miedo_btn)
        actions.add_widget(sorpresa_btn)
        actions.add_widget(incredulidad_btn)

        # Fecha de publicación
        date = Label(
            text=f"[color=#FFD700]📅[/color] {story.get('created_at', '')}",
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(30),
            halign='right',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        date.bind(size=date.setter('text_size'))

        # Sección de comentarios
        comments_title = Label(
            text='[color=#FFD700]💬[/color] Comentarios',
            font_size=sp(18),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=None,
            height=dp(40),
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        comments_title.bind(size=comments_title.setter('text_size'))

        # Campo para nuevo comentario
        comment_input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        self.comment_input = TextInput(
            hint_text='Escribe tu comentario...',
            multiline=False,
            size_hint_x=0.8,
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(16)
        )

        comment_btn = Button(
            text='[color=#FFD700]📤[/color]',
            size_hint_x=0.2,
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(20),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        comment_btn.bind(on_press=self.add_comment)

        comment_input_layout.add_widget(self.comment_input)
        comment_input_layout.add_widget(comment_btn)

        # Lista de comentarios
        self.comments_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        self.comments_layout.bind(minimum_height=self.comments_layout.setter('height'))

        # Agregar todos los elementos
        self.content_layout.add_widget(author_info)
        self.content_layout.add_widget(content)
        
        if images:
            self.content_layout.add_widget(carousel)
        
        self.content_layout.add_widget(actions)
        self.content_layout.add_widget(date)
        self.content_layout.add_widget(comments_title)
        self.content_layout.add_widget(comment_input_layout)
        self.content_layout.add_widget(self.comments_layout)

        # Cargar comentarios existentes
        self.load_comments()

    def like_story(self):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.add_like(self.current_story['id'], app.current_user['id'])
            self.load_story_detail(self.current_story)  # Recargar para actualizar contadores

    def add_reaction(self, tipo):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.add_reaction(self.current_story['id'], app.current_user['id'], tipo)
            self.load_story_detail(self.current_story)  # Recargar para actualizar contadores

    def report_story(self):
        """Navegar a la pantalla de reporte de historia"""
        report_screen = self.manager.get_screen('report')
        report_screen.load_story_for_report(self.current_story)
        self.manager.current = 'report'

    def add_comment(self, instance):
        app = App.get_running_app()
        if not hasattr(app, 'current_user'):
            self.show_popup('Error', 'Debes iniciar sesión para comentar')
            return

        comment_text = self.comment_input.text.strip()
        if not comment_text:
            self.show_popup('Error', 'Escribe un comentario')
            return

        if self.db.add_comment(self.current_story['id'], app.current_user['id'], comment_text):
            self.comment_input.text = ''
            self.load_comments()  # Recargar solo los comentarios
        else:
            self.show_popup('Error', 'No se pudo agregar el comentario')

    def load_comments(self):
        if not self.current_story:
            return

        self.comments_layout.clear_widgets()
        comments = self.db.get_comments(self.current_story['id'])

        if not comments:
            no_comments = Label(
                text='No hay comentarios aún.\n¡Sé el primero en comentar!',
                font_size=sp(14),
                color=(0.6, 0.6, 0.6, 1),
                halign='center',
                size_hint_y=None,
                height=dp(60)
            )
            no_comments.bind(size=no_comments.setter('text_size'))
            self.comments_layout.add_widget(no_comments)
        else:
            for comment in comments:
                comment_card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(80),
                    spacing=dp(5),
                    padding=[dp(10), dp(8)]
                )

                with comment_card.canvas.before:
                    Color(0.15, 0.15, 0.2, 1)
                    RoundedRectangle(pos=comment_card.pos, size=comment_card.size, radius=[dp(8)])

                comment_header = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(25),
                    spacing=dp(8)
                )

                comment_author = Label(
                    text=f"[color=#FFD700]👤[/color] {comment.get('username', 'Usuario')}",
                    font_size=sp(12),
                    bold=True,
                    color=(0.8, 0.8, 0.8, 1),
                    size_hint_x=0.7,
                    halign='left',
                    valign='middle',
                    markup=True,
                    font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
                )
                comment_author.bind(size=comment_author.setter('text_size'))

                comment_date = Label(
                    text=comment.get('created_at', ''),
                    font_size=sp(10),
                    color=(0.5, 0.5, 0.5, 1),
                    size_hint_x=0.3,
                    halign='right',
                    valign='middle'
                )
                comment_date.bind(size=comment_date.setter('text_size'))

                comment_header.add_widget(comment_author)
                comment_header.add_widget(comment_date)

                comment_content = Label(
                    text=comment.get('content', ''),
                    font_size=sp(13),
                    color=(0.9, 0.9, 0.9, 1),
                    size_hint_y=None,
                    text_size=(Window.width - dp(80), None),
                    halign='left',
                    valign='top'
                )
                comment_content.bind(size=comment_content.setter('text_size'))
                comment_content.bind(text_size=comment_content.setter('size'))

                comment_card.add_widget(comment_header)
                comment_card.add_widget(comment_content)

                self.comments_layout.add_widget(comment_card)

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

class NotificationsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.notifications = []
        self.offset = 0
        self.page_size = 20

    def on_enter(self):
        """Se ejecuta cuando se entra a la pantalla."""
        self.load_notifications()

    def load_notifications(self):
        """Carga las notificaciones del usuario actual."""
        app = App.get_running_app()
        if not hasattr(app, 'current_user'):
            return

        # Limpiar notificaciones existentes
        self.notifications_layout.clear_widgets()

        # Obtener notificaciones de la base de datos
        notifications = self.db.get_user_notifications(
            app.current_user['id'], 
            limit=self.page_size, 
            offset=self.offset
        )

        if not notifications:
            # Mostrar mensaje si no hay notificaciones
            no_notifications = Label(
                text='No tienes notificaciones',
                font_size=sp(16),
                color=(0.6, 0.6, 0.6, 1),
                halign='center'
            )
            self.notifications_layout.add_widget(no_notifications)
        else:
            for notification in notifications:
                card = self.create_notification_card(notification)
                self.notifications_layout.add_widget(card)

    def create_notification_card(self, notification):
        """Crea una tarjeta de notificación."""
        card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(12),
            padding=[dp(16), dp(12)]
        )

        with card.canvas.before:
            Color(0.12, 0.12, 0.17, 1)
            card.bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])

        # Icono según el tipo de notificación
        icon_map = {
            'like': '❤️',
            'comment': '💬',
            'reaction': '😮',
            'report': '🚨'
        }
        icon = icon_map.get(notification['tipo'], '🔔')

        icon_label = Label(
            text=icon,
            font_size=sp(24),
            size_hint_x=None,
            width=dp(40),
            halign='center',
            valign='middle',
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )

        # Contenido de la notificación
        content = BoxLayout(orientation='vertical', spacing=dp(4))
        
        title = Label(
            text=notification['titulo'],
            font_size=sp(14),
            color=(1, 1, 1, 1),
            halign='left',
            text_size=(None, None)
        )

        message = Label(
            text=notification['mensaje'],
            font_size=sp(12),
            color=(0.8, 0.8, 0.8, 1),
            halign='left',
            text_size=(None, None)
        )

        date = Label(
            text=notification['created_at'],
            font_size=sp(10),
            color=(0.6, 0.6, 0.6, 1),
            halign='left'
        )

        content.add_widget(title)
        content.add_widget(message)
        content.add_widget(date)

        # Indicador de no leída
        if not notification['leida']:
            indicator = BoxLayout(
                size_hint_x=None,
                width=dp(8),
                background_color=(0.2, 0.6, 1, 1)
            )
            card.add_widget(indicator)

        card.add_widget(icon_label)
        card.add_widget(content)

        # Al tocar la notificación, marcarla como leída y navegar a la historia si aplica
        def on_notification_tap(instance, touch):
            if instance.collide_point(*touch.pos):
                if not notification['leida']:
                    self.db.mark_notification_as_read(notification['id'], notification['user_id'])
                    self.load_notifications()  # Recargar para actualizar UI
                
                if notification['story_id']:
                    # Navegar a la historia
                    detail_screen = self.manager.get_screen('story_detail')
                    story = self.db.get_story_by_id(notification['story_id'])
                    if story:
                        detail_screen.load_story_detail(story)
                        self.manager.current = 'story_detail'

        card.bind(on_touch_down=on_notification_tap)

        return card

    def mark_all_as_read(self, instance):
        """Marca todas las notificaciones como leídas."""
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            self.db.mark_all_notifications_as_read(app.current_user['id'])
            self.load_notifications()

    def build(self):
        """Construye la interfaz de la pantalla de notificaciones."""
        layout = BoxLayout(orientation='vertical')

        # Header
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=[dp(16), dp(8)],
            spacing=dp(16)
        )

        title = Label(
            text='[color=#FFD700]🔔[/color] Notificaciones',
            font_size=sp(20),
            color=(1, 1, 1, 1),
            markup=True,
            halign='left',
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )

        mark_all_btn = Button(
            text='Marcar todas',
            size_hint_x=None,
            width=dp(120),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=sp(12)
        )
        mark_all_btn.bind(on_press=self.mark_all_as_read)

        header.add_widget(title)
        header.add_widget(mark_all_btn)

        # ScrollView para las notificaciones
        scroll = ScrollView()
        self.notifications_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8),
            padding=[dp(16), dp(8)]
        )
        self.notifications_layout.bind(minimum_height=self.notifications_layout.setter('height'))
        scroll.add_widget(self.notifications_layout)

        layout.add_widget(header)
        layout.add_widget(scroll)

        return layout

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_story = None

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

        back_btn = Button(
            text='[color=#FFD700]⬅[/color] Cancelar',
            size_hint_x=None,
            width=dp(140),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(16),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        back_btn.bind(on_press=self.go_back)

        title = Label(
            text='[color=#FF6B6B]🚨[/color] Reportar Contenido',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        title.bind(size=title.setter('text_size'))

        header.add_widget(back_btn)
        header.add_widget(title)

        scroll = ScrollView()
        form_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(12), dp(12)]
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Información de la historia reportada
        story_info = Label(
            text='Historia reportada:',
            font_size=sp(16),
            bold=True,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        )
        story_info.bind(size=story_info.setter('text_size'))

        self.story_preview = Label(
            text='',
            font_size=sp(14),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            text_size=(Window.width - dp(50), None),
            halign='left',
            valign='top'
        )
        self.story_preview.bind(size=self.story_preview.setter('text_size'))
        self.story_preview.bind(text_size=self.story_preview.setter('size'))

        # Motivos de reporte
        motivo_label = Label(
            text='Motivo del reporte:',
            font_size=sp(16),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        )
        motivo_label.bind(size=motivo_label.setter('text_size'))

        self.motivo_spinner = Spinner(
            text='Selecciona un motivo',
            values=('Contenido inapropiado', 'Spam', 'Información falsa', 'Acoso', 'Violencia', 'Otro'),
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16)
        )

        # Descripción adicional
        descripcion_label = Label(
            text='Descripción adicional (opcional):',
            font_size=sp(16),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        )
        descripcion_label.bind(size=descripcion_label.setter('text_size'))

        self.descripcion_input = TextInput(
            hint_text='Proporciona más detalles sobre el problema...',
            multiline=True,
            size_hint_y=None,
            height=dp(120),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)],
            font_size=sp(16)
        )

        # Botón de enviar reporte
        submit_btn = Button(
            text='[color=#FFD700]📤[/color] Enviar Reporte',
            size_hint_y=None,
            height=dp(55),
            background_normal='',
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            bold=True,
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        submit_btn.bind(on_press=self.submit_report)

        form_layout.add_widget(story_info)
        form_layout.add_widget(self.story_preview)
        form_layout.add_widget(motivo_label)
        form_layout.add_widget(self.motivo_spinner)
        form_layout.add_widget(descripcion_label)
        form_layout.add_widget(self.descripcion_input)
        form_layout.add_widget(submit_btn)

        scroll.add_widget(form_layout)

        layout.add_widget(header)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'feed'

    def load_story_for_report(self, story):
        """Carga la información de una historia para reportar"""
        self.current_story = story
        
        # Mostrar preview de la historia
        preview_text = f"Por: {story.get('username', 'Anónimo')}\n"
        preview_text += f"Ubicación: {story.get('location', 'Sin ubicación')}\n"
        preview_text += f"Categoría: {story.get('category', 'Aparición')}\n\n"
        
        content = story.get('content', '')
        if len(content) > 150:
            content = content[:150] + '...'
        preview_text += content
        
        self.story_preview.text = preview_text

    def submit_report(self, instance):
        app = App.get_running_app()
        if not hasattr(app, 'current_user'):
            self.show_popup('Error', 'Debes iniciar sesión para reportar')
            return

        if not self.current_story:
            self.show_popup('Error', 'No hay historia seleccionada')
            return

        motivo = self.motivo_spinner.text
        descripcion = self.descripcion_input.text.strip()

        if motivo == 'Selecciona un motivo':
            self.show_popup('Error', 'Por favor selecciona un motivo para el reporte')
            return

        if self.db.create_report(
            story_id=self.current_story['id'],
            reporter_id=app.current_user['id'],
            motivo=motivo,
            descripcion=descripcion if descripcion else None
        ):
            self.show_popup('Éxito', 'Reporte enviado exitosamente. Gracias por ayudarnos a mantener la comunidad segura.')
            self.manager.current = 'feed'
        else:
            self.show_popup('Error', 'No se pudo enviar el reporte. Es posible que ya hayas reportado esta historia.')

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

class EditStoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_story = None

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

        back_btn = Button(
            text='[color=#FFD700]⬅[/color] Cancelar',
            size_hint_x=None,
            width=dp(140),
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0.7, 0.7, 0.7, 1),
            font_size=sp(16),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        back_btn.bind(on_press=self.go_back)

        title = Label(
            text='[color=#FFD700]✏️[/color] Editar Historia',
            font_size=sp(22),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        title.bind(size=title.setter('text_size'))

        header.add_widget(back_btn)
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
            font_size=sp(16)
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
            font_size=sp(16)
        )

        category_label = Label(
            text='Categoría:',
            font_size=sp(16),
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
            font_size=sp(16)
        )

        self.anonymous_toggle = ToggleButton(
            text='[color=#FFD700]👤[/color] Modo Incógnito',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=(0.25, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=sp(13),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )

        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        save_btn = Button(
            text='[color=#FFD700]💾[/color] Guardar Cambios',
            size_hint_x=0.6,
            background_normal='',
            background_color=(0.5, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            bold=True,
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        save_btn.bind(on_press=self.save_changes)

        delete_btn = Button(
            text='[color=#FF6B6B]🗑️[/color] Eliminar',
            size_hint_x=0.4,
            background_normal='',
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(16),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        delete_btn.bind(on_press=self.delete_story)

        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(delete_btn)

        form_layout.add_widget(self.content_input)
        form_layout.add_widget(self.location_input)
        form_layout.add_widget(category_label)
        form_layout.add_widget(self.category_spinner)
        form_layout.add_widget(self.anonymous_toggle)
        form_layout.add_widget(buttons_layout)

        scroll.add_widget(form_layout)

        layout.add_widget(header)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'profile'

    def load_story_for_edit(self, story):
        """Carga los datos de una historia para editar"""
        self.current_story = story
        
        # Pre-rellenar los campos con los datos actuales
        self.content_input.text = story.get('content', '')
        self.location_input.text = story.get('location', '')
        self.category_spinner.text = story.get('category', 'Aparición')
        self.anonymous_toggle.state = 'down' if story.get('is_anonymous') else 'normal'

    def save_changes(self, instance):
        app = App.get_running_app()
        if not hasattr(app, 'current_user'):
            self.show_popup('Error', 'Debes iniciar sesión')
            return

        if not self.current_story:
            self.show_popup('Error', 'No hay historia seleccionada')
            return

        content = self.content_input.text.strip()
        location = self.location_input.text.strip()
        category = self.category_spinner.text
        is_anonymous = self.anonymous_toggle.state == 'down'

        if not content:
            self.show_popup('Error', 'Por favor escribe el contenido de la historia')
            return

        if self.db.update_story(
            story_id=self.current_story['id'],
            user_id=app.current_user['id'],
            content=content,
            location=location if location else 'Chile',
            category=category,
            is_anonymous=is_anonymous
        ):
            self.show_popup('Éxito', 'Historia actualizada exitosamente')
            self.manager.current = 'profile'
        else:
            self.show_popup('Error', 'No se pudo actualizar la historia')

    def delete_story(self, instance):
        app = App.get_running_app()
        if not hasattr(app, 'current_user'):
            self.show_popup('Error', 'Debes iniciar sesión')
            return

        if not self.current_story:
            self.show_popup('Error', 'No hay historia seleccionada')
            return

        # Mostrar confirmación
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(
            text='¿Estás seguro de que quieres eliminar esta historia?\n\nEsta acción no se puede deshacer.',
            color=(0.9, 0.9, 0.9, 1),
            halign='center'
        ))
        
        buttons_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_cancel = Button(text='Cancelar', background_color=(0.3, 0.3, 0.3, 1))
        btn_confirm = Button(text='Eliminar', background_color=(0.6, 0.2, 0.2, 1))
        
        buttons_layout.add_widget(btn_cancel)
        buttons_layout.add_widget(btn_confirm)
        content.add_widget(buttons_layout)

        popup = Popup(
            title='Confirmar Eliminación',
            content=content,
            size_hint=(0.8, 0.4),
            background_color=(0.15, 0.15, 0.2, 1)
        )
        
        btn_cancel.bind(on_press=popup.dismiss)
        btn_confirm.bind(on_press=lambda x: self.confirm_delete(popup))
        
        popup.open()

    def confirm_delete(self, popup):
        popup.dismiss()
        
        if self.db.delete_story(self.current_story['id'], App.get_running_app().current_user['id']):
            self.show_popup('Éxito', 'Historia eliminada exitosamente')
            self.manager.current = 'profile'
        else:
            self.show_popup('Error', 'No se pudo eliminar la historia')

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
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )

        email_label = Label(
            text=f"[color=#FFD700]@[/color] {user['email']}",
            font_size=sp(16),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )

        stats_label = Label(
            text=f"[color=#FFD700]📖[/color] {len(stories)} historias publicadas",
            font_size=sp(16),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(35),
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        stories_title.bind(size=stories_title.setter('text_size'))

        self.content_layout.add_widget(profile_info)
        self.content_layout.add_widget(logout_btn)
        self.content_layout.add_widget(stories_title)

        if stories:
            for story in stories:
                # Crear un layout especial para historias propias con botón de editar
                story_container = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    spacing=dp(5)
                )
                
                # Agregar la tarjeta de historia
                card = StoryCard(story, show_actions=False)
                story_container.add_widget(card)
                
                # Agregar botón de editar para historias propias
                edit_btn = Button(
                    text='[color=#FFD700]✏️[/color] Editar Historia',
                    size_hint_y=None,
                    height=dp(40),
                    background_normal='',
                    background_color=(0.3, 0.3, 0.4, 1),
                    color=(1, 1, 1, 1),
                    font_size=sp(14),
                    markup=True,
                    font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
                )
                edit_btn.bind(on_press=lambda x, s=story: self.edit_story(s))
                story_container.add_widget(edit_btn)
                
                self.content_layout.add_widget(story_container)
        else:
            no_stories = Label(
                text='Aún no has publicado historias\n\n¡Comparte tu experiencia paranormal!',
                font_size=sp(16),
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

    def edit_story(self, story):
        """Navegar a la pantalla de edición de historia"""
        edit_screen = self.manager.get_screen('edit_story')
        edit_screen.load_story_for_edit(story)
        self.manager.current = 'edit_story'

    def logout(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            delattr(app, 'current_user')
        self.manager.current = 'welcome'

class ParanormalApp(App):
    def build(self):
        self.title = 'Historias Paranormales de Chile'

        db = Database()
        all_stories = db.get_all_stories(limit=1, offset=0)
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
        sm.add_widget(StoryDetailScreen(name='story_detail'))
        sm.add_widget(EditStoryScreen(name='edit_story'))
        sm.add_widget(ReportScreen(name='report'))
        sm.add_widget(NotificationsScreen(name='notifications'))

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
