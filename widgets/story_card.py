from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp
import os

try:
    from PIL import Image, ImageDraw
    HAS_PIL = True
except Exception:
    HAS_PIL = False


def _emoji_font():
    try:
        from kivy.core.text import LabelBase
        # Prefer the registered 'EmojiFont', otherwise try common names
        for name in ('EmojiFont', 'SegoeUIEmoji', 'Segoe UI Emoji'):
            if name in getattr(LabelBase, '_fonts', {}):
                return name
        # try to register common Windows emoji font paths if available
        potential = [r"C:\\Windows\\Fonts\\seguiemj.ttf", r"C:\\Windows\\Fonts\\SegoeUIEmoji.ttf"]
        for p in potential:
            if os.path.exists(p):
                try:
                    LabelBase.register(name='SegoeUIEmoji', fn_regular=p)
                    return 'SegoeUIEmoji'
                except Exception:
                    continue
    except Exception:
        pass
    return None


class StoryCard(BoxLayout):
    def __init__(self, story, on_like=None, on_reaction=None, on_comment=None, show_actions=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.spacing = dp(8)
        self.padding = [dp(12), dp(12)]
        self.story = story
        self.on_like = on_like
        self.on_reaction = on_reaction
        self.on_comment = on_comment

        with self.canvas.before:
            Color(0.12, 0.12, 0.17, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        self.bind(pos=self.update_bg, size=self.update_bg)

        # Header (avatar + username + category)
        self.header = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8), padding=[0, dp(4)])

        # Left: avatar + name stack
        avatar_size = dp(40)
        avatar_path = story.get('user_avatar') or ''
        # If no avatar provided, ensure a default avatar image exists and use it
        if not avatar_path:
            # location for default avatar inside project media folder
            default_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))
            os.makedirs(default_dir, exist_ok=True)
            default_avatar = os.path.join(default_dir, 'default_avatar.png')
            if not os.path.exists(default_avatar) and HAS_PIL:
                # generate a simple circular default avatar similar to provided image
                size = 256
                img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                # white circle with dark border
                draw.ellipse((8, 8, size-8, size-8), fill=(255,255,255,255), outline=(30,30,30,255), width=12)
                # head (dark circle)
                hx = size*0.5
                hy = size*0.36
                hr = size*0.16
                draw.ellipse((hx-hr, hy-hr, hx+hr, hy+hr), fill=(30,30,30,255))
                # shoulders (ellipse)
                sx1 = size*0.18
                sy1 = size*0.58
                sx2 = size*0.82
                sy2 = size*0.88
                draw.ellipse((sx1, sy1, sx2, sy2), fill=(30,30,30,255))
                img.save(default_avatar)
            avatar_path = default_avatar if os.path.exists(default_avatar) else ''

        avatar = AsyncImage(source=avatar_path, size_hint=(None, None), size=(avatar_size, avatar_size), fit_mode='contain')

        name_box = BoxLayout(orientation='vertical', size_hint_x=0.7, padding=[0,0])
        username_text = story.get('username', 'Anónimo') if not story.get('is_anonymous') else 'Anónimo'
        username = Label(
            text=username_text,
            font_size=sp(14),
            bold=True,
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(20),
            text_size=(None, None)
        )
        username.bind(texture_size=lambda i, v: setattr(username, 'height', max(dp(18), v[1])))

        subtitle = story.get('role') or ''
        subtitle_label = Label(
            text=subtitle,
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(16)
        )
        subtitle_label.bind(texture_size=lambda i, v: setattr(subtitle_label, 'height', max(dp(14), v[1])))

        name_box.add_widget(username)
        name_box.add_widget(subtitle_label)

        # Right: category
        category = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('category', 'Aparición')}",
            font_size=sp(11),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_x=0.3,
            halign='right',
            valign='middle',
            markup=True,
            font_name=_emoji_font()
        )
        category.bind(texture_size=lambda i, v: setattr(category, 'height', v[1]))

        # Assemble header: avatar, name_box, category
        self.header.add_widget(avatar)
        self.header.add_widget(name_box)
        self.header.add_widget(category)

        # Location
        self.location = Label(
            text=f"[color=#FFD700]📍[/color] {story.get('location', 'Sin ubicación')}",
            font_size=sp(12),
            color=(0.6, 0.6, 0.7, 1),
            size_hint_y=None,
            halign='left',
            valign='middle',
            markup=True,
            font_name=_emoji_font()
        )
        self.location.bind(texture_size=lambda i, v: setattr(self.location, 'height', max(dp(20), v[1])))

        # Content: wrap text and update height based on texture_size
        content_text = story.get('content', '')
        # Limit length for preview but keep wrapping
        if len(content_text) > 500:
            content_text = content_text[:500] + '...'

        self.content = Label(
            text=content_text,
            font_size=sp(13),
            color=(0.85, 0.85, 0.85, 1),
            size_hint_y=None,
            halign='left',
            valign='top'
        )

        # Bind content width to card width (respecting padding) so text wraps correctly
        def _update_text_size(instance, value):
            padding_x = self.padding[0] * 2 if isinstance(self.padding, (list, tuple)) else self.padding * 2
            w = max(20, self.width - padding_x)
            instance.text_size = (w, None)
            # Force update of texture and height
            instance.texture_update()
            instance.height = instance.texture_size[1]

        self.bind(width=lambda i, v: _update_text_size(self.content, v))
        # Initialize size
        _update_text_size(self.content, self.width)

        # Images (up to 4) - place after content
        images = story.get('images') or []
        images_widget = None
        if images:
            cols = 2 if len(images) > 1 else 1
            grid = GridLayout(cols=cols, size_hint_y=None, spacing=dp(6))
            # each image height fixed but proportional to available width
            def _update_grid_width(inst, val):
                # compute image width per column
                padding_x = self.padding[0] * 2 if isinstance(self.padding, (list, tuple)) else self.padding * 2
                available = max(50, self.width - padding_x - (grid.spacing[0] * (cols - 1)))
                img_w = available / cols
                # set image height to maintain reasonable aspect (square-ish preview)
                for child in grid.children:
                    child.width = img_w
                    child.height = img_w * 0.66
                grid.height = (len(grid.children) + cols - 1) // cols * (img_w * 0.66 + grid.spacing[1])

            for path in images[:4]:
                img = AsyncImage(source=path, fit_mode='contain', size_hint=(None, None))
                grid.add_widget(img)
            grid.bind(minimum_height=grid.setter('height'))
            self.bind(width=_update_grid_width)
            # call once to set sizes
            _update_grid_width(grid, self.width)
            images_widget = grid

        # Actions and date
        actions = None
        if show_actions:
            actions = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            # Buttons: use flexible size_hint_x so they adapt
            like_btn = Button(text=f"[color=#FFD700]❤️[/color] {story.get('likes', 0)}", size_hint_x=0.25, background_normal='', background_color=(0.3, 0.2, 0.4, 1), color=(1,1,1,1), font_size=sp(12), markup=True, font_name=_emoji_font())
            if self.on_like:
                like_btn.bind(on_press=lambda x: self.on_like(story))
            comment_btn = Button(text=f"[color=#4ECDC4]💬[/color] Comentar", size_hint_x=0.25, background_normal='', background_color=(0.2,0.3,0.4,1), color=(1,1,1,1), font_size=sp(10), markup=True, font_name=_emoji_font())
            if self.on_comment:
                comment_btn.bind(on_press=lambda x: self.on_comment(story))
            miedo_btn = Button(text=f"[color=#FF6B6B]😱[/color] {story.get('miedo',0)}", size_hint_x=0.25, background_normal='', background_color=(0.35,0.15,0.25,1), color=(1,1,1,1), font_size=sp(12), markup=True, font_name=_emoji_font())
            if self.on_reaction:
                miedo_btn.bind(on_press=lambda x: self.on_reaction(story, 'miedo'))
            sorpresa_btn = Button(text=f"[color=#4ECDC4]😮[/color] {story.get('sorpresa',0)}", size_hint_x=0.25, background_normal='', background_color=(0.25,0.25,0.35,1), color=(1,1,1,1), font_size=sp(12), markup=True, font_name=_emoji_font())
            if self.on_reaction:
                sorpresa_btn.bind(on_press=lambda x: self.on_reaction(story, 'sorpresa'))
            incredulidad_btn = Button(text=f"[color=#FFE66D]🙄[/color] {story.get('incredulidad',0)}", size_hint_x=0.25, background_normal='', background_color=(0.3,0.3,0.25,1), color=(1,1,1,1), font_size=sp(12), markup=True, font_name=_emoji_font())
            if self.on_reaction:
                incredulidad_btn.bind(on_press=lambda x: self.on_reaction(story, 'incredulidad'))
            actions.add_widget(like_btn)
            actions.add_widget(comment_btn)
            actions.add_widget(miedo_btn)
            actions.add_widget(sorpresa_btn)
            actions.add_widget(incredulidad_btn)

        date = Label(text=story.get('created_at',''), font_size=sp(10), color=(0.5,0.5,0.5,1), size_hint_y=None, height=dp(18), halign='right', valign='middle')
        date.bind(texture_size=lambda i, v: setattr(date, 'height', max(dp(16), v[1])))

        # Add widgets in the correct order
        self.add_widget(self.header)
        self.add_widget(self.location)
        self.add_widget(self.content)
        if images_widget:
            self.add_widget(images_widget)
        if actions:
            self.add_widget(actions)
        self.add_widget(date)

        # Recalculate overall height based on children
        def _recalc_height(*a):
            total = 0
            for child in self.children[:]:
                # children list is reverse order for BoxLayout; compute using child.height
                h = getattr(child, 'height', 0) or 0
                total += h
            total += self.spacing * (len(self.children) - 1)
            padding_y = (self.padding[1] * 2) if isinstance(self.padding, (list, tuple)) else self.padding * 2
            self.height = total + padding_y

        # Bind changes that affect height
        self.bind(children=lambda *x: _recalc_height())
        for w in (self.header, self.location, self.content, images_widget, actions, date):
            if w is not None:
                w.bind(height=lambda *a: _recalc_height())

        # initial calc
        _recalc_height()

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


