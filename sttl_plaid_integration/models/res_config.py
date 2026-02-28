# Configuration fields for plaid.

from odoo import models, fields


class ResConfigInherit(models.TransientModel):
    _inherit = "res.config.settings"

    plaid_client_id = fields.Char(string="Client Id", 
                    config_parameter="sttl_plaid_integration.plaid_client_id")
    plaid_api_secret = fields.Char(string="Secret",
                                   config_parameter="sttl_plaid_integration.plaid_api_secret")
    plaid_environment = fields.Selection([('sandbox', 'Sandbox'), ('development', 'Development'), ('production', 'Production')],
                                         config_parameter="sttl_plaid_integration.plaid_environment")
