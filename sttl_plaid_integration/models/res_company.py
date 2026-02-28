from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    plaid_allowed_country_ids = fields.Many2many("res.country", string="Allowed Countries(Plaid)", help="Enabled countries for plaid")
