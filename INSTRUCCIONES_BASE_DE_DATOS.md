# Instrucciones de Base de Datos - Historias Paranormales de Chile

## Descripción General

La aplicación utiliza **SQLite** como sistema de gestión de base de datos. SQLite es una base de datos embebida que no requiere configuración de servidor y almacena todos los datos en un único archivo.

## Archivo de Base de Datos

- **Nombre del archivo**: `paranormal_stories.db`
- **Ubicación**: Se crea automáticamente en el directorio raíz de la aplicación
- **Gestión**: La clase `Database` en `database.py` maneja todas las operaciones

## Estructura de Tablas

### 1. Tabla: `usuarios`

Almacena la información de los usuarios registrados en la aplicación.

**Columnas:**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Identificador único del usuario
- `username` (TEXT, UNIQUE, NOT NULL): Nombre de usuario único
- `email` (TEXT, UNIQUE, NOT NULL): Correo electrónico único
- `password_hash` (TEXT, NOT NULL): Contraseña encriptada con SHA-256
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Fecha de creación de la cuenta

**Restricciones:**
- El `username` y `email` deben ser únicos
- Todos los campos son obligatorios

### 2. Tabla: `historias`

Almacena las historias paranormales publicadas por los usuarios.

**Columnas:**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Identificador único de la historia
- `user_id` (INTEGER, NOT NULL, FOREIGN KEY): ID del usuario que publicó la historia
- `content` (TEXT, NOT NULL): Contenido de la historia
- `location` (TEXT, NULLABLE): Ubicación donde ocurrió la historia
- `is_anonymous` (INTEGER, DEFAULT 0): Indica si la publicación es anónima (0=No, 1=Sí)
- `photo_path` (TEXT, NULLABLE): Ruta de la foto adjunta (opcional)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Fecha de publicación

**Relaciones:**
- `user_id` hace referencia a `usuarios.id`

### 3. Tabla: `likes`

Almacena los "me gusta" que los usuarios dan a las historias.

**Columnas:**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Identificador único del like
- `story_id` (INTEGER, NOT NULL, FOREIGN KEY): ID de la historia
- `user_id` (INTEGER, NOT NULL, FOREIGN KEY): ID del usuario que dio like
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Fecha del like

**Restricciones:**
- Combinación única de `story_id` y `user_id` (un usuario solo puede dar un like por historia)

**Relaciones:**
- `story_id` hace referencia a `historias.id`
- `user_id` hace referencia a `usuarios.id`

### 4. Tabla: `comentarios`

Almacena los comentarios en las historias (funcionalidad preparada para futuras versiones).

**Columnas:**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Identificador único del comentario
- `story_id` (INTEGER, NOT NULL, FOREIGN KEY): ID de la historia comentada
- `user_id` (INTEGER, NOT NULL, FOREIGN KEY): ID del usuario que comentó
- `content` (TEXT, NOT NULL): Contenido del comentario
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Fecha del comentario

**Relaciones:**
- `story_id` hace referencia a `historias.id`
- `user_id` hace referencia a `usuarios.id`

## Diagrama de Relaciones

```
usuarios (1) ----< (N) historias
usuarios (1) ----< (N) likes
usuarios (1) ----< (N) comentarios
historias (1) ----< (N) likes
historias (1) ----< (N) comentarios
```

**Explicación:**
- Un usuario puede publicar múltiples historias
- Un usuario puede dar múltiples likes (pero solo uno por historia)
- Un usuario puede hacer múltiples comentarios
- Una historia puede tener múltiples likes
- Una historia puede tener múltiples comentarios

## Persistencia de Datos

### Inicialización Automática

La base de datos se inicializa automáticamente al ejecutar la aplicación:

```python
db = Database()  # Crea el archivo y las tablas si no existen
```

### Seguridad

- **Contraseñas**: Se almacenan encriptadas usando SHA-256
- **Validaciones**: Se previenen duplicados mediante restricciones UNIQUE
- **Integridad referencial**: Las claves foráneas garantizan la consistencia

### Operaciones Principales

#### Crear Usuario
```python
db.create_user(username, email, password)
```

#### Iniciar Sesión
```python
user = db.login_user(username, password)
```

#### Publicar Historia
```python
db.create_story(user_id, content, location, is_anonymous)
```

#### Obtener Todas las Historias
```python
stories = db.get_all_stories()
```

#### Buscar Historias
```python
results = db.search_stories(query)
```

#### Dar Like
```python
db.add_like(story_id, user_id)
```

## Instalación y Configuración

### Requisitos

```bash
pip install -r requirements.txt
```

### Ejecución

```bash
python main.py
```

La base de datos se creará automáticamente en la primera ejecución.

## Respaldo de Datos

Para hacer una copia de seguridad, simplemente copia el archivo `paranormal_stories.db` a una ubicación segura.

### Restaurar Respaldo

Reemplaza el archivo `paranormal_stories.db` con la copia de seguridad.

## Consultas SQL Útiles

### Ver todos los usuarios
```sql
SELECT * FROM usuarios;
```

### Ver historias con información del autor
```sql
SELECT h.*, u.username
FROM historias h
LEFT JOIN usuarios u ON h.user_id = u.id;
```

### Contar likes por historia
```sql
SELECT h.id, h.content, COUNT(l.id) as total_likes
FROM historias h
LEFT JOIN likes l ON h.id = l.story_id
GROUP BY h.id;
```

### Historias más populares
```sql
SELECT h.content, u.username, COUNT(l.id) as likes
FROM historias h
LEFT JOIN usuarios u ON h.user_id = u.id
LEFT JOIN likes l ON h.id = l.story_id
GROUP BY h.id
ORDER BY likes DESC;
```

## Mantenimiento

### Limpiar datos de prueba

```python
import sqlite3
conn = sqlite3.connect('paranormal_stories.db')
cursor = conn.cursor()

# Eliminar todos los datos (cuidado, no hay vuelta atrás)
cursor.execute('DELETE FROM comentarios')
cursor.execute('DELETE FROM likes')
cursor.execute('DELETE FROM historias')
cursor.execute('DELETE FROM usuarios')

conn.commit()
conn.close()
```

### Verificar integridad

SQLite incluye un comando para verificar la integridad:

```python
conn = sqlite3.connect('paranormal_stories.db')
cursor = conn.cursor()
cursor.execute('PRAGMA integrity_check')
result = cursor.fetchone()
print(result)  # Debe retornar 'ok'
conn.close()
```

## Escalabilidad Futura

Si la aplicación crece, considera:

1. **Índices**: Agregar índices a columnas frecuentemente consultadas
2. **Migración**: Cambiar a PostgreSQL o MySQL para aplicaciones multi-usuario
3. **Caché**: Implementar caché de consultas frecuentes
4. **Paginación**: Limitar el número de historias cargadas por vez

## Solución de Problemas

### Error: "database is locked"
- Cierra todas las conexiones abiertas
- Verifica que no haya múltiples instancias de la app

### Error: "no such table"
- Elimina el archivo `.db` y deja que se recree automáticamente

### Datos no se guardan
- Verifica que se llama a `conn.commit()` después de cada operación de escritura
