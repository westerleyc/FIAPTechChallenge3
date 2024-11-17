import requests

# Global data variables
RIOT_API_BASE_URL = "https://americas.api.riotgames.com"


def get_puuid_by_summoner_name(api_key, summoner_name, tagline):

    url = f"{RIOT_API_BASE_URL}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagline}"
    #print(url)

    headers = {
        "X-Riot-Token": api_key
    }    

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('puuid')
    else:
        return {"error": response.status_code, "message": response.text}

def get_puuid_by_encrypted_summoner_name(api_key, encrypted_summoner_name, tagline):

    url = f"https://{tagline}.api.riotgames.com/tft/summoner/v1/summoners/{encrypted_summoner_name}"
    #print(url)

    headers = {
        "X-Riot-Token": api_key
    }    

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('puuid')
    else:
        return {"error": response.status_code, "message": response.text}

def get_match_list_by_puuid(api_key, puuid, start=0, count=200, start_time=None, end_time=None):

    url = f"{RIOT_API_BASE_URL}/tft/match/v1/matches/by-puuid/{puuid}/ids"
    #print(url)

    headers = {
    "X-Riot-Token": api_key
    }

    params = {
        'start': start,
        'count': count
    }
    if start_time:
        params['startTime'] = start_time
    if end_time:
        params['endTime'] = end_time

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}, {response.text}")
        return None

def get_encrypted_summoner_ids_from_league(api_key, tagline, tier, queue):

    url = f"https://{tagline}.api.riotgames.com/tft/league/v1/{tier}"

    # Cabeçalhos e parametros da requisição
    headers = {
        'X-Riot-Token': api_key
    }
    params = {
        'queue': queue
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        summoner_ids = [entry['summonerId'] for entry in data.get('entries', [])]
        return summoner_ids
    else:
        print(f"Erro: {response.status_code}, {response.text}")
        return []

def get_match_data_by_id(api_key, match_id):
    url = f"{RIOT_API_BASE_URL}/tft/match/v1/matches/{match_id}"
    
    headers = {
        "X-Riot-Token": api_key
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}, {response.text}")
        return None