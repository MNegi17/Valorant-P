import boto3
import json
import csv
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from botocore.exceptions import ClientError
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Initialize Bedrock client
bedrock = boto3.client('bedrock')
bedrock_runtime = boto3.client('bedrock-runtime')
s3 = boto3.client('s3')

# Constants
BUCKET_NAME = 'your-s3-bucket-name'
ROLE_ARN = 'arn:aws:iam::your-account-id:role/your-role-name'
MODEL_ID = 'anthropic.claude-v2'

class PlayerAnalytics:
    @staticmethod
    def calculate_impact_score(player) -> float:
        """Calculate an overall impact score for a player based on their stats"""
        weights = {
            'kd_ratio': 0.2,
            'acs': 0.2,
            'mvp': 0.15,
            'first_kills': 0.15,
            'ace': 0.1,
            'clutches': 0.1,
            'hd': 0.1
        }
        
        normalized_stats = {
            'kd_ratio': player.kd_ratio / 2,  # Assuming 2.0 is exceptional
            'acs': player.acs / 300,  # Assuming 300 ACS is exceptional
            'mvp': min(player.MVP / 10, 1),  # Cap at 10 MVPs
            'first_kills': min(player.First_kills / 15, 1),
            'ace': min(player.Ace / 5, 1),
            'clutches': min(player.clutches / 10, 1),
            'hd': player.hd / 100  # Headshot percentage is already 0-100
        }
        
        impact_score = sum(weights[stat] * value for stat, value in normalized_stats.items())
        return round(impact_score * 100, 2)

class Player:
    def __init__(self, name: str, team: str, role: str, kd_ratio: float, acs: float, 
                 MVP: float, First_kills: float, Ace: float, clutches: float, hd: float):
        self.name = name
        self.team = team
        self.role = role
        self.kd_ratio = kd_ratio
        self.acs = acs
        self.MVP = MVP
        self.First_kills = First_kills
        self.Ace = Ace
        self.clutches = clutches
        self.hd = hd
        self.impact_score = PlayerAnalytics.calculate_impact_score(self)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "team": self.team,
            "role": self.role,
            "kd_ratio": self.kd_ratio,
            "acs": self.acs,
            "MVP": self.MVP,
            "First_kills": self.First_kills,
            "Ace": self.Ace,
            "clutches": self.clutches,
            "hd": self.hd,
            "impact_score": self.impact_score
        }

class TeamAnalyzer:
    def __init__(self, players: List[Player]):
        self.players = players
        self.df = pd.DataFrame([player.to_dict() for player in players])

    def get_top_players(self, metric: str, n: int = 5) -> pd.DataFrame:
        """Get top n players based on a specific metric"""
        return self.df.nlargest(n, metric)[['name', 'team', 'role', metric]]

    def suggest_team_composition(self) -> Dict:
        """Suggest optimal team composition based on impact scores and roles"""
        roles = ['Duelist', 'Controller', 'Sentinel', 'Initiator']
        best_team = {}
        
        for role in roles:
            role_players = self.df[self.df['role'] == role]
            if not role_players.empty:
                best_player = role_players.nlargest(1, 'impact_score').iloc[0]
                best_team[role] = {
                    'name': best_player['name'],
                    'team': best_player['team'],
                    'impact_score': best_player['impact_score']
                }
        
        return best_team

def load_player_data(file_path: str) -> List[Player]:
    players = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = Player(
                name=row['Name'],
                team=row['Team'],
                role=row['Role'],
                kd_ratio=float(row['K/D Ratio']),
                acs=float(row['ACS']),
                MVP=float(row['Match MVP(s)']),
                First_kills=float(row['First Kills']),
                Ace=float(row['Aces']),
                clutches=float(row['Clutches']),
                hd=float(row['Headshot Percentage'])
            )
            players.append(player)
    return players

def process_query(query: str, team_analyzer: TeamAnalyzer) -> str:
    """Process specific types of queries with data analysis"""
    query_lower = query.lower()
    
    if "top" in query_lower and any(stat in query_lower for stat in ["kd", "acs", "mvp", "kills", "ace"]):
        # Handle top player queries
        if "kd" in query_lower:
            result = team_analyzer.get_top_players("kd_ratio")
            return f"Top players by K/D ratio:\n{result.to_string()}"
        elif "acs" in query_lower:
            result = team_analyzer.get_top_players("acs")
            return f"Top players by ACS:\n{result.to_string()}"
    
    elif "team composition" in query_lower or "best team" in query_lower:
        # Handle team composition queries
        best_team = team_analyzer.suggest_team_composition()
        response = "Suggested optimal team composition:\n"
        for role, player in best_team.items():
            response += f"{role}: {player['name']} (from {player['team']}) - Impact Score: {player['impact_score']}\n"
        return response
    
    # If no specific analysis is matched, use the general query assistant
    return query_assistant(query)

def main():
    print("\nVALORANT Esports Manager Assistant")
    print("Loading player data and initializing analysis tools...")
    
    try:
        players = load_player_data('valorant_player_data.csv')
        team_analyzer = TeamAnalyzer(players)
        upload_to_s3(players)
        knowledge_base_id = create_knowledge_base()
        ingest_data(knowledge_base_id)
        
        print("\nSystem ready! You can ask about:")
        print("- Top players by various metrics (KD, ACS, MVP, etc.)")
        print("- Optimal team compositions")
        print("- Player comparisons and analysis")
        print("Type 'exit' to quit the program.")

        while True:
            user_input = input("\nWhat would you like to know about VALORANT Esports? ")
            if user_input.lower() == 'exit':
                break
            
            response = process_query(user_input, team_analyzer)
            print(f"\nAssistant: {response}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your data file and AWS credentials.")

if __name__ == "__main__":
    main()