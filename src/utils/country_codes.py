COUNTRY_CODES = {
    "brasil": "55",
    "estados unidos": "1",
    "canada": "1",
    "mexico": "52",
    "argentina": "54",
    "chile": "56",
    "colombia": "57",
    "portugal": "351",
    "espanha": "34",
    "franca": "33",
    "alemanha": "49",
    "italia": "39",
    "inglaterra": "44",
    "japao": "81",
    "china": "86",
    "india": "91",
    "australia": "61",
    "nova zelandia": "64",
    # Adicione mais países e seus códigos de país conforme necessário
}




def get_country_code_from_country(country_name):
    return COUNTRY_CODES.get(country_name.lower(), "")

