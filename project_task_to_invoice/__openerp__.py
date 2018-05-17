# -*- coding: utf-8 -*-
{
    "name": """Project Task Materials to Invoice Task""",
    "summary": """Record products over Invoice Tasks in a Task""",
    "category": "project",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "description": """
            It allow ad time spent, material to tasks. After in Invoice Tasks you can put all in Invoice
    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "project", "product"
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
          "project_view.xml",
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


















