# It fetches transactions from plaid using API call and stores it in acocunting bank statements.

from odoo import models, fields
import requests
import datetime
from odoo.exceptions import AccessError, ValidationError

class PlaidTransaction(models.TransientModel):
    _name = "plaid.transaction.wizard"

    bank_id = fields.Many2one("plaid.bank", required=True)
    account_ids = fields.Many2many("plaid.account", required=True)
    from_date = fields.Date("From Date", required=True)
    to_date = fields.Date("To Date", required=True)


    def fetch_transactions(self):
        if self.to_date < self.from_date:
            raise ValidationError("To date must be greater than From date")
        client_id = self.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_client_id')
        secret = self.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_api_secret')
        environment = self.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_environment')
        accounts = []
        if client_id and secret and environment:
            for account in self.account_ids:
                accounts.append(account["account_id"])
            data = {
                "client_id": client_id,
                "secret": secret,
                "access_token": self.bank_id.access_token,
                "options":{
                    "account_ids": accounts
                },
                "start_date": str(self.from_date),
                "end_date": str(self.to_date),
            }
            headers = {"Content-type": "application/json"}
            response = requests.post(f"https://{environment}.plaid.com/transactions/get", json=data, headers=headers)
            if response.status_code == 200:
                transactions = response.json()["transactions"]
            else:
                raise AccessError(f"Error in fetching transactions {response.json()}")

            statement_data = {
                "name": "Plaid/" + str(datetime.date.today()),
                "date": datetime.date.today(),
                "journal_id": self.env["account.journal"].search([('type', '=', 'bank')], limit=1).id,

            }
            statement_id = self.env["account.bank.statement"].create(statement_data)
            transactions_data_list = []
            for transaction in transactions:
                partner_id = self.env["res.partner"].search([("name", "=", transaction["name"])]).id
                if partner_id:
                    partner = partner_id
                else:
                    partner = False
                journal_data = {
                    "date": datetime.date.today(),
                    "state": "draft",
                    "move_type": "entry",
                    "journal_id": self.env["account.journal"].search([('type', '=', 'bank')], limit=1).id,
                    "currency_id": self.env.company.currency_id.id
                    }
                journal_id = self.env["account.move"].create(journal_data)
                transaction_data = {
                    "statement_id": statement_id.id,
                    "currency_id": self.env.company.currency_id.id,
                    "move_id": journal_id.id,
                    "partner_id": partner,
                    "payment_ref": transaction["name"],
                    "amount": transaction["amount"],
                    "date": transaction["date"],
                    "journal_id": self.env["account.journal"].search([('type', '=', 'bank')], limit=1).id,
                    }
                transactions_data_list.append(transaction_data)
            transaction_id = self.env["account.bank.statement.line"].create(transactions_data_list)
        else:
            raise AccessError("Please enter plaid client id, secret and environment")
