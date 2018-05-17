# -*- coding: utf-8 -*-
{
    "name": """List URL Field Widget""",
    "summary": """List URL Field Widget""",
    "category": "stuff",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    'description': """

=======================

How it use: widget="ListUrl"
<field name="demander" string="Demander" widget="ListUrl""/>

    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "base",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [ 'views/templates.xml',],
    "qweb": [],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}
