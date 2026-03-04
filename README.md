# NaturalSlim eCommerce Clone

Proyecto fullstack inspirado en **tiendanaturalslim.com**: **Odoo 17** como backend (ERP/base de datos) y **Vue 3** (Vite + TypeScript + Tailwind + Pinia) como frontend.

> **Para levantar el proyecto desde cero** (incluye instalación de Docker, pasos en Odoo y solución de problemas), sigue la guía **[SETUP.md](./SETUP.md)**. Está pensada para que cualquier persona o un agente en Cursor pueda ejecutar el proyecto sin problemas.

## Requisitos

- [Docker](https://www.docker.com/get-started) y Docker Compose
- (Opcional) Node 20+ si quieres ejecutar el frontend en local sin Docker

## Estructura del proyecto

```
naturalslim-clone/
├── addons/
│   └── naturalslim_api/          # Módulo Odoo (API REST)
│       ├── __manifest__.py
│       ├── __init__.py
│       └── controllers/
│           └── main.py           # GET /api/products, POST /api/cart/sync
├── frontend/                     # Vue 3 + Vite + TS + Tailwind + Pinia
│   ├── src/
│   │   ├── api/odoo.ts
│   │   ├── components/           # Navbar, ProductCard
│   │   ├── stores/               # cartStore, searchStore
│   │   ├── views/Home.vue
│   │   └── ...
│   └── package.json
├── docker-compose.yml            # db (Postgres 15), odoo (Odoo 17), frontend (Node 20)
├── odoo.conf
└── README.md
```

## Pasos para levantar el proyecto

### 1. Levantar los servicios con Docker

En la raíz del proyecto:

```bash
docker-compose up -d
```

- **Odoo**: http://localhost:8069  
- **Frontend Vue**: http://localhost:5173  

La primera vez, el contenedor del frontend puede tardar un poco en instalar dependencias (`npm install`) y arrancar el dev server.

### 2. Crear base de datos e instalar el módulo en Odoo

1. Abre **http://localhost:8069** en el navegador.
2. Crea una nueva base de datos:
   - **Master Password**: `admin` (definido en `odoo.conf`).
   - Nombre de la BD, email y contraseña de administrador a tu elección.
3. Una vez dentro de Odoo:
   - Ve a **Apps** (Aplicaciones).
   - Quita el filtro "Apps" y busca **NaturalSlim API**.
   - Haz clic en **Instalar**.
4. (Recomendado) Crea algunos **productos** en *Ventas → Productos* y márcalos como **Vendibles** para que aparezcan en la tienda.

### 3. Probar el frontend

1. Abre **http://localhost:5173**.
2. Deberías ver la lista de productos (si hay en Odoo), el buscador y el ícono del carrito.
3. Agrega productos al carrito y haz clic en el carrito (navbar) para ir a la vista **Carrito**. Ahí puedes opcionalmente indicar nombre/email y pulsar **Crear presupuesto en Odoo** para crear un `sale.order` en el backend.

### 4. Sincronizar carrito con Odoo (Presupuesto)

El carrito en Vue se mantiene en Pinia. Desde la vista **Carrito** se llama a **POST /api/cart/sync**. También puedes crear un **Presupuesto** (sale.order) en Odoo manualmente con:

- Usa el endpoint **POST /api/cart/sync** con un body JSON como:

```json
{
  "lines": [
    { "product_id": 1, "quantity": 2, "price_unit": 29.99 }
  ],
  "partner_email": "cliente@ejemplo.com",
  "partner_name": "Cliente Web"
}
```

Desde el frontend puedes llamar a `cartStore.syncWithBackend(email, name)` cuando el usuario quiera “Enviar pedido” o “Crear presupuesto”.

## Configuración

- **Odoo**: `odoo.conf` en la raíz (addons path incluye `./addons` vía volumen).
- **Frontend**: variable de entorno `VITE_ODOO_API_URL` (por defecto `http://localhost:8069`). En Docker está definida en `docker-compose.yml`; en local puedes usar un `.env` en `frontend/` copiando `frontend/.env.example`.

## Desarrollo local del frontend (sin Docker)

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Asegúrate de que Odoo esté corriendo (por ejemplo solo con `docker-compose up -d db odoo`) y que la URL en `.env` apunte a donde escucha Odoo.

## API expuesta por el módulo Odoo

| Método | Ruta           | Descripción |
|--------|----------------|-------------|
| GET    | `/api/products` | Lista de productos (nombre, precio, imagen, descripción, categoría, stock). |
| POST   | `/api/cart/sync` | Crea un Presupuesto (sale.order) con las líneas enviadas desde el frontend. |

CORS está configurado para permitir peticiones desde `http://localhost:5173`.

## Licencia

Uso interno / educativo. Ajusta según tu proyecto.
