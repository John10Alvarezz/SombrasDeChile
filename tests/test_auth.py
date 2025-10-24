# -*- coding: utf-8 -*-
"""
Pruebas para funcionalidades de autenticación
"""
import pytest
from database import Database


class TestAuthentication:
    """Clase de pruebas para autenticación de usuarios"""
    
    def test_user_registration_success(self, temp_db):
        """Prueba registro exitoso de usuario"""
        username = "nuevo_usuario"
        email = "nuevo@example.com"
        password = "password123"
        
        result = temp_db.create_user(username, email, password)
        assert result is True
        
        # Verificar que el usuario se creó
        user = temp_db.login_user(username, password)
        assert user is not None
        assert user['username'] == username
        assert user['email'] == email
    
    def test_user_registration_duplicate_username(self, temp_db):
        """Prueba registro con username duplicado"""
        username = "usuario_duplicado"
        email1 = "email1@example.com"
        email2 = "email2@example.com"
        password = "password123"
        
        # Crear primer usuario
        result1 = temp_db.create_user(username, email1, password)
        assert result1 is True
        
        # Intentar crear segundo usuario con mismo username
        result2 = temp_db.create_user(username, email2, password)
        assert result2 is False
    
    def test_user_registration_duplicate_email(self, temp_db):
        """Prueba registro con email duplicado"""
        username1 = "usuario1"
        username2 = "usuario2"
        email = "email_duplicado@example.com"
        password = "password123"
        
        # Crear primer usuario
        result1 = temp_db.create_user(username1, email, password)
        assert result1 is True
        
        # Intentar crear segundo usuario con mismo email
        result2 = temp_db.create_user(username2, email, password)
        assert result2 is False
    
    def test_user_login_success(self, temp_db):
        """Prueba login exitoso"""
        username = "usuario_login"
        email = "login@example.com"
        password = "password123"
        
        # Crear usuario
        temp_db.create_user(username, email, password)
        
        # Login exitoso
        user = temp_db.login_user(username, password)
        assert user is not None
        assert user['username'] == username
        assert user['email'] == email
    
    def test_user_login_wrong_password(self, temp_db):
        """Prueba login con contraseña incorrecta"""
        username = "usuario_wrong_pass"
        email = "wrong@example.com"
        password = "password123"
        wrong_password = "wrongpassword"
        
        # Crear usuario
        temp_db.create_user(username, email, password)
        
        # Login con contraseña incorrecta
        user = temp_db.login_user(username, wrong_password)
        assert user is None
    
    def test_user_login_nonexistent_user(self, temp_db):
        """Prueba login con usuario inexistente"""
        username = "usuario_inexistente"
        password = "password123"
        
        # Login con usuario que no existe
        user = temp_db.login_user(username, password)
        assert user is None
    
    def test_password_hashing(self, temp_db):
        """Prueba que las contraseñas se hashean correctamente"""
        username = "usuario_hash"
        email = "hash@example.com"
        password = "password123"
        
        # Crear usuario
        temp_db.create_user(username, email, password)
        
        # Verificar que la contraseña se hasheó
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM usuarios WHERE username = ?", (username,))
        stored_hash = cursor.fetchone()[0]
        conn.close()
        
        # El hash no debe ser igual a la contraseña en texto plano
        assert stored_hash != password
        assert len(stored_hash) > 0
    
    def test_password_verification(self, temp_db):
        """Prueba verificación de contraseñas"""
        username = "usuario_verify"
        email = "verify@example.com"
        password = "password123"
        
        # Crear usuario
        temp_db.create_user(username, email, password)
        
        # Verificar que la contraseña se verifica correctamente
        user = temp_db.login_user(username, password)
        assert user is not None
        
        # Verificar que contraseña incorrecta falla
        user = temp_db.login_user(username, "wrongpassword")
        assert user is None
    
    def test_user_data_integrity(self, temp_db):
        """Prueba integridad de datos de usuario"""
        username = "usuario_integrity"
        email = "integrity@example.com"
        password = "password123"
        
        # Crear usuario
        result = temp_db.create_user(username, email, password)
        assert result is True
        
        # Login y verificar datos
        user = temp_db.login_user(username, password)
        assert user is not None
        assert user['username'] == username
        assert user['email'] == email
        assert 'id' in user
        assert 'created_at' in user
        assert user['id'] is not None
    
    def test_empty_credentials(self, temp_db):
        """Prueba manejo de credenciales vacías"""
        # Intentar crear usuario con datos vacíos
        result = temp_db.create_user("", "email@example.com", "password123")
        assert result is False
        
        result = temp_db.create_user("username", "", "password123")
        assert result is False
        
        result = temp_db.create_user("username", "email@example.com", "")
        assert result is False
    
    def test_special_characters_in_credentials(self, temp_db):
        """Prueba manejo de caracteres especiales en credenciales"""
        username = "usuario_especial_ñáéíóú"
        email = "especial@example.com"
        password = "contraseña123"
        
        # Crear usuario con caracteres especiales
        result = temp_db.create_user(username, email, password)
        assert result is True
        
        # Login exitoso
        user = temp_db.login_user(username, password)
        assert user is not None
        assert user['username'] == username
    
    def test_long_credentials(self, temp_db):
        """Prueba manejo de credenciales largas"""
        long_username = "a" * 100  # Username muy largo
        long_email = "a" * 50 + "@example.com"  # Email muy largo
        long_password = "p" * 1000  # Contraseña muy larga
        
        # Intentar crear usuario con credenciales muy largas
        result = temp_db.create_user(long_username, long_email, long_password)
        # Debería fallar o manejar correctamente
        # El resultado depende de la implementación de la base de datos
        assert result is not None  # True o False, pero no debe crashear
    
    def test_sql_injection_prevention(self, temp_db):
        """Prueba prevención de inyección SQL"""
        malicious_username = "'; DROP TABLE usuarios; --"
        malicious_email = "malicious@example.com"
        password = "password123"
        
        # Intentar crear usuario con datos maliciosos
        result = temp_db.create_user(malicious_username, malicious_email, password)
        # Debería manejar correctamente los caracteres especiales
        assert result is not None  # True o False, pero no debe crashear
        
        # Verificar que las tablas siguen existiendo
        conn = temp_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert 'usuarios' in tables  # La tabla debe seguir existiendo
