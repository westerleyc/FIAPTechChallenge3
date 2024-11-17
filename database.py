from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import sqlite3

def create_database():
    Base = declarative_base()

    # Tabela Match
    class Match(Base):
        __tablename__ = 'match'
        match_id = Column(String(50), primary_key=True)
        data_inicio = Column(DateTime, nullable=False)
        duracao = Column(Integer, nullable=False)
        queue_type = Column(String(50), nullable=False)
    
        participants = relationship("MatchParticipant", back_populates="match")

    # Tabela Champion
    class Champion(Base):
        __tablename__ = 'champion'
        champion_id = Column(String(50), primary_key=True)
        nome = Column(String(50), nullable=False)
        chosen = Column(Integer, nullable=False)
        rarity = Column(String(50), nullable=False)
        tier = Column(String(50), nullable=False)

        participants = relationship("MatchParticipant", back_populates="champion")

    # Tabela Summoner
    class Summoner(Base):
        __tablename__ = 'summoner'
        puuid = Column(String(50), primary_key=True)
        summoner_id = Column(String(50), nullable=False)
        summoner_level = Column(Integer, nullable=False)
        name = Column(String(50), nullable=False)
        tier = Column(String(50), nullable=False)
        rank = Column(String(50), nullable=False)
        lp = Column(Integer, nullable=False)
        wins = Column(Integer, nullable=False)
        losses = Column(Integer, nullable=False)
        last_update = Column(DateTime, nullable=False)
    
        participants = relationship("MatchParticipant", back_populates="summoner")

    # Tabela MatchParticipant
    class MatchParticipant(Base):
        __tablename__ = 'match_participant'
        entryId = Column(Integer, primary_key=True, autoincrement=True)
        match_id = Column(String(50), ForeignKey('match.match_id'), nullable=False)
        puuid = Column(String(78), ForeignKey('summoner.puuid'), nullable=False)
        placement = Column(Integer, nullable=False)
        level = Column(Integer, nullable=False)
        rounds_survived = Column(Integer, nullable=False)
        time_eliminated = Column(Float, nullable=False)
        total_dmg_players = Column(Integer, nullable=False)
        players_eliminated = Column(Integer, nullable=False)
        last_round = Column(Integer, nullable=False)
        championId = Column(String(50), ForeignKey('champion.champion_id'), nullable=False)
        trait_tier = Column(String(50), nullable=False)
    
        match = relationship("Match", back_populates="participants")
        champion = relationship("Champion", back_populates="participants")
        summoner = relationship("Summoner", back_populates="participants")

    engine = create_engine('sqlite:///game_data.db')
    Base.metadata.create_all(engine)

    print("Banco de dados criado com sucesso!")

def checa_banco():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tabelas no banco de dados:", tables)
    conn.close()