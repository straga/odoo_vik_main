# -*- coding: utf-8 -*-
{
    "name": """Product Price List Tab""",
    "summary": """Added support Price List Tab in product""",
    "category": "sales",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    'description': """

        =======================

    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "product",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [

        'res_extended_view.xml',
        'data/res_extended_level.xml',
        'wizard/mass_add_price_view.xml',
        'pricelist_tab_view.xml',

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











