# -*- coding: utf-8 -*-
import sqlite3
import hashlib
try:
    import bcrypt  # opcional; si no está instalado, hacemos fallback a SHA-256
    HAS_BCRYPT = True
except Exception:
    bcrypt = None
    HAS_BCRYPT = False
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='paranormal_stories.db'):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        # Activar claves foráneas para cada conexión
        try:
            conn.execute('PRAGMA foreign_keys = ON')
        except Exception:
            pass
        return conn

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                location TEXT,
                category TEXT DEFAULT 'Aparición',
                is_anonymous INTEGER DEFAULT 0,
                photo_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(story_id, user_id, tipo),
                FOREIGN KEY (story_id) REFERENCES historias(id),
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(story_id, user_id),
                FOREIGN KEY (story_id) REFERENCES historias(id),
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (story_id) REFERENCES historias(id),
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            )
        ''')

        # Tabla para múltiples imágenes por historia
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS story_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (story_id) REFERENCES historias(id)
            )
        ''')

        conn.commit()
        # Crear índices útiles para rendimiento
        self.ensure_indices(cursor)
        conn.close()

    def ensure_indices(self, cursor):
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historias_created_at ON historias(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historias_category ON historias(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historias_location ON historias(location)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_historias_user_id ON historias(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_likes_story_id ON likes(story_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reacciones_story_id ON reacciones(story_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_story_images_story_id ON story_images(story_id)')

    def hash_password_sha256(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def hash_password_bcrypt(self, password):
        if not HAS_BCRYPT:
            # Fallback si bcrypt no está disponible
            return self.hash_password_sha256(password)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password, stored_hash):
        # Compatibilidad: detectar bcrypt vs sha256
        if HAS_BCRYPT:
            try:
                if stored_hash.startswith('$2a$') or stored_hash.startswith('$2b$') or stored_hash.startswith('$2y$'):
                    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            except Exception:
                pass
        # Fallback SHA-256
        return self.hash_password_sha256(password) == stored_hash

    def create_user(self, username, email, password):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Si hay bcrypt disponible, usarlo; de lo contrario, SHA-256
            password_hash = self.hash_password_bcrypt(password) if HAS_BCRYPT else self.hash_password_sha256(password)

            cursor.execute(
                'INSERT INTO usuarios (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        user = dict(row)
        stored_hash = user.get('password_hash', '')

        if self.verify_password(password, stored_hash):
            # Migración: si es SHA-256, actualizar a bcrypt
            # Migración a bcrypt si está disponible y el hash aún es SHA-256
            if HAS_BCRYPT:
                try:
                    if not (stored_hash.startswith('$2a$') or stored_hash.startswith('$2b$') or stored_hash.startswith('$2y$')):
                        new_hash = self.hash_password_bcrypt(password)
                        cursor.execute('UPDATE usuarios SET password_hash = ? WHERE id = ?', (new_hash, user['id']))
                        conn.commit()
                except Exception:
                    pass
            conn.close()
            return user

        conn.close()
        return None

    def create_story(self, user_id, content, location=None, category='Aparición', is_anonymous=False, photo_path=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                '''INSERT INTO historias (user_id, content, location, category, is_anonymous, photo_path)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (user_id, content, location, category, 1 if is_anonymous else 0, photo_path)
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al crear historia: {e}")
            return False

    def get_all_stories(self, limit=20, offset=0):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT h.*, u.username,
                   (SELECT COUNT(*) FROM likes WHERE story_id = h.id) as likes,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'miedo') as miedo,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'sorpresa') as sorpresa,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'incredulidad') as incredulidad,
                   (SELECT GROUP_CONCAT(si.path, '|') FROM story_images si WHERE si.story_id = h.id ORDER BY si.sort_order, si.id) as images
            FROM historias h
            LEFT JOIN usuarios u ON h.user_id = u.id
            ORDER BY h.created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))

        stories = [dict(row) for row in cursor.fetchall()]
        conn.close()

        for story in stories:
            story['created_at'] = self.format_date(story['created_at'])
            if story.get('images'):
                story['images'] = [p for p in story['images'].split('|') if p]
            else:
                story['images'] = []

        return stories

    def add_story_images(self, story_id, image_paths):
        if not image_paths:
            return True
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            for idx, path in enumerate(image_paths[:4]):
                cursor.execute(
                    'INSERT INTO story_images (story_id, path, sort_order) VALUES (?, ?, ?)',
                    (story_id, path, idx)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al guardar imágenes: {e}")
            return False

    def get_user_stories(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT h.*, u.username,
                   (SELECT COUNT(*) FROM likes WHERE story_id = h.id) as likes,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'miedo') as miedo,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'sorpresa') as sorpresa,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'incredulidad') as incredulidad
            FROM historias h
            LEFT JOIN usuarios u ON h.user_id = u.id
            WHERE h.user_id = ?
            ORDER BY h.created_at DESC
        ''', (user_id,))

        stories = [dict(row) for row in cursor.fetchall()]
        conn.close()

        for story in stories:
            story['created_at'] = self.format_date(story['created_at'])

        return stories

    def search_stories(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT h.*, u.username,
                   (SELECT COUNT(*) FROM likes WHERE story_id = h.id) as likes,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'miedo') as miedo,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'sorpresa') as sorpresa,
                   (SELECT COUNT(*) FROM reacciones WHERE story_id = h.id AND tipo = 'incredulidad') as incredulidad
            FROM historias h
            LEFT JOIN usuarios u ON h.user_id = u.id
            WHERE h.content LIKE ? OR h.location LIKE ? OR h.category LIKE ?
            ORDER BY h.created_at DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))

        stories = [dict(row) for row in cursor.fetchall()]
        conn.close()

        for story in stories:
            story['created_at'] = self.format_date(story['created_at'])

        return stories

    def add_like(self, story_id, user_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO likes (story_id, user_id) VALUES (?, ?)',
                (story_id, user_id)
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_comment(self, story_id, user_id, content):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO comentarios (story_id, user_id, content) VALUES (?, ?, ?)',
                (story_id, user_id, content)
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar comentario: {e}")
            return False

    def get_comments(self, story_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.*, u.username
            FROM comentarios c
            LEFT JOIN usuarios u ON c.user_id = u.id
            WHERE c.story_id = ?
            ORDER BY c.created_at DESC
        ''', (story_id,))

        comments = [dict(row) for row in cursor.fetchall()]
        conn.close()

        for comment in comments:
            comment['created_at'] = self.format_date(comment['created_at'])

        return comments

    def format_date(self, date_string):
        try:
            date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%d/%m/%Y %H:%M')
        except:
            return date_string

    def add_reaction(self, story_id, user_id, tipo):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO reacciones (story_id, user_id, tipo) VALUES (?, ?, ?)',
                (story_id, user_id, tipo)
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def create_sample_data(self):
        sample_stories = [
            {
                'username': 'usuario_demo',
                'email': 'demo@example.com',
                'password': 'demo123',
                'stories': [
                    {
                        'content': 'En la casa de mi abuela en Valparaíso, siempre escuchábamos pasos en el segundo piso cuando nadie estaba allí. Una noche vi una figura blanca que atravesó la pared del pasillo. Desde ese día, nunca más subí sola.',
                        'location': 'Valparaíso, Chile',
                        'category': 'Aparición',
                        'is_anonymous': False
                    },
                    {
                        'content': 'Trabajaba de nochero en un hospital antiguo de Santiago. Una madrugada, vi a una enfermera vestida de blanco caminando por el pasillo del tercer piso que está cerrado desde hace años. Cuando la seguí, simplemente desapareció.',
                        'location': 'Santiago, Chile',
                        'category': 'Fantasma',
                        'is_anonymous': False
                    }
                ]
            },
            {
                'username': 'cazafantasmas_cl',
                'email': 'cazador@example.com',
                'password': 'caza123',
                'stories': [
                    {
                        'content': 'En el cementerio de Punta Arenas, durante una investigación nocturna, grabamos una voz que decía "ayúdame" en nuestro equipo EVP. Lo más escalofriante es que nadie más estaba con nosotros en ese momento.',
                        'location': 'Punta Arenas, Chile',
                        'category': 'Psicofonía',
                        'is_anonymous': False
                    }
                ]
            },
            {
                'username': 'testigo_anon',
                'email': 'testigo@example.com',
                'password': 'test123',
                'stories': [
                    {
                        'content': 'Hace años, manejando por la ruta 5 cerca de Chillán, vi luces extrañas flotando sobre los campos. Se movían de manera errática y desaparecían instantáneamente. Varios camioneros me confirmaron después que también las habían visto.',
                        'location': 'Chillán, Chile',
                        'category': 'OVNI',
                        'is_anonymous': True
                    },
                    {
                        'content': 'La leyenda del Caleuche es real. Mi abuelo pescador juraba haberlo visto navegando cerca de Chiloé en medio de la niebla. Decía que se escuchaba música y risas provenientes del barco fantasma.',
                        'location': 'Chiloé, Chile',
                        'category': 'Leyenda',
                        'is_anonymous': False
                    },
                    {
                        'content': 'En la mina abandonada cerca de Copiapó, los mineros antiguos cuentan que se escuchan golpes en las paredes y voces de compañeros que murieron en derrumbes hace décadas. Nadie quiere trabajar en el turno nocturno.',
                        'location': 'Copiapó, Chile',
                        'category': 'Aparición',
                        'is_anonymous': True
                    }
                ]
            }
        ]

        for user_data in sample_stories:
            user_created = self.create_user(user_data['username'], user_data['email'], user_data['password'])

            if user_created:
                user = self.login_user(user_data['username'], user_data['password'])

                if user:
                    for story in user_data['stories']:
                        self.create_story(
                            user_id=user['id'],
                            content=story['content'],
                            location=story['location'],
                            category=story['category'],
                            is_anonymous=story['is_anonymous']
                        )
