# Guía de configuración del proyecto NaturalSlim eCommerce

Este documento es la **única guía necesaria** para descargar, instalar y ejecutar el proyecto desde cero (incluida la instalación de Docker). Cualquier persona o un agente en Cursor puede seguir estos pasos en orden para tener el backend y el frontend funcionando.

---

## Referencia rápida (puertos y URLs)

| Servicio   | Puerto | URL en el navegador        | Uso |
|-----------|--------|----------------------------|-----|
| **Odoo**  | **8069** | **http://localhost:8069**   | Backend: crear base de datos, instalar módulo "NaturalSlim API", gestionar productos y pedidos. |
| **Frontend** | **5173** | **http://localhost:5173** | Tienda Vue: listado de productos, carrito, crear presupuesto en Odoo. |

**Para Cursor / agente:** después de levantar el proyecto con `docker compose up -d`, abrir en el navegador (o en Simple Browser / Preview) las URLs anteriores: primero **http://localhost:8069** para configurar Odoo, luego **http://localhost:5173** para usar la tienda.

---

## 1. Instalar Docker (si no lo tienes)

El proyecto usa **Docker** y **Docker Compose** para ejecutar la base de datos, Odoo y el frontend. Sin Docker no se puede levantar el backend.

### Comprobar si ya está instalado

En una terminal ejecuta:

```bash
docker --version
docker compose version
```

Si ambos comandos muestran una versión, puedes saltar a la **sección 2**. Si alguno falla o el comando no existe, instala Docker según tu sistema.

---

### Instalar Docker en macOS (Apple Silicon o Intel)

1. **Descargar Docker Desktop para Mac**
   - Ve a: **https://www.docker.com/products/docker-desktop/**
   - Pulsa **Download for Mac** y elige la versión correcta (Apple Silicon = M1/M2/M3, o Intel).
   - Descarga el archivo `.dmg`.

2. **Instalar**
   - Abre el `.dmg` y arrastra **Docker** a la carpeta **Applications**.
   - Cierra el instalador.

3. **Abrir Docker Desktop**
   - Abre **Docker** desde **Applications** (o con Spotlight: Cmd+Space, escribe "Docker").
   - Acepta los permisos que pida (acceso a la red, etc.).
   - Espera a que en la barra de menú (arriba) el icono de Docker deje de mostrar "Starting..." y pase a "Docker Desktop is running" o similar. Puede tardar 1–2 minutos la primera vez.

4. **Comprobar en terminal**
   - Abre **Terminal** (o iTerm) y ejecuta:
   ```bash
   docker --version
   docker compose version
   ```
   - Deben aparecer versiones. Si no, cierra y vuelve a abrir la terminal o reinicia Docker Desktop.

**Importante:** Cada vez que quieras usar el proyecto, **Docker Desktop debe estar abierto y en estado "Running"** antes de ejecutar `docker compose up`.

---

### Instalar Docker en Windows

1. Descarga **Docker Desktop** desde **https://www.docker.com/products/docker-desktop/** (Download for Windows).
2. Ejecuta el instalador y sigue los pasos (WSL 2 si te lo recomienda).
3. Reinicia si lo pide.
4. Abre **Docker Desktop** desde el menú de inicio y espera a que diga que está en ejecución.
5. En PowerShell o CMD: `docker --version` y `docker compose version`.

---

### Instalar Docker en Linux

Sigue la guía oficial según tu distribución: **https://docs.docker.com/engine/install/**  
Luego instala el plugin Compose o el binario `docker compose`.  
No hace falta "Docker Desktop"; el daemon de Docker se gestiona por sistema.

---

## 2. Comprobar que Docker está en ejecución

Antes de levantar el proyecto:

- **macOS / Windows:** Abre **Docker Desktop** y espera a que el icono indique que está en ejecución. Si no está abierto, `docker compose up` fallará con errores de conexión.
- **Linux:** El servicio Docker suele estar activo; si no: `sudo systemctl start docker`.

Prueba en la terminal:

```bash
docker info
```

Si no da error, Docker está listo.

---

## 3. Estructura del proyecto

Asegúrate de estar en la **raíz del proyecto** (donde está el archivo `docker-compose.yml`). Deben existir:

- `docker-compose.yml`
- `odoo.conf`
- Carpeta `addons/naturalslim_api/` (módulo de Odoo)
- Carpeta `frontend/` (proyecto Vue con `package.json`, `vite.config.ts`, `src/`)

Si has clonado el repositorio, la estructura ya debería estar. Si falta algo, el proyecto no está completo.

---

## 4. Levantar todos los servicios (backend + frontend)

**Desde la raíz del proyecto** (donde está `docker-compose.yml`), en la terminal:

```bash
docker compose up -d
```

(O si tu sistema usa el comando antiguo: `docker-compose up -d`.)

Esto hace lo siguiente:

- Descarga las imágenes necesarias (PostgreSQL, Odoo 17, Node 20) si no las tienes.
- Crea y arranca tres contenedores:
  - **db:** base de datos PostgreSQL (solo uso interno).
  - **odoo:** backend Odoo 17 en el puerto **8069**.
  - **frontend:** aplicación Vue en el puerto **5173**.

La primera vez puede tardar varios minutos (descarga de imágenes e `npm install` en el frontend).

**Comprobar que todo está en marcha:**

```bash
docker compose ps
```

Deben aparecer los tres servicios en estado "Up" (o "running").

---

## 5. Configurar Odoo (crear base de datos e instalar el módulo)

1. **Abrir Odoo en el navegador**  
   - URL: **http://localhost:8069**  
   - (Cursor: puedes abrir esta URL en Simple Browser o en tu navegador.)

