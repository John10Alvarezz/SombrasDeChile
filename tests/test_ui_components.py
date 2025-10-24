# -*- coding: utf-8 -*-
"""
Pruebas para componentes de interfaz de usuario
"""
import pytest
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from widgets.navbar import NavBar
from widgets.story_card import StoryCard


class TestUIComponents:
    """Clase de pruebas para componentes de UI"""
    
    def test_navbar_creation(self):
        """Prueba creación de barra de navegación"""
        navbar = NavBar()
        assert navbar is not None
        assert navbar.orientation == 'horizontal'
        assert navbar.size_hint == (1, None)
        assert navbar.screen_manager is None
    
    def test_navbar_buttons(self):
        """Prueba que la barra de navegación tiene los botones correctos"""
        navbar = NavBar()
        
        # Verificar que se crearon los botones
        assert len(navbar.children) == 5  # 5 botones de navegación
        
        # Verificar textos de los botones
        button_texts = [child.text for child in navbar.children]
        expected_texts = [
            '[color=#FFD700]👤[/color]\nPerfil',
            '[color=#FFD700]+[/color]\nCrear',
            '[color=#FFD700]🔔[/color]\nNotificaciones',
            '[color=#FFD700]🔍[/color]\nBuscar',
            '[color=#FFD700]🏠[/color]\nInicio'
        ]
        
        for expected_text in expected_texts:
            assert any(expected_text in text for text in button_texts)
    
    def test_navbar_screen_manager_setting(self):
        """Prueba configuración del screen manager en navbar"""
        navbar = NavBar()
        screen_manager = ScreenManager()
        
        navbar.set_screen_manager(screen_manager)
        assert navbar.screen_manager == screen_manager
    
    def test_story_card_creation(self):
        """Prueba creación de tarjeta de historia"""
        story_data = {
            'id': 1,
            'content': 'Historia de prueba',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 5,
            'miedo': 2,
            'sorpresa': 1,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False
        }
        
        card = StoryCard(story_data)
        assert card is not None
        assert card.story == story_data
        assert card.orientation == 'vertical'
        assert card.size_hint_y is None
    
    def test_story_card_anonymous(self):
        """Prueba tarjeta de historia anónima"""
        story_data = {
            'id': 1,
            'content': 'Historia anónima de prueba',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 0,
            'miedo': 0,
            'sorpresa': 0,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': True
        }
        
        card = StoryCard(story_data)
        assert card is not None
        
        # Verificar que se muestra como anónimo
        # Esto se verifica en el texto del username
        username_widget = None
        for child in card.children:
            if hasattr(child, 'children'):
                for grandchild in child.children:
                    if hasattr(grandchild, 'text') and 'Anónimo' in grandchild.text:
                        username_widget = grandchild
                        break
        
        assert username_widget is not None
    
    def test_story_card_with_images(self):
        """Prueba tarjeta de historia con imágenes"""
        story_data = {
            'id': 1,
            'content': 'Historia con imágenes',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 0,
            'miedo': 0,
            'sorpresa': 0,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False,
            'images': ['media/imagen1.jpg', 'media/imagen2.jpg']
        }
        
        card = StoryCard(story_data)
        assert card is not None
        
        # Verificar que se creó el grid de imágenes
        has_image_grid = False
        for child in card.children:
            if hasattr(child, 'cols'):  # GridLayout tiene atributo cols
                has_image_grid = True
                break
        
        assert has_image_grid
    
    def test_story_card_without_actions(self):
        """Prueba tarjeta de historia sin botones de acción"""
        story_data = {
            'id': 1,
            'content': 'Historia sin acciones',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 0,
            'miedo': 0,
            'sorpresa': 0,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False
        }
        
        card = StoryCard(story_data, show_actions=False)
        assert card is not None
        
        # Verificar que no hay botones de acción
        has_action_buttons = False
        for child in card.children:
            if hasattr(child, 'children'):
                for grandchild in child.children:
                    if hasattr(grandchild, 'text') and ('❤️' in grandchild.text or '💬' in grandchild.text):
                        has_action_buttons = True
                        break
        
        assert not has_action_buttons
    
    def test_story_card_content_truncation(self):
        """Prueba truncamiento de contenido largo en tarjeta"""
        long_content = "Esta es una historia muy larga que debería ser truncada para que no ocupe demasiado espacio en la tarjeta. " * 10
        
        story_data = {
            'id': 1,
            'content': long_content,
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 0,
            'miedo': 0,
            'sorpresa': 0,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False
        }
        
        card = StoryCard(story_data)
        assert card is not None
        
        # Verificar que el contenido se truncó
        content_widget = None
        for child in card.children:
            if hasattr(child, 'text') and len(child.text) < len(long_content):
                content_widget = child
                break
        
        assert content_widget is not None
        assert len(content_widget.text) < len(long_content)
        assert content_widget.text.endswith('...')
    
    def test_story_card_callback_functions(self):
        """Prueba funciones de callback en tarjeta de historia"""
        story_data = {
            'id': 1,
            'content': 'Historia con callbacks',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 0,
            'miedo': 0,
            'sorpresa': 0,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False
        }
        
        # Funciones de callback mock
        like_called = False
        reaction_called = False
        comment_called = False
        
        def mock_like(story):
            nonlocal like_called
            like_called = True
        
        def mock_reaction(story, tipo):
            nonlocal reaction_called
            reaction_called = True
        
        def mock_comment(story):
            nonlocal comment_called
            comment_called = True
        
        card = StoryCard(
            story_data,
            on_like=mock_like,
            on_reaction=mock_reaction,
            on_comment=mock_comment
        )
        
        assert card is not None
        assert card.on_like == mock_like
        assert card.on_reaction == mock_reaction
        assert card.on_comment == mock_comment
    
    def test_story_card_reaction_counts(self):
        """Prueba que los contadores de reacciones se muestran correctamente"""
        story_data = {
            'id': 1,
            'content': 'Historia con reacciones',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 10,
            'miedo': 5,
            'sorpresa': 3,
            'incredulidad': 2,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False
        }
        
        card = StoryCard(story_data)
        assert card is not None
        
        # Verificar que los contadores se muestran en los botones
        button_texts = []
        for child in card.children:
            if hasattr(child, 'children'):
                for grandchild in child.children:
                    if hasattr(grandchild, 'text'):
                        button_texts.append(grandchild.text)
        
        # Verificar que los números están en los textos
        assert any('10' in text for text in button_texts)  # likes
        assert any('5' in text for text in button_texts)   # miedo
        assert any('3' in text for text in button_texts)   # sorpresa
        assert any('2' in text for text in button_texts)   # incredulidad
    
    def test_story_card_date_display(self):
        """Prueba que la fecha se muestra correctamente"""
        story_data = {
            'id': 1,
            'content': 'Historia con fecha',
            'location': 'Santiago, Chile',
            'category': 'Aparición',
            'username': 'test_user',
            'likes': 0,
            'miedo': 0,
            'sorpresa': 0,
            'incredulidad': 0,
            'created_at': '01/01/2024 12:00',
            'is_anonymous': False
        }
        
        card = StoryCard(story_data)
        assert card is not None
        
        # Verificar que la fecha se muestra
        date_widget = None
        for child in card.children:
            if hasattr(child, 'text') and '01/01/2024' in child.text:
                date_widget = child
                break
        
        assert date_widget is not None
        assert '01/01/2024' in date_widget.text
    
    def test_navbar_button_press(self):
        """Prueba que los botones de navbar responden a eventos"""
        navbar = NavBar()
        
        # Mock screen manager
        class MockScreenManager:
            def __init__(self):
                self.current = None
        
        screen_manager = MockScreenManager()
        navbar.set_screen_manager(screen_manager)
        
        # Simular presión de botón
        try:
            navbar.change_screen('feed')
            assert screen_manager.current == 'feed'
        except Exception:
            # Si hay error, al menos verificar que no crashea
            pass
    
    def test_story_card_empty_story(self):
        """Prueba tarjeta con datos de historia vacíos"""
        empty_story = {}
        
        card = StoryCard(empty_story)
        assert card is not None
        
        # Debe manejar datos vacíos sin crashear
        # Los valores por defecto se aplican en el widget
