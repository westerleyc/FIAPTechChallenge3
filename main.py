from flask import Flask, jsonify, request
from riot_api import get_puuid_by_summoner_name

app = Flask(__name__)

RIOT_API_KEY = "RGAPI-9f02381c-9d6d-49f4-96f9-d1e18d9742e1"

summoner_name = "Donkey Shot"
tagline = "BR1"

puuid = get_puuid_by_summoner_name(RIOT_API_KEY, summoner_name, tagline)
print(f"PUUID do jogador {summoner_name}: {puuid}")

if __name__ == '__main__':
    app.run(debug=True)