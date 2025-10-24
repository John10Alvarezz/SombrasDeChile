# -*- coding: utf-8 -*-
"""
Configuración global para las pruebas de Sombras de Chile
"""
import pytest
import os
import tempfile
import shutil
from database import Database


@pytest.fixture
def temp_db():
    """Fixture que crea una base de datos temporal para las pruebas"""
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test_paranormal_stories.db')
    
    # Crear instancia de base de datos con ruta temporal
    db = Database(db_name=db_path)
    
    yield db
    
    # Limpiar después de las pruebas
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass


@pytest.fixture
def sample_user_data():
    """Datos de usuario de prueba"""
    return {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test123456'
    }


@pytest.fixture
def sample_story_data():
    """Datos de historia de prueba"""
    return {
        'content': 'Esta es una historia de prueba para testing. Contiene información paranormal ficticia.',
        'location': 'Santiago, Chile',
        'category': 'Aparición',
        'is_anonymous': False
    }


@pytest.fixture
def sample_comment_data():
    """Datos de comentario de prueba"""
    return {
        'content': 'Este es un comentario de prueba para testing.'
    }
