import requests

def buscar_endereco_por_cep(cep: str) -> dict:
    """Consulta a API ViaCEP e retorna os dados do endereço"""
    cep = cep.replace("-", "").strip()

    if len(cep) != 8 or not cep.isdigit():
        raise ValueError("CEP inválido. Deve conter 8 dígitos.")

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code != 200:
        raise ConnectionError("Erro ao acessar a API do ViaCEP.")

    dados = response.json()
    
    if "erro" in dados:
        raise ValueError("CEP não encontrado na base do ViaCEP.")

    return dados
