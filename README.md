# Sistema de Gestión de Libros

## Descripción
Este es un sistema backend para la gestión de información de libros utilizando MongoDB como base de datos. El sistema proporciona una API REST construida con FastAPI para realizar operaciones CRUD completas y agregaciones avanzadas mediante pipelines de MongoDB.

### Características del Sistema
Cada libro contiene la siguiente información:
- **title**: Título del libro
- **author**: Autor del libro
- **published_date**: Fecha de publicación
- **genre**: Género literario
- **price**: Precio del libro

### Funcionalidades Implementadas
- ✅ **CRUD Completo**: Operaciones Create, Read, Update y Delete para libros
- ✅ **Agregaciones MongoDB**: Pipeline de agregación para calcular el precio promedio de libros por año de publicación
- ✅ **Autenticación JWT**: Sistema de login con access tokens temporales
- ✅ **Sistema de Permisos**: Control de acceso basado en permisos de usuario
- ✅ **Paginación con Links**: Paginación page-based con links de navegación (next, prev, first, last)
- ✅ **Serializers Personalizados**: Representación optimizada de datos con Pydantic
- ✅ **Pruebas Unitarias**: Tests con mocks para funciones clave (JWT, Repository)
- ✅ **Configuración de Testing**: pytest.ini configurado con ambientes de prueba (.env.test)
- ✅ **Script de Migración**: Datos iniciales de prueba (50+ libros)
- ✅ **Arquitectura Flexible**: Selectores de DB para intercambiar gestores de base de datos por entidad

## Stack Tecnológico
- **Framework**: FastAPI
- **Servidor ASGI**: Uvicorn
- **Base de Datos**: MongoDB (con soporte para múltiples gestores)
- **ODM**: PyMongo
- **Seguridad**: JWT con Bearer Tokens (Access + Refresh)
- **Testing**: Pytest
- **Gestor de Dependencias**: UV (Astral)
- **Paginación**: fastapi-pagination

## Requisitos Previos
- Python 3.12+
- MongoDB instalado y ejecutándose
- UV (Astral) instalado en el sistema

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/fereicod/seek-backend-test.git
cd seek-backend-test
```

### 2. Configurar variables de entorno
Copia el archivo de ejemplo y configura las variables según tu entorno:
```bash
cp .env.test .env
```

Configura las siguientes variables en tu archivo `.env`:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=books_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Instalar dependencias

> [!NOTE]
> **Instalación de UV (Astral)**
> 
> Si aún no tienes UV instalado:
> 
> **Con Homebrew (macOS/Linux):**
> ```bash
> brew install uv
> ```
> 
> **Con pip:**
> ```bash
> pip install uv
> ```
> 
> **Otras opciones:**
> Consulta la [documentación oficial de UV](https://docs.astral.sh/uv/getting-started/installation/) para más métodos de instalación.

Una vez instalado UV, ejecuta:
```bash
uv sync
```

### 4. Ejecutar el script de migración
Ejecuta el script para cargar los datos iniciales de prueba:
```bash
uv run python -m app.migrations.seed
```

### 5. Ejecutar la aplicación
```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en:
```
http://localhost:8000
```

## Documentación de la API

### Swagger UI (OpenAPI)
Una vez que la aplicación esté ejecutándose, accede a la documentación interactiva:
```
http://localhost:8000/docs
```

> [!IMPORTANT]
> **Autenticación en Swagger**
> 
> Para probar los endpoints de `/api/v1/books`, primero debes iniciar sesión:
> 
> **Usuarios de prueba** (si ejecutaste correctamente el seed con MongoDB):
> - **Email:** `admin@example.com` | **Password:** `admin123` | **Permisos:** Todos
> 
> **Pasos para autenticarte en Swagger:**
> 1. Ve al endpoint `POST /api/v1/auth/login`
> 2. Ejecuta el login con uno de los usuarios de prueba
> 3. Copia el `access_token` de la respuesta
> 4. Haz clic en el botón **"Authorize"** (🔒) en la parte superior derecha
> 5. Ingresa el token en el formato: `Bearer <tu_token_aqui>`
> 6. Haz clic en "Authorize" y cierra el modal
> 7. Ahora puedes ejecutar todos los endpoints protegidos

