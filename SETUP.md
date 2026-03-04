# Guía de configuración del proyecto NaturalSlim eCommerce

Este documento permite a cualquier persona (o a un agente en Cursor) levantar el proyecto desde cero. Sigue los pasos en orden.

---

## 1. Prerrequisitos

### 1.1 Docker y Docker Compose

El proyecto usa **Docker** para ejecutar la base de datos (PostgreSQL), Odoo 17 y opcionalmente el frontend.

**Comprobar si Docker está instalado:**

```bash
docker --version
docker compose version
```

Si uno de los dos falla o no existe el comando, hay que instalar Docker.

**Instalar Docker:**

- **Windows / Mac:** Descargar e instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/). Tras instalar, abrir Docker Desktop y esperar a que esté en estado "Running".
- **Linux:** Seguir la [guía oficial de instalación](https://docs.docker.com/engine/install/) para tu distribución. Luego instalar el plugin Compose o el binario `docker compose`.

**Importante:** Docker Desktop (en Windows/Mac) debe estar **abierto y en ejecución** antes de usar `docker compose` o `docker-compose`. Si no, aparecerán errores como "cannot find the file specified" o "error during connect".

### 1.2 Node.js (solo si quieres correr el frontend en local)

Opcional. Si usas el contenedor `frontend` del `docker-compose`, no hace falta.

- Para ejecutar el frontend con `npm run dev` en tu máquina: instalar [Node.js 20 LTS](https://nodejs.org/).
- Comprobar: `node --version` (debe ser v20.x o superior).

---

## 2. Estructura del proyecto que debe existir

Antes de levantar, en la raíz del proyecto deben existir al menos:

- `docker-compose.yml`
- `odoo.conf`
- Carpeta `addons/naturalslim_api/` con el módulo de Odoo (incluye `__manifest__.py` y `controllers/main.py`)
- Carpeta `frontend/` con el proyecto Vue (incluye `package.json`, `vite.config.ts`, `src/`)

Si falta algo, el proyecto no está completo o el repositorio no se clonó bien.

---

## 3. Levantar los servicios con Docker

**Desde la raíz del proyecto** (donde está `docker-compose.yml`):

```bash
docker compose up -d
```

O, si tu instalación usa el binario antiguo:

```bash
docker-compose up -d
```

Esto levanta:

- **db:** PostgreSQL 15 (puerto interno).
- **odoo:** Odoo 17 en **http://localhost:8069**
- **frontend:** Vue (Vite) en **http://localhost:5173**

La primera vez puede tardar varios minutos en descargar imágenes e instalar dependencias del frontend.

**Comprobar que los contenedores están en marcha:**

```bash
docker compose ps
```

Deben aparecer `naturalslim_db`, `naturalslim_odoo` y `naturalslim_frontend` (o el nombre del servicio `frontend`) en estado "Up".

---

## 4. Crear la base de datos en Odoo e instalar el módulo

1. Abrir en el navegador: **http://localhost:8069**

2. **Si es la primera vez**, Odoo pedirá crear una base de datos:
   - **Master Password:** `admin` (está definido en `odoo.conf`).
   - **Database Name:** por ejemplo `naturalslim`.
   - **Email** y **Password:** los que quieras para el usuario administrador.
   - Pulsar **Create database** y esperar.

3. **Instalar el módulo "NaturalSlim API":**
   - Ir al menú **Apps** (Aplicaciones).
   - Quitar el filtro que limita a "Apps" instaladas (para ver todos los módulos).
   - En el buscador escribir: **NaturalSlim** o **naturalslim**.
   - Debe aparecer **NaturalSlim API**. Pulsar **Install** (Instalar).
   - Si no aparece: en **Apps**, menú (tres puntos) → **Update Apps List**, confirmar y volver a buscar **NaturalSlim API**.

4. **(Recomendado)** Crear al menos un producto de prueba:
   - Ir a **Ventas → Productos** (o **Inventory → Products**).
   - Crear un producto, marcar como **Vendible** y guardar.
   Así la tienda frontend mostrará datos.

---

## 5. Comprobar que todo funciona

1. **Backend (Odoo):**  
   Abrir **http://localhost:8069/api/products** en el navegador. Debe devolver JSON, por ejemplo: `{"products": [...]}`.

2. **Frontend (Vue):**  
   Abrir **http://localhost:5173**. Debe cargar la página "Productos" de NaturalSlim. Si Odoo está arriba y el módulo instalado, no debería aparecer "Failed to fetch".

3. **Flujo completo:**  
   En el frontend, agregar un producto al carrito, ir a Carrito y pulsar "Crear presupuesto en Odoo". En Odoo, en **Ventas → Pedidos**, debe aparecer el presupuesto creado.

---

## 6. Alternativa: frontend en local (sin contenedor frontend)

Si prefieres no usar el contenedor del frontend:

1. Levantar solo base de datos y Odoo:

   ```bash
   docker compose up -d db odoo
   ```

2. En otra terminal, desde la raíz del proyecto:

   ```bash
   cd frontend
   cp .env.example .env
   npm install
   npm run dev
   ```

3. Abrir **http://localhost:5173**. El archivo `vite.config.ts` tiene un proxy: en desarrollo las peticiones a `/api` se reenvían a `http://localhost:8069`, así que no hace falta cambiar `.env` si Odoo corre en 8069.

---

## 7. Problemas frecuentes

| Problema | Qué hacer |
|----------|-----------|
| "Failed to fetch" en el frontend | Odoo no está en marcha, el módulo no está instalado o el puerto 8069 está bloqueado. Comprobar `docker compose ps`, abrir http://localhost:8069 y http://localhost:8069/api/products. |
| "cannot find the file specified" / "error during connect" al hacer `docker compose up` | Docker Desktop no está abierto o el motor Docker no está corriendo. Abrir Docker Desktop (Windows/Mac) y esperar a que esté "Running". |
| No aparece el módulo "NaturalSlim API" en Apps | Reiniciar Odoo: `docker compose restart odoo`. En Odoo: Apps → menú → Update Apps List. Comprobar que existe la carpeta `addons/naturalslim_api/` con `__manifest__.py`. |
| El frontend no arranca en el contenedor | Revisar logs: `docker compose logs frontend`. Si falla `npm install`, puede ser red o permisos; en ese caso usar la opción de frontend en local (sección 6). |
| Puerto 8069 o 5173 ya en uso | Cambiar en `docker-compose.yml` el mapeo de puertos (ej. `"8070:8069"` para Odoo). Si cambias el puerto de Odoo, en frontend local o en el proxy de Vite tendrás que apuntar a ese puerto. |

---

## 8. Resumen para un agente (Cursor)

- **Requisito obligatorio:** Docker (y Docker Desktop en ejecución en Windows/Mac).
- **Comandos en orden:**  
  1) `docker compose up -d` (desde la raíz).  
  2) Abrir http://localhost:8069, crear BD si aplica, instalar módulo "NaturalSlim API".  
  3) Abrir http://localhost:5173 para usar el frontend.
- **Contraseña master de Odoo:** `admin` (en `odoo.conf`).
- **Si falla "Failed to fetch":** comprobar que Odoo esté arriba y que el módulo esté instalado; el frontend usa proxy en dev a `http://localhost:8069`.
