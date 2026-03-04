# -*- coding: utf-8 -*-
{
    "name": "NaturalSlim API",
    "version": "17.0.1.0.0",
    "category": "Website",
    "summary": "API REST para integración con frontend Vue (eCommerce NaturalSlim)",
    "description": """
        Expone endpoints para:
        - GET /api/products: Lista de productos con nombre, precio, imagen, descripción, categoría y stock.
        - POST /api/cart/sync: Sincroniza carrito desde Vue y crea Presupuesto (sale.order) en Odoo.
    """,
    "author": "NaturalSlim",
    "website": "https://www.naturalslim.com",
    "license": "LGPL-3",
    "depends": ["base", "sale", "product", "stock"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
