import requests

# API Key and Player Information
API_KEY = 'RGAPI-2503cbec-7477-41d9-b277-4839a8793f56'  # Replace with your Riot API key
GAME_NAME = 'kARMa'  # Replace with the player's game name
TAG_LINE = 'XTXT'  # Replace with the player's tagline

# Step 1: Get PUUID from Asia server
def get_puuid(game_name, tag_line, api_key):
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        print("PUUID retrieved successfully")
        return response.json()['puuid']
    else:
        print("Error fetching PUUID:", response.status_code, response.json())
        return None

# Step 2: Get Match History from Asia server
def get_match_history(puuid, api_key):
    url = f"https://ap.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Match history retrieved successfully")
        return response.json()['history']  # Returns list of match history
    else:
        print("Error fetching match history:", response.status_code, response.json())
        return None

# Step 3: Get Match Details from Asia server
def get_match_details(match_id, api_key):
    url = f"https://asia.api.riotgames.com/val/match/v1/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Match details for {match_id} retrieved successfully")
        return response.json()  # Returns detailed match data
    else:
        print(f"Error fetching match details for {match_id}:", response.status_code, response.json())
        return None

# Example usage
def main():
    # Get the PUUID for the player
    puuid = get_puuid(GAME_NAME, TAG_LINE, API_KEY)
    if puuid:
        # Get the match history for the player
        match_history = get_match_history(puuid, API_KEY)
        if match_history:
            # Loop through the match history and get detailed stats for each match
            for match in match_history:
                match_id = match['matchId']
                match_details = get_match_details(match_id, API_KEY)
                if match_details:
                    print(match_details)  # Print out detailed match data for each match

if __name__ == "__main__":
    main()