# -*- coding: utf-8 -*-
{
    "name": """Product Reorder Rule""",
    "summary": """Added support - Count Reorder Rule in Product in List View""",
    "category": "product",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "description": """

        =======================
    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "product","stock",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'product_reorder_view.xml',
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