### ReDoc
Documentación alternativa disponible en:
```
http://localhost:8000/redoc
```

## Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión y obtener access

### Libros (Requieren autenticación)
- `GET /api/v1/books` - Listar libros (con paginación, requiere permisos)
- `GET /api/v1/books/{id}` - Obtener un libro específico (requiere permisos)
- `POST /api/v1/books` - Crear un nuevo libro (requiere permisos)
- `PUT /api/v1/books/{id}` - Actualizar un libro existente (requiere permisos)
- `DELETE /api/v1/books/{id}` - Eliminar un libro (requiere permisos)

### Agregaciones
- `GET /api/v1/books/stats/average-price-by-year?year={year}` - Obtener precio promedio de libros publicados en un año específico

## Pruebas

### Ejecutar todas las pruebas
```bash
uv run pytest
```

### Ejecutar pruebas con cobertura

**Para ver líneas faltantes en terminal:**
```bash
uv run pytest --cov=app --cov-report=term-missing
```

**Para generar reporte HTML:**
```bash
uv run pytest --cov=app --cov-report=html
```

**Para ambos reportes:**
```bash
uv run pytest --cov=app --cov-report=term-missing --cov-report=html
```

### Ejecutar pruebas específicas
```bash
uv run pytest tests/test_books.py -v
```

> [!NOTE]
> El archivo `pytest.ini` contiene la configuración base para las pruebas de integración del proyecto.

## Colección de Postman

Se incluye una colección de Postman con ejemplos de todas las llamadas a la API:
- Casos exitosos (HTTP 200)
- Casos de error (HTTP 400, 401, 500)
- Variables de entorno preconfiguradas

