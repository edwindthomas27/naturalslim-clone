# -*- coding: utf-8 -*-

import base64
import json
from odoo import http
from odoo.http import request, Response


# Origen permitido para CORS (frontend Vue en desarrollo)
CORS_ORIGIN = "http://localhost:5173"
CORS_HEADERS = {
    "Access-Control-Allow-Origin": CORS_ORIGIN,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
}


def _apply_cors_headers(response_headers):
    """Añade cabeceras CORS a una lista de cabeceras (tuplas)."""
    for key, value in CORS_HEADERS.items():
        response_headers.append((key, value))
    return response_headers


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
                headers=_apply_cors_headers([]),
            )

        ProductProduct = request.env["product.product"].sudo()
        products = ProductProduct.search([
            ("sale_ok", "=", True),
        ], order="name asc")

        result = []
        for product in products:
            # Imagen en base64 para evitar CORS con otro dominio; si no hay imagen, null
            image_data = None
            if product.image_1920:
                image_data = base64.b64encode(product.image_1920).decode("utf-8")

            # Categoría (primera categoría del producto)
            category_name = ""
            if product.categ_id:
                category_name = product.categ_id.name or ""

            # Stock disponible (si el módulo stock está instalado)
            free_qty = 0.0
            if "qty_available" in product._fields:
                free_qty = product.qty_available

            result.append({
                "id": product.id,
                "name": product.name or "",
                "list_price": product.list_price,
                "image_1920": image_data,
                "description_sale": (product.description_sale or "").strip() or (product.description or "").strip() or "",
                "category": category_name,
                "stock": free_qty,
            })

        body = json.dumps({"products": result})
        headers = [("Content-Type", "application/json")]
        _apply_cors_headers(headers)
        return Response(body, status=200, headers=headers)

    @http.route("/api/cart/sync", type="http", auth="public", methods=["POST", "OPTIONS"], csrf=False)
    def api_cart_sync(self, **kwargs):
        """
        POST /api/cart/sync (body JSON)
        Recibe el carrito desde Vue y crea un sale.order (Presupuesto) en Odoo.
        Body esperado: { "lines": [ { "product_id": int, "quantity": float, "price_unit": float }, ... ], "partner_email": str (opcional), "partner_name": str (opcional) }
        """
        if request.httprequest.method == "OPTIONS":
            return Response(status=204, headers=_apply_cors_headers([]))

        try:
            payload = json.loads(request.httprequest.get_data(as_text=True) or "{}")
        except json.JSONDecodeError:
            body = json.dumps({"success": False, "message": "JSON inválido.", "order_id": None})
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers)
            return Response(body, status=400, headers=headers)

        lines = payload.get("lines") or []
        partner_email = payload.get("partner_email") or ""
        partner_name = payload.get("partner_name") or "Cliente Web"

        if not lines:
            body = json.dumps({"success": False, "message": "El carrito está vacío.", "order_id": None})
            headers = [("Content-Type", "application/json")]
            _apply_cors_headers(headers)
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
            _apply_cors_headers(headers)
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
        _apply_cors_headers(headers)
        return Response(body, status=200, headers=headers)