2. **Crear la base de datos (solo la primera vez)**  
   - Odoo te pedirá:
     - **Master Password:** escribe **`admin`** (está definido en `odoo.conf` del proyecto).
     - **Database Name:** por ejemplo `naturalslim`.
     - **Email** y **Password:** los que quieras para el usuario administrador.
   - Pulsa **Create database** y espera a que cargue.

3. **Instalar el módulo "NaturalSlim API"**  
   - En el menú superior, entra en **Apps** (Aplicaciones).
   - Quita el filtro que muestra solo "Apps" instaladas (para ver todos los módulos).
   - En el buscador escribe **NaturalSlim** o **naturalslim**.
   - Debe aparecer **NaturalSlim API**. Pulsa **Install** (Instalar).
   - Si no aparece: en **Apps**, menú de tres puntos (⋮) → **Update Apps List** → confirmar. Vuelve a buscar **NaturalSlim API** e instala.

4. **(Recomendado) Crear al menos un producto**  
   - Ve a **Ventas → Productos** (o **Inventory → Products**).
   - Crea un producto, márcalo como **Vendible** y guarda.  
   Así la tienda frontend tendrá al menos un producto que mostrar.

---

## 6. Abrir el frontend (tienda)

1. **Abrir la tienda en el navegador**  
   - URL: **http://localhost:5173**  
   - (Cursor: abre esta URL para ver la tienda Vue.)

2. Deberías ver la página **Productos** de NaturalSlim. Si configuraste Odoo y creaste productos, aparecerán en la lista. Puedes usar el buscador y el carrito.

3. **Probar el flujo completo:** agrega un producto al carrito, ve a **Carrito** (icono en la barra) y pulsa **Crear presupuesto en Odoo**. En Odoo, en **Ventas → Pedidos**, debería aparecer el presupuesto creado.

---

## 7. Verificación rápida

| Comprobación | Cómo |
|--------------|------|
| Backend (API) | Abrir **http://localhost:8069/api/products** en el navegador. Debe devolver JSON con `{"products": [...]}`. |
| Frontend | Abrir **http://localhost:5173**. Debe cargar la página sin "Failed to fetch" (si Odoo está arriba y el módulo instalado). |

---

## 8. Alternativa: frontend en local (sin contenedor frontend)

Si prefieres no usar el contenedor del frontend (por ejemplo en Mac sin Docker para el frontend):

1. Levantar solo base de datos y Odoo:
   ```bash
   docker compose up -d db odoo
   ```

2. Tener **Node.js 20** instalado en tu Mac. Descarga desde **https://nodejs.org/** si no lo tienes.

3. En otra terminal, desde la raíz del proyecto:
   ```bash
   cd frontend
   cp .env.example .env
   npm install
   npm run dev
   ```

4. Abrir **http://localhost:5173**. El proxy de Vite enviará las peticiones `/api` a Odoo en `http://localhost:8069`.

---

## 9. Problemas frecuentes

| Problema | Qué hacer |
|----------|-----------|
| "Failed to fetch" en el frontend | El frontend en Docker usa un proxy hacia el servicio `odoo`. Comprueba que en `docker-compose.yml` el servicio `frontend` tenga `VITE_PROXY_TARGET=http://odoo:8069`. Luego: `docker compose restart frontend`. Si el frontend corre en local (`npm run dev`), comprueba que Odoo esté en marcha y que el módulo "NaturalSlim API" esté instalado. Prueba **http://localhost:8069/api/products** en el navegador. |
| "cannot find the file specified" / "error during connect" al hacer `docker compose up` | Docker Desktop no está en ejecución. En Mac/Windows: abre **Docker Desktop** y espera a que esté "Running". Vuelve a ejecutar `docker compose up -d`. |
| No aparece el módulo "NaturalSlim API" en Apps | Ejecuta `docker compose restart odoo`. En Odoo: **Apps** → menú (⋮) → **Update Apps List**. Comprueba que exista la carpeta `addons/naturalslim_api/` con `__manifest__.py`. |
| El frontend no arranca en el contenedor | Revisa los logs: `docker compose logs frontend`. Si falla `npm install` por red o permisos, usa la opción de frontend en local (sección 8). |
| Puerto 8069 o 5173 ya en uso | Cambia en `docker-compose.yml` el mapeo de puertos (por ejemplo `"8070:8069"` para Odoo). Si cambias el puerto de Odoo, en frontend local o en el proxy de Vite tendrás que apuntar a ese puerto. |

---

## 10. Resumen para un agente (Cursor)

- **Requisito obligatorio:** Docker instalado y en ejecución (en Mac/Windows, Docker Desktop debe estar abierto y en estado "Running").
- **Orden de pasos:**  
  1) `docker compose up -d` desde la raíz del proyecto.  
  2) Abrir **http://localhost:8069** → crear base de datos si es la primera vez (Master Password: `admin`) → instalar módulo "NaturalSlim API" desde Apps.  
  3) Opcional: crear al menos un producto vendible en Odoo.  
  4) Abrir **http://localhost:5173** para usar la tienda (frontend).
- **Puertos:** Odoo = **8069**, Frontend = **5173**.
- **URLs para abrir en el navegador (o en Cursor):**  
  - Backend Odoo: **http://localhost:8069**  
  - API de productos: **http://localhost:8069/api/products**  
  - Tienda (frontend): **http://localhost:5173**
- Si el frontend muestra "Failed to fetch", comprobar que Odoo esté en marcha (`docker compose ps`), que el módulo esté instalado y que el servicio `frontend` en `docker-compose.yml` tenga la variable `VITE_PROXY_TARGET=http://odoo:8069`.
