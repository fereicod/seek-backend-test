# Sistema de Gestión de Libros

## Descripción
Este es un sistema backend para la gestión de información de libros utilizando MongoDB como base de datos. El sistema proporciona una API REST construida con FastAPI para realizar operaciones CRUD completas y agregaciones avanzadas mediante pipelines de MongoDB.

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

### 🚀 API Demo (Producción)

> [!TIP]
> **Prueba la API sin instalar nada**
> 
> La API está desplegada y disponible para probar directamente:
> 
> 👉 **[https://seek-backend-test.vercel.app/docs](https://seek-backend-test.vercel.app/docs)**
> 
> **Credenciales de prueba:** `admin@test.com` / `adminpass`

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

## Diagrama general

```mermaid
graph TB
    Client["👤 API Client<br/>(Postman / Swagger)"]
    
    subgraph FastAPI["⚡ FastAPI Books System"]
        direction TB
        
        Router["🔌 API Routers<br/>• /api/v1/auth (login)<br/>• /api/v1/books (CRUD + Stats)"]
        
        Security["🔐 Security Layer<br/>• JWT Authentication<br/>• Permission Checks<br/>(book:read, book:create, book:update, book:delete)"]
        
        Repos["📦 Repository Layer<br/>• UserMongoRepository<br/>• BookMongoRepository<br/>• DB Selectors"]
        
        Logic["⚙️ Business Logic<br/>• Pagination (Page/Offset)<br/>• Sorting & Filtering<br/>• MongoDB Aggregation Pipeline"]
    end
    
    Database[("🍃 MongoDB<br/>• users collection<br/>• books collection")]
    
    Client -->|"HTTPS/REST"| Router
    Router --> Security
    Security --> Repos
    Repos --> Logic
    Logic --> Database
    Repos --> Database

    style Client fill:#E3F2FD,stroke:#1976D2,stroke-width:2px,color:#000
    style FastAPI fill:#FFF3E0,stroke:#F57C00,stroke-width:3px,color:#000
    style Database fill:#E8F5E9,stroke:#388E3C,stroke-width:3px,color:#000
    style Router fill:#BBDEFB,stroke:#1976D2,color:#000
    style Security fill:#FFCCBC,stroke:#E64A19,color:#000
    style Repos fill:#FFE082,stroke:#F57C00,color:#000
    style Logic fill:#C5E1A5,stroke:#689F38,color:#000
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

Arquitectura híbrida: **Clean Architecture + Capas**, optimizada para FastAPI.

**Capas:** Routers → Schemas → Repositories → Models → Core

**Ventajas:** Separación de responsabilidades, testabilidad, flexibilidad de DB (selectores permiten intercambiar gestores por entidad)

## Mejoras Futuras

- [ ] Gestión de Tokens (refresh, logout)
- [ ] Rate Limiting
- [ ] Paginación cursor-based y limit-offset
- [ ] Ampliar cobertura de pruebas (~32% actual)
- [ ] Códigos HTTP específicos (404, 422, 429)
- [ ] Validación de usuario activo en cada request
- [ ] Sistema de roles con jerarquía
- [ ] Caché con Redis
- [ ] Dockerización y Health checks

## Notas sobre el Reto Técnico

### 1. Migración con Django
**Decisión:** No se usó Django. Se implementó `app/migrations/seed.py` con PyMongo, manteniendo coherencia con el stack FastAPI.

### 2. Autenticación JWT
**Decisión:** JWT con bcrypt + sistema de permisos granular (`book:read`, `book:create`, etc.). Preparado para escalar a roles.

### 3. Arquitectura
**Decisión:** Híbrido Clean Architecture + Capas. Ver diagrama y sección "Arquitectura del Proyecto" arriba.

### 4. Códigos HTTP
**Estado:** Implementación básica. Falta 404, 422, 429. Ver "Mejoras Futuras".

### 5. Validación de Usuario
**Pendiente:** Verificar `user.is_active` en cada request (actualmente solo valida JWT).


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