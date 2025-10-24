# -*- coding: utf-8 -*-
"""
Pruebas para funcionalidades de gestión de historias
"""
import pytest
from database import Database


class TestStoryManagement:
    """Clase de pruebas para gestión de historias"""
    
    def test_create_story_success(self, temp_db, sample_user_data, sample_story_data):
        """Prueba creación exitosa de historia"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historia
        result = temp_db.create_story(
            user_id=user['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category'],
            is_anonymous=sample_story_data['is_anonymous']
        )
        assert result is True
        
        # Verificar que la historia se creó
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 1
        assert stories[0]['content'] == sample_story_data['content']
        assert stories[0]['location'] == sample_story_data['location']
        assert stories[0]['category'] == sample_story_data['category']
        assert stories[0]['username'] == sample_user_data['username']
    
    def test_create_anonymous_story(self, temp_db, sample_user_data):
        """Prueba creación de historia anónima"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historia anónima
        result = temp_db.create_story(
            user_id=user['id'],
            content="Historia anónima de prueba",
            location="Ubicación anónima",
            category="Aparición",
            is_anonymous=True
        )
        assert result is True
        
        # Verificar que la historia se creó como anónima
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 1
        assert stories[0]['is_anonymous'] == 1
    
    def test_get_user_stories(self, temp_db, sample_user_data):
        """Prueba obtención de historias de usuario"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear múltiples historias
        stories_data = [
            {'content': 'Historia 1', 'location': 'Lugar 1', 'category': 'Aparición'},
            {'content': 'Historia 2', 'location': 'Lugar 2', 'category': 'Fantasma'},
            {'content': 'Historia 3', 'location': 'Lugar 3', 'category': 'OVNI'}
        ]
        
        for story_data in stories_data:
            temp_db.create_story(
                user_id=user['id'],
                content=story_data['content'],
                location=story_data['location'],
                category=story_data['category']
            )
        
        # Obtener historias del usuario
        user_stories = temp_db.get_user_stories(user['id'])
        assert len(user_stories) == 3
        
        # Verificar que todas las historias pertenecen al usuario
        for story in user_stories:
            assert story['user_id'] == user['id']
    
    def test_story_pagination(self, temp_db, sample_user_data):
        """Prueba paginación de historias"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear 5 historias
        for i in range(5):
            temp_db.create_story(
                user_id=user['id'],
                content=f"Historia {i+1}",
                location=f"Lugar {i+1}",
                category="Aparición"
            )
        
        # Probar paginación
        page1 = temp_db.get_all_stories(limit=2, offset=0)
        assert len(page1) == 2
        
        page2 = temp_db.get_all_stories(limit=2, offset=2)
        assert len(page2) == 2
        
        page3 = temp_db.get_all_stories(limit=2, offset=4)
        assert len(page3) == 1
        
        # Verificar que las historias son diferentes
        page1_ids = [story['id'] for story in page1]
        page2_ids = [story['id'] for story in page2]
        page3_ids = [story['id'] for story in page3]
        
        assert not set(page1_ids).intersection(set(page2_ids))
        assert not set(page2_ids).intersection(set(page3_ids))
        assert not set(page1_ids).intersection(set(page3_ids))
    
    def test_story_search_by_content(self, temp_db, sample_user_data):
        """Prueba búsqueda de historias por contenido"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historias con contenido específico
        stories_data = [
            {'content': 'Historia sobre fantasmas en Valparaíso', 'location': 'Valparaíso', 'category': 'Fantasma'},
            {'content': 'Aparición en Santiago', 'location': 'Santiago', 'category': 'Aparición'},
            {'content': 'OVNI avistado en el norte', 'location': 'Antofagasta', 'category': 'OVNI'}
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
        
        results = temp_db.search_stories('aparición')
        assert len(results) == 1
        assert 'aparición' in results[0]['content'].lower()
    
    def test_story_search_by_location(self, temp_db, sample_user_data):
        """Prueba búsqueda de historias por ubicación"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historias en diferentes ubicaciones
        stories_data = [
            {'content': 'Historia 1', 'location': 'Santiago, Chile', 'category': 'Aparición'},
            {'content': 'Historia 2', 'location': 'Valparaíso, Chile', 'category': 'Fantasma'},
            {'content': 'Historia 3', 'location': 'Concepción, Chile', 'category': 'OVNI'}
        ]
        
        for story_data in stories_data:
            temp_db.create_story(
                user_id=user['id'],
                content=story_data['content'],
                location=story_data['location'],
                category=story_data['category']
            )
        
        # Buscar por ubicación
        results = temp_db.search_stories('Santiago')
        assert len(results) == 1
        assert 'Santiago' in results[0]['location']
        
        results = temp_db.search_stories('Valparaíso')
        assert len(results) == 1
        assert 'Valparaíso' in results[0]['location']
    
    def test_story_search_by_category(self, temp_db, sample_user_data):
        """Prueba búsqueda de historias por categoría"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historias con diferentes categorías
        stories_data = [
            {'content': 'Historia 1', 'location': 'Lugar 1', 'category': 'Aparición'},
            {'content': 'Historia 2', 'location': 'Lugar 2', 'category': 'Fantasma'},
            {'content': 'Historia 3', 'location': 'Lugar 3', 'category': 'OVNI'},
            {'content': 'Historia 4', 'location': 'Lugar 4', 'category': 'Leyenda'}
        ]
        
        for story_data in stories_data:
            temp_db.create_story(
                user_id=user['id'],
                content=story_data['content'],
                location=story_data['location'],
                category=story_data['category']
            )
        
        # Buscar por categoría
        results = temp_db.search_stories('Aparición')
        assert len(results) == 1
        assert results[0]['category'] == 'Aparición'
        
        results = temp_db.search_stories('Fantasma')
        assert len(results) == 1
        assert results[0]['category'] == 'Fantasma'
    
    def test_story_update(self, temp_db, sample_user_data, sample_story_data):
        """Prueba actualización de historia"""
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
    
    def test_story_update_unauthorized(self, temp_db, sample_user_data, sample_story_data):
        """Prueba actualización de historia por usuario no autorizado"""
        # Crear dos usuarios
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user1 = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_user("usuario2", "usuario2@example.com", "password123")
        user2 = temp_db.login_user("usuario2", "password123")
        
        # Usuario 1 crea historia
        temp_db.create_story(
            user_id=user1['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Usuario 2 intenta actualizar historia de usuario 1
        result = temp_db.update_story(
            story_id=story_id,
            user_id=user2['id'],
            content="Contenido malicioso",
            location="Ubicación maliciosa",
            category="Categoría maliciosa"
        )
        assert result is False  # No debe permitir actualización
    
    def test_story_delete(self, temp_db, sample_user_data, sample_story_data):
        """Prueba eliminación de historia"""
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
        
        # Eliminar historia
        result = temp_db.delete_story(story_id, user['id'])
        assert result is True
        
        # Verificar eliminación
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 0
    
    def test_story_delete_unauthorized(self, temp_db, sample_user_data, sample_story_data):
        """Prueba eliminación de historia por usuario no autorizado"""
        # Crear dos usuarios
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user1 = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        temp_db.create_user("usuario2", "usuario2@example.com", "password123")
        user2 = temp_db.login_user("usuario2", "password123")
        
        # Usuario 1 crea historia
        temp_db.create_story(
            user_id=user1['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Usuario 2 intenta eliminar historia de usuario 1
        result = temp_db.delete_story(story_id, user2['id'])
        assert result is False  # No debe permitir eliminación
        
        # Verificar que la historia sigue existiendo
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 1
    
    def test_story_with_images(self, temp_db, sample_user_data):
        """Prueba creación de historia con imágenes"""
        # Crear usuario
        temp_db.create_user(
            sample_user_data['username'],
            sample_user_data['email'],
            sample_user_data['password']
        )
        user = temp_db.login_user(sample_user_data['username'], sample_user_data['password'])
        
        # Crear historia
        temp_db.create_story(
            user_id=user['id'],
            content="Historia con imágenes",
            location="Lugar con imágenes",
            category="Aparición"
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Agregar imágenes
        image_paths = [
            "media/imagen1.jpg",
            "media/imagen2.jpg",
            "media/imagen3.jpg"
        ]
        
        result = temp_db.add_story_images(story_id, image_paths)
        assert result is True
        
        # Verificar que las imágenes se guardaron
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert len(stories[0]['images']) == 3
        assert stories[0]['images'] == image_paths
