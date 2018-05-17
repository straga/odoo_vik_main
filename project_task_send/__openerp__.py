# -*- coding: utf-8 -*-
{
    "name": """Project task send""",
    "summary": """Send task over email. When create task.""",
    "category": "project",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "description": """

        =======================

        Send task over email. When create task.
        Create email_template
        Send to assignment (get email from user)
        Subject: Customer : Task name
        Body:
            Task Description
            Context.
    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "project",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
          'task_send_template.xml',
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


















