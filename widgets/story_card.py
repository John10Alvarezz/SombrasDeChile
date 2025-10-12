from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp


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

        self.header = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(8))

        username_text = story.get('username', 'Anónimo') if not story.get('is_anonymous') else '[color=#FFD700]👤[/color] Anónimo'
        username = Label(
            text=username_text,
            font_size=sp(14),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_x=0.5,
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        username.bind(size=username.setter('text_size'))

        category = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('category', 'Aparición')}",
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_x=0.5,
            halign='right',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        category.bind(size=category.setter('text_size'))

        self.header.add_widget(username)
        self.header.add_widget(category)

        self.location = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('location', 'Sin ubicación')}",
            font_size=sp(12),
            color=(0.6, 0.6, 0.7, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            valign='middle',
            markup=True,
            font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
        )
        self.location.bind(size=self.location.setter('text_size'))

        content_text = story.get('content', '')
        if len(content_text) > 180:
            content_text = content_text[:180] + '...'

        self.content = Label(
            text=content_text,
            font_size=sp(13),
            color=(0.85, 0.85, 0.85, 1),
            size_hint_y=None,
            height=dp(90),
            text_size=(Window.width - dp(50), None),
            halign='left',
            valign='top'
        )

        # Imágenes (hasta 4) en grilla 2x2 si existen
        images = story.get('images') or []
        if images:
            grid = GridLayout(cols=2, size_hint_y=None, spacing=dp(6))
            # altura proporcional: dos filas, cada una ~100dp
            grid.bind(minimum_height=grid.setter('height'))
            for path in images[:4]:
                img = AsyncImage(source=path, allow_stretch=True, keep_ratio=True, size_hint_y=None, height=dp(100))
                grid.add_widget(img)
            self.add_widget(grid)

        if show_actions:
            actions = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))

            like_btn = Button(
                text=f"[color=#FFD700]❤️[/color] {story.get('likes', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.3, 0.2, 0.4, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True,
                font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
            )
            if self.on_like:
                like_btn.bind(on_press=lambda x: self.on_like(story))

            miedo_btn = Button(
                text=f"[color=#FF6B6B]😱[/color] {story.get('miedo', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.35, 0.15, 0.25, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True,
                font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
            )
            if self.on_reaction:
                miedo_btn.bind(on_press=lambda x: self.on_reaction(story, 'miedo'))

            sorpresa_btn = Button(
                text=f"[color=#4ECDC4]😮[/color] {story.get('sorpresa', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.25, 0.25, 0.35, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True,
                font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
            )
            if self.on_reaction:
                sorpresa_btn.bind(on_press=lambda x: self.on_reaction(story, 'sorpresa'))

            incredulidad_btn = Button(
                text=f"[color=#FFE66D]🙄[/color] {story.get('incredulidad', 0)}",
                size_hint_x=0.25,
                background_normal='',
                background_color=(0.3, 0.3, 0.25, 1),
                color=(1, 1, 1, 1),
                font_size=sp(12),
                markup=True,
                font_name='EmojiFont' if 'EmojiFont' in LabelBase._fonts else 'SegoeUIEmoji' if 'SegoeUIEmoji' in LabelBase._fonts else None
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

            self.add_widget(self.header)
            self.add_widget(self.location)
            self.add_widget(self.content)
            self.add_widget(actions)
            self.add_widget(date)
        else:
            self.add_widget(self.header)
            self.add_widget(self.location)
            self.add_widget(self.content)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


