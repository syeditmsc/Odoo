# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Force HTTPS URL Root',
    'version': '17.0.1.0.0',
    'category': 'Technical',
    'summary': 'Force HTTPS URLs globally by monkey-patching request.httprequest.url_root',
    'description': """
        This module globally overrides the request.httprequest.url_root to always use HTTPS.
        It uses a monkey patch on the request object to force url_root to start with 'https://'.
        This is useful for environments where you want to ensure all URLs are HTTPS.
    """,
    'author': 'Odoo Developer',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'web'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
} 