# Sombras de Chile 👻

Una aplicación móvil desarrollada con Kivy para compartir historias paranormales, mitos y leyendas de Chile.

## Integrantes y roles
Líder/Coordinador: [John Alvarez & Emanuel Torres]
Analista de datos / Modelador ER: [John Alvarez & Emanuel Torres]
Implementador SQLite / Kivy: [John Alvarez & Emanuel Torres]
Redactor / QA: [John Alvarez & Emanuel Torres]
Presentador: [John Alvarez & Emanuel Torres]

### 🧭 **1. Alcance y Datos Relevantes**

#### 📘 **Descripción General**
El proyecto **Historias Paranormales de Chile** consiste en una aplicación móvil donde los usuarios pueden **compartir y leer experiencias paranormales ocurridas en distintas regiones del país**.  
Cada historia puede incluir una ubicación, una fotografía opcional y permite interacción mediante *likes* y *comentarios*.  
Toda la información se almacena de manera persistente utilizando **SQLite** como motor de base de datos local, garantizando la integridad y seguridad de los datos sin necesidad de un servidor externo.

---

#### 🧩 **Entidades Clave**
| Entidad | Descripción | Tipo de relación |
|----------|--------------|------------------|
| **Usuario** | Representa a cada persona registrada en la aplicación. | 1:N con Historias, Likes, Comentarios |
| **Historia** | Relato o suceso paranormal publicado por un usuario. | N:1 con Usuario, 1:N con Likes y Comentarios |
| **Like** | Reacción positiva que un usuario da a una historia. | N:1 con Usuario, N:1 con Historia |
| **Comentario** | Opinión o aporte textual sobre una historia. | N:1 con Usuario, N:1 con Historia |

---

#### 📊 **Volumen Esperado de Datos**
| Entidad | Registros estimados | Observaciones |
|----------|--------------------|----------------|
| **Usuarios** | 100–500 | Base inicial de usuarios activos |
| **Historias** | 500–2000 | Publicaciones en crecimiento |
| **Likes** | 5000+ | Alta interacción social esperada |
| **Comentarios** | 2000+ | Promedio de 3–5 por historia |

---

#### ⚙️ **Operaciones CRUD**
| Entidad | Crear | Leer | Actualizar | Eliminar |
|----------|--------|-------|-------------|----------|
| **Usuario** | Registrar usuario nuevo | Iniciar sesión, listar usuarios | Modificar perfil | Eliminar cuenta |
| **Historia** | Publicar historia nueva | Ver historias, buscar por región o usuario | Editar historia propia | Eliminar historia propia |
| **Like** | Dar “me gusta” | Contar likes por historia | — | Quitar like |
| **Comentario** | Comentar historia | Ver comentarios asociados | Editar comentario propio | Eliminar comentario propio |

---

#### 🔐 **Requisitos de Seguridad**
- Contraseñas encriptadas mediante **SHA-256**.  
- Campos `username` y `email` definidos como **UNIQUE**.  
- Integridad referencial con **claves foráneas**.  
- Restricción única `(user_id, story_id)` para evitar likes duplicados.  

---

#### 💾 **Persistencia**
- **Motor de base de datos:** SQLite  
- **Archivo:** `paranormal_stories.db`  
- **Creación automática:** al ejecutar `database.py`  
- **Tablas:** `usuarios`, `historias`, `likes`, `comentarios`  
- **Ubicación:** Directorio raíz del proyecto  

---

### 🗂️ **5. Persistencia**
El proyecto utiliza **SQLite** como sistema embebido de base de datos, permitiendo crear un archivo local (`paranormal_stories.db`) que se inicializa automáticamente al ejecutar el programa.