# -*- coding: utf-8 -*-

import base64
import json
from odoo import http
from odoo.http import request, Response


# Orígenes permitidos para CORS (frontend Vue en desarrollo, cualquier puerto localhost)
CORS_ORIGINS = (
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5180",
    "http://localhost:5182",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5180",
    "http://127.0.0.1:5182",
)


def _get_cors_headers(origin=None):
    """Cabeceras CORS; si origin es localhost o 127.0.0.1, lo permitimos (cualquier puerto)."""
    allow_origin = "http://localhost:5173"
    if origin and ("localhost" in origin or "127.0.0.1" in origin):
        allow_origin = origin
    elif origin and origin in CORS_ORIGINS:
        allow_origin = origin
    return {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400",
    }


def _apply_cors_headers(response_headers, request=None):
    """Añade cabeceras CORS a una lista de cabeceras (tuplas)."""
    origin = None
    if request and request.httprequest:
        origin = request.httprequest.headers.get("Origin")
    for key, value in _get_cors_headers(origin).items():
        response_headers.append((key, value))
    return response_headers


def _product_has_image(product):
    """True si el producto o su plantilla tiene imagen."""
    if product.image_1920:
        return True
    if product.product_tmpl_id and product.product_tmpl_id.image_1920:
        return True
    return False


def _product_image_raw(product):
    """Obtiene los bytes de la imagen (producto o plantilla). None si no hay."""
    raw = product.image_1920
    if not raw and product.product_tmpl_id:
        raw = product.product_tmpl_id.image_1920
    return raw


def _is_image_magic_bytes(data):
    """True si data empieza por cabecera de imagen conocida (JPEG, PNG, GIF)."""
    if not data or len(data) < 2:
        return False
    if data[:2] == b"\xff\xd8":
        return True  # JPEG
    if len(data) >= 8 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return True  # PNG
    if len(data) >= 6 and data[:6] in (b"GIF87a", b"GIF89a"):
        return True  # GIF
    return False


def _raw_to_image_bytes(raw):
    """
    Convierte el valor de image_1920 de Odoo (bytes, str base64, bytearray, etc.) a bytes.
    En algunos entornos Odoo devuelve bytes que son base64 en ASCII (ej. b'/9j/4AAQ...');
    en ese caso hay que decodificar una vez para obtener la imagen real.
    Devuelve (image_bytes, content_type) o (None, None) si falla.
    """
    if not raw:
        return None, None
    try:
        if isinstance(raw, bytes):
            image_bytes = raw
            # Si son bytes pero no son cabecera de imagen, pueden ser base64 en ASCII (Odoo)
            if not _is_image_magic_bytes(image_bytes):
                try:
                    b64_str = image_bytes.decode("utf-8").strip().replace("\r", "").replace("\n", "")
                    if b64_str and len(b64_str) % 4 in (0, 2):  # longitud típica de base64
                        decoded = base64.b64decode(b64_str)
                        if decoded and _is_image_magic_bytes(decoded):
                            image_bytes = decoded
                except Exception:
                    pass
        elif isinstance(raw, bytearray):
            image_bytes = bytes(raw)
            if not _is_image_magic_bytes(image_bytes):
                try:
                    b64_str = image_bytes.decode("utf-8").strip().replace("\r", "").replace("\n", "")
                    if b64_str and len(b64_str) % 4 in (0, 2):
                        decoded = base64.b64decode(b64_str)
                        if decoded and _is_image_magic_bytes(decoded):
                            image_bytes = decoded
                except Exception:
                    pass
        elif isinstance(raw, (memoryview,)):
            image_bytes = bytes(raw)
        elif isinstance(raw, str):
            b64 = raw.strip().replace("\r", "").replace("\n", "")
            image_bytes = base64.b64decode(b64)
        else:
            try:
                s = str(raw).strip().replace("\r", "").replace("\n", "")
                image_bytes = base64.b64decode(s)
            except Exception:
                image_bytes = bytes(raw)
        if not image_bytes:
            return None, None
        if len(image_bytes) >= 8 and image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
            return image_bytes, "image/png"
        if len(image_bytes) >= 2 and image_bytes[:2] == b"\xff\xd8":
            return image_bytes, "image/jpeg"
        if len(image_bytes) >= 6 and image_bytes[:6] in (b"GIF87a", b"GIF89a"):
            return image_bytes, "image/gif"
        return image_bytes, "image/jpeg"
    except Exception:
        return None, None


