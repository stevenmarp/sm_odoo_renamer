# -*- coding: utf-8 -*-
{
    "name": "Odoo Renamer: Fields, Buttons & Tabs",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "summary": "Rename field labels, button texts and tab names without writing a single line of code, globally or per model, per language.",
    "description": """
Odoo Renamer: Fields, Buttons & Tabs
====================================

Rename any field label, button text or notebook tab title from a simple
configuration screen. No code, no view inheritance, no Studio.

* Rename form field labels, button texts and tab titles
* Apply a rename globally or only on a specific model
* Language aware: rename a label in one language without touching the others
* Works with standard and custom modules
* Dedicated "Renamer Manager" access group
* Rules are applied on the fly, original views are never modified
    """,
    "author": "Steven Marp",
    "website": "https://apps.odoo.com/apps/modules/browse?author=Steven Marp",
    "license": "OPL-1",
    "images": [
        "static/description/banner.gif",
        "static/description/icon.png",
        "static/description/renamer_01_rule_config.png",
        "static/description/renamer_02_sale_order_result.png",
    ],
    "depends": ["base", "web"],
    "data": [
        "security/renamer_security.xml",
        "security/ir.model.access.csv",
        "views/renamer_rule_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "price": 150.00,
    "currency": "USD",
}
