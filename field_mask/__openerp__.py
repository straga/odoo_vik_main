# -*- coding: utf-8 -*-
{
    "name": """Char Input Field Mask""",
    "summary": """Char Input Field Mask""",
    "category": "project",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",
    "description": """

        =======================

        This module adds Char Input Field Mask - Widget:

           mask="+(999)-999-999"  //static mask
           mask="9-a{1,3}9{1,3}" //mask with dynamic syntax

           <field name="business_phone"  placeholder="+(999)-999-99-99" widget="mask" mask="+(999)-999-99-99" /> with placeholder
           <field name="business_phone"  widget="mask" mask="+(999)-999-99-99" /> without placeholder


    """,


    "author": "Viktor Vorobjov",
    "license": "LGPL-3",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "base",

    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/templates.xml',
    ],
    "qweb": [ 'static/src/xml/mask.xml',],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}


