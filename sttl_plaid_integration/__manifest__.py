# -*- coding: utf-8 -*-
{
    "name": "Odoo Plaid Integration",
    "version": "17.0.2.0",
    "author": "Silver Touch Technologies Limited",
    "category": "accounting",
    "website": "https://www.silvertouch.com/",
    "description": """
	This module provides you functionality to integrate Plaid with Odoo.
        Fetch Bank accounts, Transactions of those accounts from Plaid to Odoo.
        """,
    "summary": """
    	This module provides you functionality to integrate Plaid with Odoo.
        Fetch Bank accounts, Transactions of those accounts from Plaid to Odoo.
    """,
    "depends": ["account", "base_accounting_kit", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config.xml",
        "views/invoicing_menu.xml",
        "views/plaid_bank.xml",
        "views/res_company_views.xml",
        'views/account_bank_statement.xml',
        "wizard/plaid_transaction_wizard.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sttl_plaid_integration/static/src/js/plaid.js",
            "https://cdn.plaid.com/link/v2/stable/link-initialize.js",
        ],
    },
    "price": 0,
    "currency": "USD",
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "images": ["static/description/banner.png"]
}
