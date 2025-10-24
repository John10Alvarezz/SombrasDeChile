# -*- coding: utf-8 -*-
"""
Pruebas unitarias para la clase Database
"""
import pytest
from database import Database


class TestDatabase:
    """Clase de pruebas para la funcionalidad de base de datos"""
    
    def test_database_initialization(self, temp_db):
        """Prueba que la base de datos se inicializa correctamente"""
        assert temp_db is not None
        assert temp_db.db_name is not None
        
        # Verificar que las tablas se crearon
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        
        # Verificar existencia de tablas principales
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['usuarios', 'historias', 'likes', 'comentarios', 'reacciones', 'story_images', 'reportes', 'notificaciones']
        for table in expected_tables:
            assert table in tables
        
        conn.close()
    
    def test_user_creation(self, temp_db, sample_user_data):
        """Prueba la creación de usuarios"""
        # Crear usuario exitosamente
        result = temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        assert result is True
        
        # Intentar crear usuario duplicado
        result = temp_db.create_user(
            sample_user_data['username'],
            'otro@example.com',
            'password123'
        )
        assert result is False  # Debe fallar por username duplicado
        
        result = temp_db.create_user(
            'otro_usuario',
            sample_user_data['email'],
            'password123'
        )
        assert result is False  # Debe fallar por email duplicado
    
    def test_user_login(self, temp_db, sample_user_data):
        """Prueba el login de usuarios"""
        # Crear usuario primero
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        
        # Login exitoso
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        assert user is not None
        assert user['username'] == sample_user_data['username']
        assert user['email'] == sample_user_data['email']
        
        # Login con credenciales incorrectas
        user = temp_db.login_user(sample_user_data['username'], 'password_incorrecta')
        assert user is None
        
        user = temp_db.login_user('usuario_inexistente', sample_user_data['password'])
        assert user is None
    
    def test_story_creation(self, temp_db, sample_user_data, sample_story_data):
        """Prueba la creación de historias"""
        # Crear usuario primero
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historia exitosamente
        result = temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category'],
            is_anonymous=sample_story_data['is_anonymous']
        )
        assert result is True
        
        # Verificar que la historia se guardó
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 1
        assert stories[0]['content'] == sample_story_data['content']
        assert stories[0]['location'] == sample_story_data['location']
        assert stories[0]['category'] == sample_story_data['category']
    
    def test_story_search(self, temp_db, sample_user_data):
        """Prueba la búsqueda de historias"""
        # Crear usuario y historias
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear múltiples historias
        stories_data = [
            {'content': 'Historia sobre fantasmas en Valparaíso', 'location': 'Valparaíso', 'category': 'Fantasma'},
            {'content': 'OVNI avistado en Santiago', 'location': 'Santiago', 'category': 'OVNI'},
            {'content': 'Leyenda del Caleuche en Chiloé', 'location': 'Chiloé', 'category': 'Leyenda'}
        ]
        
        for story_data in stories_data:
            temp_db.create_story(
                user_id=user['id'],
                content=story_data['content'],
                location=story_data['location'],
                category=story_data['category']
            )
        
        # Buscar por contenido
        results = temp_db.search_stories('fantasmas')
        assert len(results) == 1
        assert 'fantasmas' in results[0]['content'].lower()
        
        # Buscar por ubicación
        results = temp_db.search_stories('Santiago')
        assert len(results) == 1
        assert results[0]['location'] == 'Santiago'
        
        # Buscar por categoría
        results = temp_db.search_stories('OVNI')
        assert len(results) == 1
        assert results[0]['category'] == 'OVNI'
    
    def test_like_functionality(self, temp_db, sample_user_data, sample_story_data):
        """Prueba la funcionalidad de likes"""
        # Crear usuario y historia
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Agregar like
        result = temp_db.add_like(story_id, user['id'])
        assert result is True
        
        # Intentar agregar like duplicado
        result = temp_db.add_like(story_id, user['id'])
        assert result is False  # No debe permitir likes duplicados
        
        # Verificar que el like se contó
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 1
    
    def test_comment_functionality(self, temp_db, sample_user_data, sample_story_data, sample_comment_data):
        """Prueba la funcionalidad de comentarios"""
        # Crear usuario y historia
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Agregar comentario
        result = temp_db.add_comment(story_id, user['id'], sample_comment_data['content'])
        assert result is True
        
        # Verificar que el comentario se guardó
        comments = temp_db.get_comments(story_id)
        assert len(comments) == 1
        assert comments[0]['content'] == sample_comment_data['content']
        assert comments[0]['username'] == sample_user_data['username']
    
    def test_reaction_functionality(self, temp_db, sample_user_data, sample_story_data):
        """Prueba la funcionalidad de reacciones"""
        # Crear usuario y historia
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Agregar reacciones
        reaction_types = ['miedo', 'sorpresa', 'incredulidad']
        for reaction_type in reaction_types:
            result = temp_db.add_reaction(story_id, user['id'], reaction_type)
            assert result is True
        
        # Verificar contadores de reacciones
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story = stories[0]
        assert story['miedo'] == 1
        assert story['sorpresa'] == 1
        assert story['incredulidad'] == 1
    
    def test_story_update_and_delete(self, temp_db, sample_user_data, sample_story_data):
        """Prueba la actualización y eliminación de historias"""
        # Crear usuario y historia
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Actualizar historia
        new_content = "Contenido actualizado de la historia"
        new_location = "Nueva ubicación"
        new_category = "Fantasma"
        
        result = temp_db.update_story(
            story_id=story_id,
            user_id=user['id'],
            content=new_content,
            location=new_location,
            category=new_category,
            is_anonymous=True
        )
        assert result is True
        
        # Verificar actualización
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['content'] == new_content
        assert stories[0]['location'] == new_location
        assert stories[0]['category'] == new_category
        assert stories[0]['is_anonymous'] == 1
        
        # Eliminar historia
        result = temp_db.delete_story(story_id, user['id'])
        assert result is True
        
        # Verificar eliminación
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 0
    
    def test_report_functionality(self, temp_db, sample_user_data, sample_story_data):
        """Prueba la funcionalidad de reportes"""
        # Crear usuario y historia
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Crear reporte
        result = temp_db.create_report(
            story_id=story_id,
            reporter_id=user['id'],
            motivo='Contenido inapropiado',
            descripcion='Este contenido no es apropiado'
        )
        assert result is True
        
        # Intentar crear reporte duplicado
        result = temp_db.create_report(
            story_id=story_id,
            reporter_id=user['id'],
            motivo='Spam',
            descripcion='Otro motivo'
        )
        assert result is False  # No debe permitir reportes duplicados
        
        # Verificar reporte
        reports = temp_db.get_reports()
        assert len(reports) == 1
        assert reports[0]['motivo'] == 'Contenido inapropiado'
        assert reports[0]['descripcion'] == 'Este contenido no es apropiado'
    
    def test_notification_functionality(self, temp_db, sample_user_data):
        """Prueba la funcionalidad de notificaciones"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear notificación
        result = temp_db.create_notification(
            user_id=user['id'],
            tipo='like',
            titulo='Nuevo like',
            mensaje='Alguien le dio like a tu historia',
            story_id=1
        )
        assert result is True
        
        # Obtener notificaciones
        notifications = temp_db.get_user_notifications(user['id'])
        assert len(notifications) == 1
        assert notifications[0]['tipo'] == 'like'
        assert notifications[0]['titulo'] == 'Nuevo like'
        
        # Marcar como leída
        notification_id = notifications[0]['id']
        result = temp_db.mark_notification_as_read(notification_id, user['id'])
        assert result is True
        
        # Marcar todas como leídas
        result = temp_db.mark_all_notifications_as_read(user['id'])
        assert result is True