**Importar colección**: 
- Desde el repositorio: `postman/Books_API_Collection.postman_collection.json`
- Desde Postman público: [Ver colección en Postman](https://www.postman.com/fernandoei/seektestbook/collection/846952-e9739a4d-8a7c-4d40-8103-6d956e31a132/?action=share&creator=846952)

## Estructura del Proyecto

```
seek-backend-test/
├── app/
│   ├── core/           # Configuración, seguridad, dependencias
│   ├── db/             # Conexión a MongoDB y selectores de DB
│   ├── migrations/     # Scripts de migración y seed data
│   ├── models/         # Modelos de datos
│   ├── repositories/   # Capa de acceso a datos
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Schemas Pydantic (serializers)
│   └── main.py         # Aplicación principal
├── tests/              # Pruebas de integración
├── .env.test           # Variables de entorno de ejemplo
├── pyproject.toml      # Configuración del proyecto y dependencias
├── pytest.ini          # Configuración de pytest para integración
└── README.md           # Este archivo
```

## Uso de la API

### Ejemplo: Autenticación
```bash
# Login y obtener tokens
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@test.com&password=adminpass"
```

### Ejemplo: Crear un libro
```bash
curl -X POST "http://localhost:8000/api/v1/books" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "published_date": "2008-08-01",
    "genre": "Technology",
    "price": 32.99
  }'
```

### Ejemplo: Obtener precio promedio por año
```bash
curl -X GET "http://localhost:8000/api/v1/books/stats/average-price-by-year?year=2008" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Variables de Entorno Requeridas en Producción
```env
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
MONGO_DB_NAME=books_production
SECRET_KEY=super-secret-production-key-change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## Arquitectura del Proyecto

Este proyecto implementa una **arquitectura híbrida** que combina principios de **Clean Architecture** con **Arquitectura por Capas**, optimizada para FastAPI.

### Ventajas de esta Arquitectura

**Clean Architecture + Arquitectura por Capas:**
- **Separación de responsabilidades**: Cada capa tiene una responsabilidad clara y definida
- **Independencia de frameworks**: La lógica de negocio no depende de FastAPI directamente
- **Testabilidad**: Las capas se pueden probar de forma aislada
- **Mantenibilidad**: El código es más fácil de mantener y escalar
- **Flexibilidad de base de datos**: Los selectores de DB permiten cambiar gestores sin afectar la lógica

### Capas del Proyecto

1. **Routers (Presentación)**: Maneja las solicitudes HTTP y respuestas
2. **Schemas (Contratos)**: Define la estructura de entrada/salida de datos
3. **Repositories (Acceso a Datos)**: Abstrae las operaciones de base de datos
4. **Models (Dominio)**: Representa las entidades del negocio
5. **Core (Infraestructura)**: Configuración, seguridad, utilidades

### Selectores de Base de Datos

El proyecto incluye **selectores de DB** que permiten:
- Usar diferentes gestores de base de datos por entidad
- Ejemplo: Tokens en Redis, Books en MongoDB, Users en MySQL (esto es poco comun pero flexible)
- Facilita la migración y escalabilidad del sistema

## Mejoras Futuras

- [ ] **Gestión de Tokens**: Implementar endpoints para refresh token, logout y logout all (actualmente solo login)
- [ ] **Rate Limiting**: Implementar protección contra ataques DoS/DDoS con límites por IP y usuario
- [ ] **Paginación Múltiple**: Implementar soporte de limit-offset y cursor-based pagination además de page-based
- [ ] **Pruebas de Integración**: Ampliar cobertura de pruebas (actualmente ~32%) para cubrir más escenarios
- [ ] **Códigos de estado HTTP correctos**: Actualmente algunos endpoints retornan HTTP 500 en escenarios que deberían usar códigos más específicos (ej: 404 Not Found cuando un libro no existe, etc). Se debe implementar manejo de excepciones personalizado por cada caso
- [ ] **Validación de usuario activo**: Aunque el token JWT sea válido, falta verificar que el usuario esté activo en base de datos antes de procesar cada request. Agregar middleware o dependencia que valide `user.is_active` en cada endpoint protegido
- [ ] **Sistema de roles completo**: Actualmente tenemos permisos básicos a nivel granular, falta implementar:
  - Grupos de permisos (roles como Admin, Editor, Viewer)
  - Validación por roles además de permisos individuales
  - Jerarquía de roles con herencia de permisos
- [ ] **Caché con Redis**: Implementar caché para consultas frecuentes y mejorar rendimiento
- [ ] **Patrón Strategy para DB**: Implementar patrón estrategia en los selectores de repositorio para elegir dinámicamente el tipo de base de datos por cada entidad (Redis, MySQL, MongoDB)
- [ ] **Logging estructurado**: Agregar logs detallados con niveles y rotación
- [ ] **Dockerización completa**: Crear Dockerfile y docker-compose para facilitar el despliegue
- [ ] **Health checks**: Endpoints para monitorear el estado de la aplicación y dependencias

## Dudas y Comentarios sobre el Reto Técnico

### 1. Migración con Django
**Pregunta del reto:** *"Proporciona datos de prueba iniciales para al menos 5 libros utilizando un script de migración para la BD (podrías usar Django para esto)."*

**Decisión tomada:** No se utilizó Django para las migraciones.

**Razón:**
- El proyecto está construido completamente en **FastAPI**, que es un framework moderno y ligero para APIs
- Introducir Django solo para migraciones añadiría una dependencia pesada e innecesaria
- Se implementó un **script de seed data** (`app/migrations/seed.py`) que cumple el mismo propósito de manera más eficiente y consistente con el stack tecnológico
- El script de migración utiliza directamente **PyMongo** para insertar los datos de prueba, manteniendo la coherencia con el resto del proyecto

### 2. Implementación de Autenticación JWT y Usuarios
**Observación:** El reto solicita "implementar autenticación de usuarios utilizando Token Authentication".

**Decisión tomada:** Se implementó un **sistema completo de autenticación JWT** con las siguientes características:

- **Modelo de Usuario**: Email, password hasheado con bcrypt, y sistema de permisos
- **Sistema de Permisos**: Control de acceso a endpoints basado en permisos del usuario (ejemplo: `books:read`, `books:write`, `books:delete`)

**Ventajas de este enfoque:**
- Mayor seguridad con tokens de corta duración
- Control granular de permisos por endpoint
- Preparado para escalar a un sistema de roles completo

### 3. Arquitectura del Proyecto
**Decisión:** Implementar una arquitectura híbrida que combina **Clean Architecture** y **Arquitectura por Capas**.

**De Clean Architecture:**
- ✅ Separación de responsabilidades por capas
- ✅ Independencia de frameworks (la lógica no está acoplada a FastAPI)
- ✅ Inversión de dependencias (repositories abstraen el acceso a datos)
- ✅ Entidades de dominio (models) independientes

**De Arquitectura por Capas:**
- ✅ Capas bien definidas: Presentación → Aplicación → Dominio → Infraestructura
- ✅ Comunicación unidireccional entre capas
- ✅ Cada capa tiene responsabilidades específicas

**Ventajas de esta arquitectura híbrida:**
1. **Mantenibilidad**: Código organizado y fácil de navegar
2. **Testabilidad**: Cada capa se puede probar de forma aislada (mocking de repositories)
3. **Escalabilidad**: Fácil agregar nuevas funcionalidades sin afectar código existente
4. **Flexibilidad**: Los selectores de DB permiten cambiar tecnologías sin reescribir lógica
5. **Colaboración**: Estructura clara facilita el trabajo en equipo
6. **Pragmatismo**: No es tan rígida como Clean Architecture pura, pero mantiene sus beneficios

### 4. Códigos de Estado HTTP y Manejo de Errores
**Estado actual:** El proyecto tiene una implementación básica de manejo de errores.

**Problemas identificados:**
- Algunos endpoints retornan **HTTP 500** (Internal Server Error) en escenarios que deberían usar códigos más específicos
- Ejemplo: `GET /api/v1/books/{id}` retorna 500 cuando el libro no existe, pero debería retornar **404 Not Found**
- Falta manejo de excepciones personalizado para diferentes escenarios

**Mejora propuesta:**
```python
# Implementar excepciones personalizadas
class BookNotFoundException(HTTPException):
    def __init__(self, book_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
```

**Códigos HTTP que deberían implementarse:**
- ✅ `200 OK` - Operación exitosa
- ✅ `201 Created` - Recurso creado exitosamente
- ⚠️ `400 Bad Request` - Request mal formado (parcialmente implementado)
- ⚠️ `401 Unauthorized` - Token inválido o ausente (implementado)
- ⚠️ `403 Forbidden` - Usuario sin permisos (implementado)
- ❌ `404 Not Found` - Recurso no encontrado (falta implementar)
- ❌ `409 Conflict` - Conflicto (ej: duplicados)
- ❌ `422 Unprocessable Entity` - Validación de datos fallida
- ❌ `429 Too Many Requests` - Rate limit excedido (falta implementar)
- ⚠️ `500 Internal Server Error` - Error del servidor (actualmente usado en exceso)

### 5. Validación de Usuario Activo
**Estado actual:** El sistema valida que el JWT sea válido y que el usuario tenga los permisos necesarios.

**Vulnerabilidad identificada:**
- Aunque el token sea válido, **no se verifica que el usuario siga activo** en la base de datos
- Escenario problemático: Un administrador desactiva un usuario, pero sus tokens siguen funcionando hasta que expiren
- Solo se verifica la firma y expiración del JWT, no el estado actual del usuario


## Contacto y Soporte

Para preguntas o reportar problemas, por favor abre un issue en el repositorio:
```
https://github.com/fereicod/seek-backend-test/issues
```

## Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Aggregation Pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)
- [JWT Authentication](https://jwt.io/introduction)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Licencia

Este proyecto fue desarrollado como parte de un reto técnico de codificación.