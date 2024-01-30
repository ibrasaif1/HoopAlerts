# import requests

# # Replace with your actual API URL and key
# api_url = "https://api.sportradar.us/nba/trial/v7/en/games/20adc0dd-2579-445a-9f06-a5420b648645/pbp.json?api_key=ak3f6srtfgb2t8p4evdsyc52"

# response = requests.get(api_url)
# data = response.json()

# # Replace this with the name of the player you're looking for
# target_player_name = "Gordon Hayward"

# event_count = 0

# for period in data.get("periods", []):
#     quarter_number = period.get("number")
#     for event in period.get("events", []):
#         if event.get("event_type") == "lineupchange":
#             time_left = event.get("clock_decimal")
#             for side in ['home', 'away']:
#                 players = event.get("on_court", {}).get(side, {}).get("players", [])
#                 for player in players:
#                     if player.get("full_name") == target_player_name:
#                         if quarter_number == 1:
#                             print(f"{target_player_name} has been substituted into the game with {time_left} in the {quarter_number}st quarter")
#                         elif quarter_number == 2:
#                             print(f"{target_player_name} has been substituted into the game with {time_left} in the {quarter_number}nd quarter")
#                         elif quarter_number == 3:
#                             print(f"{target_player_name} has been substituted into the game with {time_left} in the {quarter_number}rd quarter")
#                         elif quarter_number == 4:
#                             print(f"{target_player_name} has been substituted into the game with {time_left} in the {quarter_number}th quarter")
#                         event_count += 1

# print(event_count, "events")

import requests

api_url = "https://api.sportradar.us/nba/trial/v7/en/games/20adc0dd-2579-445a-9f06-a5420b648645/pbp.json?api_key=ak3f6srtfgb2t8p4evdsyc52"

response = requests.get(api_url)
data = response.json()

target_player_name = "Gordon Hayward"
event_count = 0

for period in data.get("periods", []):
    quarter_number = period.get("number")
    players_on_court = set()  # Initialize with the starting lineup if known

    for event in period.get("events", []):
        if event.get("event_type") == "lineupchange":
            new_lineup = set()
            for side in ['home', 'away']:
                players = event.get("on_court", {}).get(side, {}).get("players", [])
                for player in players:
                    new_lineup.add(player.get("full_name"))

            if target_player_name not in players_on_court and target_player_name in new_lineup:
                # Target player substituted in
                time_left = event.get("clock_decimal")
                if quarter_number == 1:
                    quarter_suffix = "st"
                elif quarter_number == 2:
                    quarter_suffix = "nd"
                elif quarter_number == 3:
                    quarter_suffix = "rd"
                elif quarter_number == 4:
                    quarter_suffix = "th"
                print(f"{target_player_name} has been substituted into the game with {time_left} left in the {quarter_number}{quarter_suffix} quarter")
                event_count += 1

            players_on_court = new_lineup  # Update the players on court

print(event_count, "substitution events for", target_player_name)