# -*- coding: utf-8 -*-
{
    "name": """Purchases order user info""",
    "summary": """Added support shows - who originally made the order.line""",
    "category": "Project",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",
    "description": """
        Possible information - who originally made the order.line

    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",
    "price": 10.00,
    "currency": "EUR",

    "depends": [
        'base_setup',
        'product',
        'purchase',
        'field_json'
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
         'purchase_order_view.xml',
    ],
    "qweb": [],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}
