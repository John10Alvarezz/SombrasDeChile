# Historias Paranormales de Chile 👻

Una aplicación de escritorio desarrollada con Kivy para compartir historias paranormales, mitos y leyendas de Chile.

## Características

- **Modo Oscuro**: Diseño con temática oscura para crear atmósfera de misterio
- **Sistema de Autenticación**: Registro e inicio de sesión de usuarios
- **Modo Invitado**: Navega sin registrarte
- **Publicación de Historias**: Comparte tus experiencias paranormales
- **Modo Incógnito**: Publica de forma anónima
- **Ubicaciones**: Agrega la ubicación de tus historias
- **Sistema de Likes**: Reacciona a las historias que te gustan
- **Búsqueda**: Encuentra historias por contenido o ubicación
- **Perfil de Usuario**: Visualiza tus historias publicadas

## Requisitos

- Python 3.8 o superior
- Kivy 2.3.1
- SQLite (incluido con Python)

## Instalación

1. Clona o descarga el proyecto

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación:
```bash
python main.py
```

## Estructura del Proyecto

```
.
├── main.py                          # Archivo principal de la aplicación
├── database.py                      # Gestión de base de datos SQLite
├── requirements.txt                 # Dependencias del proyecto
├── INSTRUCCIONES_BASE_DE_DATOS.md  # Documentación de la base de datos
└── paranormal_stories.db           # Base de datos (se crea automáticamente)
```

## Pantallas de la Aplicación

### 1. Pantalla de Bienvenida
- Opción para continuar como invitado
- Opción para iniciar sesión

### 2. Login y Registro
- Crear cuenta nueva
- Iniciar sesión con credenciales existentes

### 3. Feed de Historias
- Visualiza todas las historias publicadas
- Da likes a las historias (usuarios registrados)
- Ordenadas por fecha de publicación

### 4. Búsqueda
- Busca historias por palabras clave
- Filtra por ubicación o contenido

### 5. Crear Historia
- Escribe tu historia paranormal
- Agrega ubicación (opcional)
- Publica en modo incógnito
- Opción para agregar foto (preparada para futuras versiones)

### 6. Perfil
- Visualiza tu información de usuario
- Ve todas tus historias publicadas
- Cierra sesión

## Base de Datos

La aplicación utiliza SQLite con las siguientes tablas:

- **usuarios**: Información de usuarios registrados
- **historias**: Historias publicadas
- **likes**: Sistema de "me gusta"
- **comentarios**: Preparado para futuras versiones

Para más detalles, consulta: `INSTRUCCIONES_BASE_DE_DATOS.md`

## Características Técnicas

### Diseño
- Color de fondo principal: RGB(0.08, 0.08, 0.12)
- Color de tarjetas: RGB(0.12, 0.12, 0.17)
- Botones principales: Tonos púrpura oscuro
- Tipografía clara y legible en modo oscuro

### Seguridad
- Contraseñas encriptadas con SHA-256
- Validación de datos de entrada
- Restricciones de integridad en la base de datos

### Navegación
- Barra de navegación inferior persistente
- Transiciones suaves entre pantallas
- Scroll infinito en feeds

## Desarrollo Futuro

Características planeadas:
- [ ] Sistema de comentarios activo
- [ ] Subida y visualización de fotos
- [ ] Filtros por región de Chile
- [ ] Sistema de notificaciones
- [ ] Compartir historias
- [ ] Modo de lectura nocturna
- [ ] Estadísticas de usuario

## Limitaciones Conocidas

- La funcionalidad de fotos está preparada pero no implementada completamente
- Los comentarios están en la base de datos pero no en la interfaz
- Modo invitado tiene funcionalidad limitada (no puede publicar ni dar likes)

## Solución de Problemas

### La aplicación no inicia
- Verifica que Kivy 2.3.1 esté instalado correctamente
- Asegúrate de tener Python 3.8 o superior

### No se guardan los datos
- Verifica permisos de escritura en el directorio
- Revisa que no haya errores en la consola

### Problemas con la base de datos
- Elimina `paranormal_stories.db` y deja que se recree
- Consulta `INSTRUCCIONES_BASE_DE_DATOS.md`

## Compatibilidad

- **Windows**: ✅ Completamente compatible
- **macOS**: ✅ Compatible (requiere dependencias adicionales de Kivy)
- **Linux**: ✅ Compatible

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un pull request

## Autor

Desarrollado para la comunidad chilena interesada en lo paranormal.

---

**¡Comparte tus historias paranormales y descubre los misterios de Chile!** 👻🇨🇱
