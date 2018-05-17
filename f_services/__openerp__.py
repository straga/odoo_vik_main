# -*- coding: utf-8 -*-
{
    "name": """Service Task""",
    "summary": """Added support Service Task Control""",
    "category": "project",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "base",

    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'task_view.xml',
        'res_partner_view.xml',
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