class NaturalSlimAPI(http.Controller):
    """Controlador de la API REST para el eCommerce NaturalSlim."""

    @http.route("/api/products", type="http", auth="public", methods=["GET"], csrf=False)
    def api_products(self, **kwargs):
        """
        GET /api/products
        Devuelve lista de productos: nombre, precio, imagen_1920, descripción, categoría, stock.
        """
        if request.httprequest.method == "OPTIONS":
            return Response(
                status=204,
                headers=_apply_cors_headers([], request),
            )

        try:
            ProductProduct = request.env["product.product"].sudo()
            products = ProductProduct.search([
                ("sale_ok", "=", True),
            ], order="name asc")

            result = []
            for product in products:
                # Imagen: se sirve por URL en GET /api/product/<id>/image (sin base64 en JSON)
                image_url = f"/api/product/{product.id}/image" if _product_has_image(product) else None

                category_name = ""
                if product.categ_id:
                    category_name = product.categ_id.name or ""

                free_qty = 0.0
                if "qty_available" in product._fields:
                    free_qty = product.qty_available

                result.append({
                    "id": product.id,
                    "name": product.name or "",
                    "list_price": product.list_price,
                    "image_url": image_url,
                    "description_sale": (product.description_sale or "").strip() or (product.description or "").strip() or "",
                    "category": category_name,
                    "stock": free_qty,
                })

            body = json.dumps({"products": result})
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers, request)
            return Response(body, status=200, headers=headers)
        except Exception as e:
            body = json.dumps({
                "products": [],
                "error": str(e),
            })
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers, request)
            return Response(body, status=200, headers=headers)

    @http.route("/api/product/<int:product_id>/image", type="http", auth="public", methods=["GET", "OPTIONS"], csrf=False)
    def api_product_image(self, product_id, **kwargs):
        """
        GET /api/product/<id>/image
        Devuelve la imagen del producto como binario. Usa imagen de la plantilla si la variante no tiene.
        """
        def cors_headers():
            h = []
            _apply_cors_headers(h, request)
            return h

        if request.httprequest.method == "OPTIONS":
            return Response(status=204, headers=cors_headers())

        try:
            ProductProduct = request.env["product.product"].sudo()
            product = ProductProduct.browse(product_id)
            if not product.exists():
                return Response(status=404, headers=cors_headers())

            raw = _product_image_raw(product)
            if not raw:
                return Response(status=404, headers=cors_headers())

            image_bytes, content_type = _raw_to_image_bytes(raw)
            if not image_bytes or not content_type:
                return Response(status=404, headers=cors_headers())

            headers = [
                ("Content-Type", content_type),
                ("Cache-Control", "public, max-age=86400"),  # 1 día
            ]
            _apply_cors_headers(headers, request)
            return Response(image_bytes, status=200, headers=headers)
        except Exception:
            return Response(status=500, headers=cors_headers())

    @http.route("/api/cart/sync", type="http", auth="public", methods=["POST", "OPTIONS"], csrf=False)
    def api_cart_sync(self, **kwargs):
        """
        POST /api/cart/sync (body JSON)
        Recibe el carrito desde Vue y crea un sale.order (Presupuesto) en Odoo.
        Body esperado: { "lines": [ { "product_id": int, "quantity": float, "price_unit": float }, ... ], "partner_email": str (opcional), "partner_name": str (opcional) }
        """
        if request.httprequest.method == "OPTIONS":
            return Response(status=204, headers=_apply_cors_headers([], request))

        try:
            payload = json.loads(request.httprequest.get_data(as_text=True) or "{}")
        except json.JSONDecodeError:
            body = json.dumps({"success": False, "message": "JSON inválido.", "order_id": None})
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers, request)
            return Response(body, status=400, headers=headers)

        lines = payload.get("lines") or []
        partner_email = payload.get("partner_email") or ""
        partner_name = payload.get("partner_name") or "Cliente Web"

        if not lines:
            body = json.dumps({"success": False, "message": "El carrito está vacío.", "order_id": None})
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers, request)
            return Response(body, status=400, headers=headers)

        SaleOrder = request.env["sale.order"].sudo()
        Partner = request.env["res.partner"].sudo()

        partner = Partner.browse()
        if partner_email:
            partner = Partner.search([("email", "=", partner_email)], limit=1)
        if not partner:
            partner = Partner.search([("name", "=", "Public User")], limit=1)
        if not partner:
            partner = Partner.create({
                "name": partner_name or "Cliente Web",
                "email": partner_email or False,
            })

        order_lines = []
        for line in lines:
            product_id = line.get("product_id")
            qty = float(line.get("quantity") or 1)
            price_unit = float(line.get("price_unit") or 0)
            if not product_id or qty <= 0:
                continue
            order_lines.append((0, 0, {
                "product_id": int(product_id),
                "product_uom_qty": qty,
                "price_unit": price_unit,
            }))

        if not order_lines:
            body = json.dumps({"success": False, "message": "No hay líneas válidas en el carrito.", "order_id": None})
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers, request)
            return Response(body, status=400, headers=headers)

        order_vals = {
            "partner_id": partner.id,
            "order_line": order_lines,
            "origin": "NaturalSlim eCommerce",
        }
        order = SaleOrder.create(order_vals)

        result = {
            "success": True,
            "message": "Presupuesto creado correctamente.",
            "order_id": order.id,
            "order_name": order.name,
        }
        body = json.dumps(result)
        headers = [("Content-Type", "application/json")]
        _apply_cors_headers(headers, request)
        return Response(body, status=200, headers=headers)
