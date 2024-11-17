import time
from matchParticipant import MatchData
from itertools import islice
from flask import Flask, jsonify, request
from riot_api import get_puuid_by_summoner_name, get_match_list_by_puuid, get_encrypted_summoner_ids_from_league, get_puuid_by_encrypted_summoner_name,get_match_data_by_id
import database

app = Flask(__name__)

# Dados globais de teste
RIOT_API_KEY = "RGAPI-827e28ca-a2b0-45ca-9106-7516bd14efa6"
puuid_Donkey_Shot = "fQtyji3v9QOPNwFlY-mJ-4DUHdnH7Ch3jb5VeJU4dYCwlFtjbLnVvOv7wJvcvFEQzyNcMG2YCoecig"
summoner_name = "Donkey Shot"
tagline = "BR1"
league = "master"
queue = "RANKED_TFT"
total_summoners = 100
total_matches_per_summoner = 20

# Função para limitar a taxa de requisições
def rate_limited_getter(getter, *args, **kwargs):
    result = getter(*args, **kwargs)
    time.sleep(120 / 200)  # Limite de 200 requisições a cada 120 segundos
    return result

# Chamadas teste na API

# Recupera puuid pelo nome de invocador
puuid = rate_limited_getter(get_puuid_by_summoner_name, RIOT_API_KEY, summoner_name, tagline)
print(f"PUUID do jogador {summoner_name}: {puuid}")

# Recupera lista de summonerids encriptados
lista_summoners = rate_limited_getter(get_encrypted_summoner_ids_from_league, RIOT_API_KEY, tagline, league, queue)
lista_puuids = []
for summoner in islice(lista_summoners, total_summoners):
    print("Summoner: ", summoner)
    lista_puuids.append(rate_limited_getter(get_puuid_by_encrypted_summoner_name, RIOT_API_KEY, summoner, tagline))

# Monta conjunto de matches pelo puuid
conjunto_de_matches = set()
for puuid in lista_puuids:
    print("puuid: ", puuid)
    lista_matches = rate_limited_getter(get_match_list_by_puuid, RIOT_API_KEY, puuid)
    for matchId in islice(lista_matches, total_matches_per_summoner):
        print("MatchID: ",matchId)
        conjunto_de_matches.add(matchId)

count = total_matches_per_summoner*total_summoners

with open('matches.txt', 'w') as file:
    for match in conjunto_de_matches:        
        file.write(f"{match}\n")
        match_data_json = rate_limited_getter(get_match_data_by_id, RIOT_API_KEY, matchId)
        #TO DO: CHECAR SE O METADATA É NULO E SE O TIPO DE DADOS É "data_version": "6"
        match_data = MatchData.from_json(match_data_json)
        match_data.write_participants_to_csv('participantData.csv')
        print(count)
        count -= 1 # contador pra acompanhar o progresso da execução

print("End")
    

if __name__ == '__main__':
    app.run(debug=True)