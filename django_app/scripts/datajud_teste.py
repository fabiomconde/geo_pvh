#https://datajud-wiki.cnj.jus.br/api-publica/exemplos/exemplo2
import requests
import json

url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjdft/_search"

payload = json.dumps({
    "query": {
        "bool": {
            "must": [
                {"match": {"classe.codigo": 1116}},
                {"match": {"orgaoJulgador.codigo": 13597}}
            ]
        }
    }
}
)

#Substituir <API Key> pela Chave Pública
headers = {
  'Authorization': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)