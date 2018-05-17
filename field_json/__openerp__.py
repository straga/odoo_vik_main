# -*- coding: utf-8 -*-
{
    "name": """Json Field Widget""",
    "summary": """Added support Json Field Widget""",
    "category": "stuff",
    "images": ['static/description/icon.png'],
    "version": "1.0.0",

    'description': """

        =======================

        This module adds - Json Field Widget:
        How it use: widget="jsonurl"
        <field name="demander" string="Demander" widget="jsonurl" attrs="{'readonly': 1}"/>

        demander = fields.Char('UoM', compute='_compute_demander')

        data = dict()

        for procurement_id in self.procurement_ids:
            procur_name = procurement_id.name
            procur_qty = procurement_id.product_qty

            if procurement_id.move_dest_id:
                procur_name = procurement_id.move_dest_id.name
                procur_qty = procurement_id.move_dest_id.product_qty


            procur_id = procurement_id.id
            uid_id = procurement_id.create_uid.id
            uid_name = procurement_id.create_uid.name
            uid_model = procurement_id.create_uid._model._name
            uid_partner_id = procurement_id.create_uid.partner_id.id


        data[procur_id] = {

                                "uid_id": uid_id,
                                "uid_model": uid_model,
                                "uid_name": uid_name,
                                "procur_id" : procur_id,
                                "procur_name": procur_name,
                                "procur_qty":  procur_qty,
                                "uid_partner_id" : uid_partner_id
        }

        Json convert: json_str = json.dumps(data)
        Return Json Field: self.demander = json_str


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
    "qweb": [ 'static/src/xml/json.xml',],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}







