import json, os, csv
from typing import List, Dict, Any

class Companion:
    def __init__(self, content_ID: str, item_ID: int, skin_ID: int, species: str):
        self.content_ID = content_ID
        self.item_ID = item_ID
        self.skin_ID = skin_ID
        self.species = species

class Trait:
    def __init__(self, name: str, num_units: int, style: int, tier_current: int, tier_total: int):
        self.name = name
        self.num_units = num_units
        self.style = style
        self.tier_current = tier_current
        self.tier_total = tier_total

class Unit:
    def __init__(self, character_id: str, itemNames: List[str], name: str, rarity: int, tier: int):
        self.character_id = character_id
        self.itemNames = itemNames
        self.name = name
        self.rarity = rarity
        self.tier = tier

class Participant:
    def __init__(self, augments: List[str], 
                 companion: Companion, 
                 gold_left: int, 
                 last_round: int, 
                 level: int, 
                 missions: Dict[str, int], 
                 placement: int, 
                 players_eliminated: int,
                 puuid: str, riotIdGameName: str, 
                 riotIdTagline: str, 
                 time_eliminated: float, 
                 total_damage_to_players: int, 
                 traits: List[Trait], 
                 units: List[Unit], 
                 win: bool):
        self.augments = augments
        self.companion = companion
        self.gold_left = gold_left
        self.last_round = last_round
        self.level = level
        self.missions = missions
        self.placement = placement
        self.players_eliminated = players_eliminated
        self.puuid = puuid
        self.riotIdGameName = riotIdGameName
        self.riotIdTagline = riotIdTagline
        self.time_eliminated = time_eliminated
        self.total_damage_to_players = total_damage_to_players
        self.traits = traits
        self.units = units
        self.win = win

class Metadata:
    def __init__(self, data_version: str, match_id: str, participants: List[str]):
        self.data_version = data_version
        self.match_id = match_id
        self.participants = participants

class Info:
    def __init__(self, endOfGameResult: str, gameCreation: int, gameId: int, game_datetime: int, game_length: float, game_version: str, mapId: int, participants: List[Participant], queueId: int, queue_id: int, tft_game_type: str, tft_set_core_name: str, tft_set_number: int):
        self.endOfGameResult = endOfGameResult
        self.gameCreation = gameCreation
        self.gameId = gameId
        self.game_datetime = game_datetime
        self.game_length = game_length
        self.game_version = game_version
        self.mapId = mapId
        self.participants = participants
        self.queueId = queueId
        self.queue_id = queue_id
        self.tft_game_type = tft_game_type
        self.tft_set_core_name = tft_set_core_name
        self.tft_set_number = tft_set_number

class MatchData:
    def __init__(self, metadata: Metadata, info: Info):
        self.metadata = metadata
        self.info = info

    @staticmethod
    def from_json(data: Dict[str, Any]) -> 'MatchData':
        metadata = Metadata(**data['metadata'])
        participants = [Participant(
            augments=p['augments'],
            companion=Companion(**p['companion']),
            gold_left=p['gold_left'],
            last_round=p['last_round'],
            level=p['level'],
            missions=p['missions'],
            placement=p['placement'],
            players_eliminated=p['players_eliminated'],
            puuid=p['puuid'],
            riotIdGameName=p['riotIdGameName'],
            riotIdTagline=p['riotIdTagline'],
            time_eliminated=p['time_eliminated'],
            total_damage_to_players=p['total_damage_to_players'],
            traits=[Trait(**t) for t in p['traits']],
            units=[Unit(**u) for u in p['units']],
            win=p['win']
        ) for p in data['info']['participants']]
        info = Info(
            endOfGameResult=data['info']['endOfGameResult'],
            gameCreation=data['info']['gameCreation'],
            gameId=data['info']['gameId'],
            game_datetime=data['info']['game_datetime'],
            game_length=data['info']['game_length'],
            game_version=data['info']['game_version'],
            mapId=data['info']['mapId'],
            participants=participants,
            queueId=data['info']['queueId'],
            queue_id=data['info']['queue_id'],
            tft_game_type=data['info']['tft_game_type'],
            tft_set_core_name=data['info']['tft_set_core_name'],
            tft_set_number=data['info']['tft_set_number']
        )
        return MatchData(metadata, info)

    def write_participants_to_csv(self, filename: str):
        file_exists = os.path.isfile(filename)
        
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Escreve o cabeçalho apenas se o arquivo ainda n eiste na pasta
            if not file_exists:
                header = [f'character_{i+1}' for i in range(12)] + ['placement', 'win']
                writer.writerow(header)
            
            for participant in self.info.participants:
                row = [unit.character_id for unit in participant.units]
                
                # Preenche com strings vazias se houver menos de 12 characters
                row += [''] * (12 - len(row))
                
                # Adiciona placement e win
                row.append(participant.placement)
                row.append(1 if participant.placement == 1 else 0)
                
                writer.writerow(row)