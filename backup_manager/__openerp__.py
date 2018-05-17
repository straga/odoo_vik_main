# -*- coding: utf-8 -*-

{
    'name' : 'Automatic BackUp Manager Odoo',
    'version' : '1.0.0',
    'author' : 'Viktor Vorobjov',
    'category': 'Cron',
    'description' : """

        Backup manager for odoo. You can backup any database from diferent servers, to local folder on the server.

        Restore over standart - database manager in odoo.

        Also you can install Yandex Disk connector and back all to yandex disk.
    
    """,
    'website' : 'http://www.prolv.net',
    'depends' : ['base_setup','warning_popup'],
    'data': [
        'abackup_view.xml',
    ],
    'installable': True,
}

