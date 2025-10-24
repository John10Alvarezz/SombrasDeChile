# -*- coding: utf-8 -*-
"""
Pruebas de integración para el sistema completo
"""
import pytest
from database import Database


class TestIntegration:
    """Clase de pruebas de integración para el sistema completo"""
    
    def test_complete_user_workflow(self, temp_db):
        """Prueba flujo completo de usuario: registro, login, crear historia, interacciones"""
        # 1. Registro de usuario
        username = "usuario_completo"
        email = "completo@example.com"
        password = "password123"
        
        result = temp_db.create_user(username, email, password)
        assert result is True
        
        # 2. Login
        user = temp_db.login_user(username, password)
        assert user is not None
        assert user['username'] == username
        
        # 3. Crear historia
        story_content = "Esta es una historia completa de prueba"
        story_location = "Santiago, Chile"
        story_category = "Aparición"
        
        result = temp_db.create_story(
            user_id=user['id'],
            content=story_content,
            location=story_location,
            category=story_category
        )
        assert result is True
        
        # 4. Verificar que la historia se creó
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 1
        assert stories[0]['content'] == story_content
        
        # 5. Agregar interacciones
        story_id = stories[0]['id']
        
        # Like
        result = temp_db.add_like(story_id, user['id'])
        assert result is True
        
        # Comentario
        result = temp_db.add_comment(story_id, user['id'], "Comentario de prueba")
        assert result is True
        
        # Reacciones
        for reaction_type in ['miedo', 'sorpresa', 'incredulidad']:
            result = temp_db.add_reaction(story_id, user['id'], reaction_type)
            assert result is True
        
        # 6. Verificar interacciones
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 1
        assert stories[0]['miedo'] == 1
        assert stories[0]['sorpresa'] == 1
        assert stories[0]['incredulidad'] == 1
        
        comments = temp_db.get_comments(story_id)
        assert len(comments) == 1
        assert comments[0]['content'] == "Comentario de prueba"
    
    def test_multi_user_interaction(self, temp_db):
        """Prueba interacciones entre múltiples usuarios"""
        # Crear usuarios
        users = []
        for i in range(3):
            username = f"usuario{i+1}"
            email = f"usuario{i+1}@example.com"
            password = "password123"
            
            temp_db.create_user(username, email, password)
            user = temp_db.login_user(username, password)
            users.append(user)
        
        # Usuario 1 crea historia
        story_content = "Historia para interacciones múltiples"
        story_location = "Valparaíso, Chile"
        story_category = "Fantasma"
        
        temp_db.create_story(
            user_id=users[0]['id'],
            content=story_content,
            location=story_location,
            category=story_category
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Usuarios 2 y 3 interactúan con la historia
        for i, user in enumerate(users[1:], 1):
            # Like
            temp_db.add_like(story_id, user['id'])
            
            # Comentario
            temp_db.add_comment(story_id, user['id'], f"Comentario del usuario {i+1}")
            
            # Reacción
            reaction_types = ['miedo', 'sorpresa', 'incredulidad']
            temp_db.add_reaction(story_id, user['id'], reaction_types[i-1])
        
        # Verificar interacciones
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 2  # 2 usuarios dieron like
        
        comments = temp_db.get_comments(story_id)
        assert len(comments) == 2  # 2 comentarios
        
        # Verificar reacciones
        assert stories[0]['miedo'] == 1
        assert stories[0]['sorpresa'] == 1
        assert stories[0]['incredulidad'] == 0  # Solo 2 usuarios, 2 tipos de reacción
        
        # Verificar notificaciones del autor
        notifications = temp_db.get_user_notifications(users[0]['id'])
        assert len(notifications) >= 4  # Al menos 4 notificaciones (2 likes, 2 comentarios, 2 reacciones)
    
    def test_story_lifecycle(self, temp_db):
        """Prueba ciclo de vida completo de una historia"""
        # Crear usuario
        temp_db.create_user("autor", "autor@example.com", "password123")
        user = temp_db.login_user("autor", "password123")
        
        # 1. Crear historia
        story_content = "Historia para ciclo de vida"
        story_location = "Concepción, Chile"
        story_category = "OVNI"
        
        result = temp_db.create_story(
            user_id=user['id'],
            content=story_content,
            location=story_location,
            category=story_category
        )
        assert result is True
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # 2. Agregar imágenes
        image_paths = ["media/imagen1.jpg", "media/imagen2.jpg"]
        result = temp_db.add_story_images(story_id, image_paths)
        assert result is True
        
        # 3. Agregar interacciones
        temp_db.add_like(story_id, user['id'])
        temp_db.add_comment(story_id, user['id'], "Comentario del autor")
        temp_db.add_reaction(story_id, user['id'], 'miedo')
        
        # 4. Actualizar historia
        new_content = "Historia actualizada"
        new_location = "Nueva ubicación"
        new_category = "Leyenda"
        
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
        
        # 5. Crear reporte
        temp_db.create_user("reporter", "reporter@example.com", "password123")
        reporter = temp_db.login_user("reporter", "password123")
        
        result = temp_db.create_report(
            story_id=story_id,
            reporter_id=reporter['id'],
            motivo='Contenido inapropiado',
            descripcion='Este contenido no es apropiado'
        )
        assert result is True
        
        # Verificar reporte
        reports = temp_db.get_reports()
        assert len(reports) == 1
        assert reports[0]['motivo'] == 'Contenido inapropiado'
        
        # 6. Eliminar historia
        result = temp_db.delete_story(story_id, user['id'])
        assert result is True
        
        # Verificar eliminación
        stories = temp_db.get_all_stories(limit=10, offset=0)
        assert len(stories) == 0
        
        # Verificar que las interacciones también se eliminaron
        comments = temp_db.get_comments(story_id)
        assert len(comments) == 0
    
    def test_search_functionality(self, temp_db):
        """Prueba funcionalidad de búsqueda completa"""
        # Crear usuarios y historias
        users = []
        for i in range(2):
            username = f"buscador{i+1}"
            email = f"buscador{i+1}@example.com"
            password = "password123"
            
            temp_db.create_user(username, email, password)
            user = temp_db.login_user(username, password)
            users.append(user)
        
        # Crear historias con diferentes características
        stories_data = [
            {
                'content': 'Fantasmas en el cementerio de Valparaíso',
                'location': 'Valparaíso, Chile',
                'category': 'Fantasma'
            },
            {
                'content': 'OVNI avistado en el desierto de Atacama',
                'location': 'Atacama, Chile',
                'category': 'OVNI'
            },
            {
                'content': 'Leyenda del Caleuche en Chiloé',
                'location': 'Chiloé, Chile',
                'category': 'Leyenda'
            },
            {
                'content': 'Aparición en hospital de Santiago',
                'location': 'Santiago, Chile',
                'category': 'Aparición'
            }
        ]
        
        for i, story_data in enumerate(stories_data):
            temp_db.create_story(
                user_id=users[i % 2]['id'],
                content=story_data['content'],
                location=story_data['location'],
                category=story_data['category']
            )
        
        # Pruebas de búsqueda
        # Búsqueda por contenido
        results = temp_db.search_stories('fantasmas')
        assert len(results) == 1
        assert 'fantasmas' in results[0]['content'].lower()
        
        # Búsqueda por ubicación
        results = temp_db.search_stories('Santiago')
        assert len(results) == 1
        assert 'Santiago' in results[0]['location']
        
        # Búsqueda por categoría
        results = temp_db.search_stories('OVNI')
        assert len(results) == 1
        assert results[0]['category'] == 'OVNI'
        
        # Búsqueda que no encuentra nada
        results = temp_db.search_stories('término_inexistente')
        assert len(results) == 0
    
    def test_notification_system(self, temp_db):
        """Prueba sistema completo de notificaciones"""
        # Crear usuarios
        temp_db.create_user("autor", "autor@example.com", "password123")
        autor = temp_db.login_user("autor", "password123")
        
        temp_db.create_user("interactor1", "interactor1@example.com", "password123")
        interactor1 = temp_db.login_user("interactor1", "password123")
        
        temp_db.create_user("interactor2", "interactor2@example.com", "password123")
        interactor2 = temp_db.login_user("interactor2", "password123")
        
        # Autor crea historia
        temp_db.create_story(
            user_id=autor['id'],
            content="Historia para notificaciones",
            location="Santiago, Chile",
            category="Aparición"
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Interactor1 interactúa
        temp_db.add_like(story_id, interactor1['id'])
        temp_db.add_comment(story_id, interactor1['id'], "Comentario 1")
        temp_db.add_reaction(story_id, interactor1['id'], 'miedo')
        
        # Interactor2 interactúa
        temp_db.add_like(story_id, interactor2['id'])
        temp_db.add_comment(story_id, interactor2['id'], "Comentario 2")
        temp_db.add_reaction(story_id, interactor2['id'], 'sorpresa')
        
        # Verificar notificaciones del autor
        notifications = temp_db.get_user_notifications(autor['id'])
        assert len(notifications) == 6  # 2 likes, 2 comentarios, 2 reacciones
        
        # Verificar tipos de notificaciones
        notification_types = [n['tipo'] for n in notifications]
        assert notification_types.count('like') == 2
        assert notification_types.count('comment') == 2
        assert notification_types.count('reaction') == 2
        
        # Marcar notificación como leída
        notification_id = notifications[0]['id']
        result = temp_db.mark_notification_as_read(notification_id, autor['id'])
        assert result is True
        
        # Marcar todas como leídas
        result = temp_db.mark_all_notifications_as_read(autor['id'])
        assert result is True
    
    def test_data_consistency(self, temp_db):
        """Prueba consistencia de datos en operaciones complejas"""
        # Crear usuarios
        users = []
        for i in range(3):
            username = f"consistencia{i+1}"
            email = f"consistencia{i+1}@example.com"
            password = "password123"
            
            temp_db.create_user(username, email, password)
            user = temp_db.login_user(username, password)
            users.append(user)
        
        # Usuario 1 crea historia
        temp_db.create_story(
            user_id=users[0]['id'],
            content="Historia para consistencia",
            location="Santiago, Chile",
            category="Aparición"
        )
        
        stories = temp_db.get_all_stories(limit=1, offset=0)
        story_id = stories[0]['id']
        
        # Múltiples interacciones
        for user in users:
            temp_db.add_like(story_id, user['id'])
            temp_db.add_comment(story_id, user['id'], f"Comentario de {user['username']}")
            temp_db.add_reaction(story_id, user['id'], 'miedo')
        
        # Verificar consistencia de contadores
        stories = temp_db.get_all_stories(limit=1, offset=0)
        assert stories[0]['likes'] == 3
        assert stories[0]['miedo'] == 3
        
        comments = temp_db.get_comments(story_id)
        assert len(comments) == 3
        
        # Verificar que no hay duplicados
        like_ids = set()
        comment_ids = set()
        reaction_ids = set()
        
        # Verificar en base de datos directamente
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM likes WHERE story_id = ?", (story_id,))
        like_user_ids = [row[0] for row in cursor.fetchall()]
        assert len(like_user_ids) == 3
        assert len(set(like_user_ids)) == 3  # No duplicados
        
        cursor.execute("SELECT user_id FROM comentarios WHERE story_id = ?", (story_id,))
        comment_user_ids = [row[0] for row in cursor.fetchall()]
        assert len(comment_user_ids) == 3
        assert len(set(comment_user_ids)) == 3  # No duplicados
        
        cursor.execute("SELECT user_id FROM reacciones WHERE story_id = ?", (story_id,))
        reaction_user_ids = [row[0] for row in cursor.fetchall()]
        assert len(reaction_user_ids) == 3
        assert len(set(reaction_user_ids)) == 3  # No duplicados
        
        conn.close()
    
    def test_error_handling(self, temp_db):
        """Prueba manejo de errores en operaciones complejas"""
        # Intentar operaciones con datos inválidos
        result = temp_db.create_user("", "email@example.com", "password")
        assert result is False
        
        result = temp_db.create_user("username", "", "password")
        assert result is False
        
        result = temp_db.create_user("username", "email@example.com", "")
        assert result is False
        
        # Intentar operaciones con IDs inexistentes
        result = temp_db.add_like(999, 999)
        assert result is False
        
        result = temp_db.add_comment(999, 999, "Comentario")
        assert result is False
        
        result = temp_db.add_reaction(999, 999, 'miedo')
        assert result is False
        
        # Intentar actualizar historia inexistente
        result = temp_db.update_story(999, 999, "Contenido", "Ubicación", "Categoría")
        assert result is False
        
        # Intentar eliminar historia inexistente
        result = temp_db.delete_story(999, 999)
        assert result is False
