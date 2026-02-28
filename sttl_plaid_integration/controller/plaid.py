from odoo.http import Response
import requests
import json
from odoo import http
from odoo.http import request

# Creating API endpoints. This endpoints will be called from js.
class PlaidController(http.Controller):
    @http.route("/create_link_token", methods=['POST'], auth="user", csrf=False) # Creating link token using API call.
    def create_link_token(self):
        client_id = request.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_client_id')
        secret = request.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_api_secret')
        environment = request.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_environment')
        allowed_countries = request.env.company.plaid_allowed_country_ids
        if not allowed_countries:
            return Response("Please add valid allowed countries for plaid in company settings", status=400, content_type='text/plain')
        allowed_country_codes = allowed_countries.mapped("code")
        if not allowed_country_codes:
            return Response("Please add valid allowed countries for plaid in company settings", status=400, content_type='text/plain')
        if client_id and secret and environment:
            headers = {"Content-type": "application/json"}
            data = {
                "client_id": client_id,
                "secret": secret,
                "client_name": "Odoo Plaid Integration",
                "language": "en",
                "country_codes": allowed_country_codes,
                "user": {
                    "client_user_id": 'user-id'
                },
                "products": ["transactions"]
            }
            response = requests.post(f"https://{environment}.plaid.com/link/token/create",
                                        json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                response_body = json.dumps(response_data)
                return Response(response_body, status=200, content_type='application/json')
            else:
                error_message = "Failed to create link token"
                return Response(error_message, status=response.status_code, content_type='text/plain')
        else:
            error_message = "Please enter plaid client id, secret and environment"
            return Response(error_message, status=400, content_type='text/plain')
            

    @http.route("/exchange_public_token", methods=['POST'], auth="user", csrf=False)  # Exchanging public token for access token.
    def exchange_public_token(self, **params):
        client_id = request.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_client_id')
        secret = request.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_api_secret')
        environment = request.env['ir.config_parameter'].get_param(
            'sttl_plaid_integration.plaid_environment')
        data = {
            "client_id": client_id,
            "secret": secret,
            "public_token": params["public_token"]
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(
            f"https://{environment}.plaid.com/item/public_token/exchange", json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            current = request.env['plaid.bank'].search([('id', '=', params["current"])])
            current.access_token = response_data["access_token"]
            current.status = "connected"
            response_body = json.dumps(response_data)
            self.get_accounts(current, client_id, secret, environment)
            return Response(response_body, status=200, content_type='application/json')
        else:
            error_message = "Failed to get access token. Please make sure you have configured client id, secret and environment correct."
            return Response(error_message, status=response.status_code, content_type='text/plain')


    def get_accounts(self, current, client_id, secret, environment):  # Fetching accounts using API call.
        data = {
            "client_id": client_id,
            "secret": secret,
            "access_token": current.access_token
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(f"https://{environment}.plaid.com/accounts/get", json=data, headers=headers)
        accounts = response.json()["accounts"]
        for account in accounts:
            if account["balances"]["available"]:
                balance = account["balances"]["available"]
            else:
                balance = account["balances"]["current"]
            data = {
                "name": account["name"],
                "account_type": account["subtype"],
                "account_subtype": account["type"],
                "account_id": account["account_id"],
                "balance": balance,
                "currency_id": request.env.company.currency_id.id
            }
            plaid_account_id = request.env["plaid.account"].create(data)
            current.account_ids += plaid_account_id
