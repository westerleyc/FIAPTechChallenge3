import requests

def get_puuid_by_summoner_name(api_key, summoner_name, tagline):

    RIOT_API_BASE_URL = "https://americas.api.riotgames.com"
    url = f"{RIOT_API_BASE_URL}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagline}"
    print(url)
    headers = {
        "X-Riot-Token": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('puuid')
    else:
        return {"error": response.status_code, "message": response.text}