# -*- coding: utf-8 -*-
{
    "name": """Sale uom Ext""",
    "summary": """Sale uom Ext""",
    "category": "sale",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "description": """
    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        'product','sale'
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'sale_ext_view.xml',
        'wizard/unit_weight_view.xml',
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
























