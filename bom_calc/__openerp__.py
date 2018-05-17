# -*- coding: utf-8 -*-
{
    "name": """MRP BoM Drill Down Calc""",
    "summary": """Added support BOM Drill Down Calculation""",
    "category": "manufacturing",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "mrp",

    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'bom_calc_view.xml',
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

