# -*- coding: utf-8 -*-
{
    "name": """F - Sale Tax""",
    "summary": """Added support Sale Tax Control""",
    "category": "project",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "base", "f_services"

    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_tax_view.xml',
        'views/res_partner_view.xml'
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





