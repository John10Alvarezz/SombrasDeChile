# -*- coding: utf-8 -*-
"""
Pruebas para funcionalidades de interacción (likes, comentarios, reacciones)
"""
import pytest
from database import Database


class TestInteractions:
    """Clase de pruebas para interacciones de usuarios"""
    
    def test_like_story_success(self, temp_db, sample_user_data, sample_story_data):
        """Prueba like exitoso a historia"""
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
        
        # Dar like
        result = temp_db.add_like(story_id, user['id'])
        assert result is True
        
        # Verificar que el like se contó
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 1
    
    def test_like_story_duplicate(self, temp_db, sample_user_data, sample_story_data):
        """Prueba like duplicado a historia"""
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
        
        # Dar like
        result1 = temp_db.add_like(story_id, user['id'])
        assert result1 is True
        
        # Intentar dar like duplicado
        result2 = temp_db.add_like(story_id, user['id'])
        assert result2 is False  # No debe permitir likes duplicados
        
        # Verificar que solo hay un like
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 1
    
    def test_multiple_users_like_story(self, temp_db, sample_story_data):
        """Prueba múltiples usuarios dando like a la misma historia"""
        # Crear múltiples usuarios
        users = []
        for i in range(3):
            username = f"usuario{i+1}"
            email = f"usuario{i+1}@example.com"
            password = "password123"
            
            temp_db.create_user(username, email, password)
            user = temp_db.login_user(username, password)
            users.append(user)
        
        # Usuario 1 crea historia
        temp_db.create_story(
            user_id=users[0]['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Todos los usuarios dan like
        for user in users:
            result = temp_db.add_like(story_id, user['id'])
            assert result is True
        
        # Verificar que se contaron todos los likes
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 3
    
    def test_comment_story_success(self, temp_db, sample_user_data, sample_story_data, sample_comment_data):
        """Prueba comentario exitoso a historia"""
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
    
    def test_multiple_comments_story(self, temp_db, sample_story_data):
        """Prueba múltiples comentarios en una historia"""
        # Crear múltiples usuarios
        users = []
        for i in range(3):
            username = f"usuario{i+1}"
            email = f"usuario{i+1}@example.com"
            password = "password123"
            
            temp_db.create_user(username, email, password)
            user = temp_db.login_user(username, password)
            users.append(user)
        
        # Usuario 1 crea historia
        temp_db.create_story(
            user_id=users[0]['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Todos los usuarios comentan
        for i, user in enumerate(users):
            comment_content = f"Comentario del usuario {i+1}"
            result = temp_db.add_comment(story_id, user['id'], comment_content)
            assert result is True
        
        # Verificar que se guardaron todos los comentarios
        comments = temp_db.get_comments(story_id)
        assert len(comments) == 3
        
        # Verificar que los comentarios son diferentes
        comment_contents = [comment['content'] for comment in comments]
        assert len(set(comment_contents)) == 3  # Todos deben ser únicos
    
    def test_reaction_miedo_success(self, temp_db, sample_user_data, sample_story_data):
        """Prueba reacción de miedo exitosa"""
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
        
        # Agregar reacción de miedo
        result = temp_db.add_reaction(story_id, user['id'], 'miedo')
        assert result is True
        
        # Verificar que la reacción se contó
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['miedo'] == 1
    
    def test_reaction_sorpresa_success(self, temp_db, sample_user_data, sample_story_data):
        """Prueba reacción de sorpresa exitosa"""
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
        
        # Agregar reacción de sorpresa
        result = temp_db.add_reaction(story_id, user['id'], 'sorpresa')
        assert result is True
        
        # Verificar que la reacción se contó
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['sorpresa'] == 1
    
    def test_reaction_incredulidad_success(self, temp_db, sample_user_data, sample_story_data):
        """Prueba reacción de incredulidad exitosa"""
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
        
        # Agregar reacción de incredulidad
        result = temp_db.add_reaction(story_id, user['id'], 'incredulidad')
        assert result is True
        
        # Verificar que la reacción se contó
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['incredulidad'] == 1
    
    def test_reaction_duplicate(self, temp_db, sample_user_data, sample_story_data):
        """Prueba reacción duplicada"""
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
        
        # Agregar reacción
        result1 = temp_db.add_reaction(story_id, user['id'], 'miedo')
        assert result1 is True
        
        # Intentar agregar reacción duplicada
        result2 = temp_db.add_reaction(story_id, user['id'], 'miedo')
        assert result2 is False  # No debe permitir reacciones duplicadas
        
        # Verificar que solo hay una reacción
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['miedo'] == 1
    
    def test_multiple_reactions_same_story(self, temp_db, sample_user_data, sample_story_data):
        """Prueba múltiples tipos de reacciones en la misma historia"""
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
        
        # Agregar diferentes tipos de reacciones
        reaction_types = ['miedo', 'sorpresa', 'incredulidad']
        for reaction_type in reaction_types:
            result = temp_db.add_reaction(story_id, user['id'], reaction_type)
            assert result is True
        
        # Verificar que todas las reacciones se contaron
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['miedo'] == 1
        assert stories[0]['sorpresa'] == 1
        assert stories[0]['incredulidad'] == 1
    
    def test_interaction_notifications(self, temp_db, sample_story_data):
        """Prueba que las interacciones generan notificaciones"""
        # Crear dos usuarios
        temp_db.create_user("autor", "autor@example.com", "password123")
        autor = temp_db.login_user("autor", "password123")
        
        temp_db.create_user("interactor", "interactor@example.com", "password123")
        interactor = temp_db.login_user("interactor", "password123")
        
        # Autor crea historia
        temp_db.create_story(
            user_id=autor['id'],
            content=sample_story_data['content'],
            location=sample_story_data['location'],
            category=sample_story_data['category']
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Interactor da like
        temp_db.add_like(story_id, interactor['id'])
        
        # Interactor comenta
        temp_db.add_comment(story_id, interactor['id'], "Comentario de prueba")
        
        # Interactor reacciona
        temp_db.add_reaction(story_id, interactor['id'], 'miedo')
        
        # Verificar notificaciones del autor
        notifications = temp_db.get_user_notifications(autor['id'])
        assert len(notifications) == 3  # Like, comentario y reacción
        
        # Verificar tipos de notificaciones
        notification_types = [n['tipo'] for n in notifications]
        assert 'like' in notification_types
        assert 'comment' in notification_types
        assert 'reaction' in notification_types
    
    def test_empty_comment(self, temp_db, sample_user_data, sample_story_data):
        """Prueba comentario vacío"""
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
        
        # Intentar agregar comentario vacío
        result = temp_db.add_comment(story_id, user['id'], "")
        # El resultado depende de la implementación, pero no debe crashear
        assert result is not None
    
    def test_long_comment(self, temp_db, sample_user_data, sample_story_data):
        """Prueba comentario muy largo"""
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
        
        # Comentario muy largo
        long_comment = "a" * 10000  # 10,000 caracteres
        
        result = temp_db.add_comment(story_id, user['id'], long_comment)
        # Debería manejar correctamente comentarios largos
        assert result is not None
