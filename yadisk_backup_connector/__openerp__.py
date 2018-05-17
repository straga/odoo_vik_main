# -*- coding: utf-8 -*-
{
    "name": """Yandex Disk BackUP Connector""",
    "summary": """Yandex Disk BackUP Connector for BackUP manager""",
    "category": "cron",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    "description": """
    """,

    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        'base_setup', 'yandex_disk', 'backup_manager'
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'yadisk_connector_view.xml',
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





















