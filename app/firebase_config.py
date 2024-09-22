import os
import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Carregar credenciais do Google Cloud Messaging da variável de ambiente
credentials_json = os.getenv('GOOGLE_CREDENTIALS')
if credentials_json:
    credentials_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
else:
    raise ValueError("Credenciais do Google não encontradas.")

# Agora você pode usar as credenciais conforme necessário em seu código
