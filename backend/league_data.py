""" Module to fetch data from the Riot Games API """

import requests
from datetime import datetime

QUEUE_TYPES = {"Ranked": [420],
               "Flex": [440],
               "Aram": [100, 450],
               "Normal": [400, 430],
               "Arena": [1700]}


def get_player_puuid(user_settings):
    """ Will return the puuid based on riot id """

    # get player and tag through settings
    player_name = user_settings["RiotId"].split("#")[0]
    player_tag = user_settings["RiotId"].split("#")[1]
    api_key = user_settings["Riot Games API Key"]
    url_to_puuid = (f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player_name}/{player_tag}?"
                    f"api_key={api_key}")
    try:
        resp = requests.get(url_to_puuid)
        resp.raise_for_status()
        puuid = resp.json()["puuid"]
        return puuid
    except requests.RequestException:
        print("\033[91m Error while fetching puuid \033[0m")


def create_player_base_data_dict(user_settings):
    """ Will return the base_data_dict -> contains most important ids """

    api_key = user_settings["Riot Games API Key"]
    puuid = get_player_puuid(user_settings)

    url_player_data = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"

    try:
        resp = requests.get(url_player_data)
        resp.raise_for_status()
        player_base_data = resp.json()
    except requests.RequestException:
        print("\033[91m Error while fetching Player Base Data \033[0m")
        return

    summoner_id = player_base_data["id"]

    base_data_dict = {
        "puuid": puuid,
        "summoner_id": summoner_id
    }
    return base_data_dict


def get_recent_match_ids(puuid, user_settings):
    """ Returns recent match ids """

    api_key = user_settings["Riot Games API Key"]

    match_id_url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20"
                    f"&api_key={api_key}")
    try:
        resp = requests.get(match_id_url)
        resp.raise_for_status()
        match_ids = resp.json()
    except requests.RequestException:
        print("\033[91m Error while fetching Match ID Data \033[0m")
        return []
    recent_match_ids = []
    for match_id in match_ids:
        recent_match_ids.append(match_id)
    return recent_match_ids


def get_recent_matches(match_ids, user_settings):
    """ Returns the match data of the last 20 matches

    This function does 20 API calls to the Riot Games API -> is only called ONCE in the program
    """

    api_key = user_settings["Riot Games API Key"]
    base_url_match_data = f"https://europe.api.riotgames.com/lol/match/v5/matches/"

    # if there was an error fetching the match_ids, return
    if not match_ids:
        return []

    full_match_data_list = []
    for match_id in match_ids:
        curr_match_url = base_url_match_data + match_id + f"?api_key={api_key}"
        try:
            resp = requests.get(curr_match_url)
            resp.raise_for_status()
            match_info = resp.json()
        except requests.RequestException:
            print("\033[91m Error while fetching League Match Data \033[0m")
            return []

        full_match_data_list.append(match_info)
    return full_match_data_list


def create_matches_dict(user_settings, player_base_data):
    """ Creates a dictionary which contains the most important data about matches """

    puuid = player_base_data["puuid"]
    match_ids = get_recent_match_ids(puuid, user_settings)
    matches = get_recent_matches(match_ids, user_settings)

    matches_dict = {}
    for match in matches:
        if check_if_match_is_valid(match, user_settings):
            add_match_to_matches_dict(match, matches_dict, user_settings)
    return matches_dict


def check_if_match_is_valid(match, user_settings):
    """ Checks if a match is valid """
    queue_type = user_settings["Match Type"]
    player = user_settings["RiotId"].split("#")[0]

    # match time
    match_day, match_hour = convert_game_start_to_datetime(match['info']['gameCreation'])

    # if it is a remake, skip
    if match["info"]["gameDuration"] < 300:
        return False
    # check if the match type is correct
    queue_id = match['info']['queueId']
    if queue_type == "All Modes" or queue_id in QUEUE_TYPES[queue_type]:
        for participant in match['info']['participants']:
            if participant['riotIdGameName'] == player:
                # check if time is correct -> day is from 6AM to 6AM
                if check_time_of_match(match_day, match_hour):
                    return True
    return False


def evaluate_matches_dict(matches_dict, user_settings):
    """ Will evaluate given matches and return wins/losses """

    wins = losses = 0

    for match_id, match_data in matches_dict.items():
        match_day = match_data["match_day"]
        match_hour = match_data["match_hour"]
        queue_type = user_settings["Match Type"]
        if check_time_of_match(match_day, match_hour):
            if queue_type == "All Modes" or matches_dict[match_id]["queue_type"] == queue_type:
                if matches_dict[match_id]["win"]:
                    wins += 1
                else:
                    losses += 1
    return wins, losses


def add_match_to_matches_dict(match, matches_dict, user_settings):
    """ Adds a match to the matches dictionary """

    player = user_settings["RiotId"].split("#")[0]
    match_id = match["metadata"]["matchId"]
    participants = match['info']['participants']
    participant = None
    for summoner in participants:
        if summoner["riotIdGameName"] == player:
            participant = summoner
            break

    match_day, match_hour = convert_game_start_to_datetime(match['info']['gameCreation'])
    queue_type = user_settings["Match Type"]

    # add new entry
    matches_dict[match_id] = {}
    matches_dict[match_id]["win"] = 1 if participant["win"] else 0
    matches_dict[match_id]["match_day"] = match_day
    matches_dict[match_id]["match_hour"] = match_hour
    matches_dict[match_id]["queue_type"] = queue_type


def get_player_rank_data(user_settings, player_base_data):
    """ Returns player rank data like division, rank, lp """

    api_key = user_settings["Riot Games API Key"]
    summoner_id = player_base_data["summoner_id"]
    queue_type = user_settings["Match Type"]
    rank_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"

    try:
        resp = requests.get(rank_url)
        resp.raise_for_status()
        rank_data = resp.json()
    except requests.RequestException:
        print("\033[91m Error while fetching League Rank Data \033[0m")
        return "Unranked", "error", 13

    try:
        division, rank, lp = evaluate_rank_data(queue_type, rank_data)
        return division, rank, lp
    except TypeError:
        print("FETCHING RANK DATA FAILED: PLAYER IS UNRANKED OR THERE IS AN ERROR")
        return "Unranked", "", ""


def evaluate_rank_data(queue_type, rank_data):
    """ Provides rank data for 'get_player_rank_data.py' """

    queue_type = "RANKED_SOLO_5x5" if queue_type == "Ranked" else "RANKED_FLEX_SR"

    for match_type in rank_data:
        if match_type["queueType"] == queue_type:
            division = match_type["tier"]
            rank = match_type["rank"]
            lp = match_type["leaguePoints"]
            return division, rank, lp


def get_latest_match_id(matches_dict):
    """ Returns the latest match_id of a given queue_type """

    if not matches_dict:
        return None

    # return the first entry of the dictionary
    for match in matches_dict:
        return match


def check_time_of_match(match_day, match_hour):
    """ Check if match was played in valid time """

    current_day = datetime.now().day
    current_hour = datetime.now().hour

    if (int(match_day) == current_day and int(match_hour) > 6) or (
            int(match_day) == current_day - 1 and int(match_hour) > 6 >= current_hour >= 0):
        return True
    else:
        return False


def convert_game_start_to_datetime(game_start_timestamp):
    """ Converts game_start to current date """

    game_date = datetime.utcfromtimestamp(game_start_timestamp / 1000)
    day_of_month = game_date.strftime('%d')
    hour = str(int(game_date.strftime('%H')) + 2)

    return day_of_month, hour


def create_initial_player_data(user_settings):
    """ Will create the final dictionary containing information which will be given to Frontend"""

    player = user_settings["RiotId"].split("#")[0]
    player_base_data = create_player_base_data_dict(user_settings)
    matches_dict = create_matches_dict(user_settings, player_base_data)
    recent_match_id = get_latest_match_id(matches_dict)

    # get wins
    wins, losses = evaluate_matches_dict(matches_dict, user_settings)
    if wins + losses == 0:
        session_wr = 0
    else:
        session_wr = round(wins / (wins + losses) * 100, 0)

    # get rank

    division, rank, lp = get_player_rank_data(user_settings, player_base_data)
    division = division.capitalize()

    initial_data_dict = {
        "player": player,
        "most_recent_match_id": recent_match_id,
        "wins": wins,
        "losses": losses,
        "session_wr": session_wr,
        "division": division,
        "rank": rank,
        "lp": lp
    }

    return matches_dict, initial_data_dict


def check_for_new_match(player_data, user_settings):
    """ Will check if there is a new match """

    print(f"CURRENT DATA: {player_data}")
    puuid = get_player_puuid(user_settings)
    # latest match which was already found and played
    latest_match_id_played = player_data["most_recent_match_id"]
    recent_match_ids = get_recent_match_ids(puuid, user_settings)
    # latest match which was not found yet
    latest_match_id_new = recent_match_ids[0]
    if latest_match_id_played is None or latest_match_id_played != latest_match_id_new:
        recent_match_new = get_recent_matches([latest_match_id_new], user_settings)[0]
        if check_if_match_is_valid(recent_match_new, user_settings):
            player_data["most_recent_match_id"] = latest_match_id_new
            print("NEW GAME FOUND")
            return recent_match_new
    print("NO NEW MATCH")
    print("\n")
    return False


def update_player_data(player_data, user_settings, matches_dict, new_match):
    """ Will update the player data and add wins/losses/rank etc... """

    player_base_data = create_player_base_data_dict(user_settings)

    # handle rank
    division, rank, lp = get_player_rank_data(user_settings, player_base_data)

    # handle session stats
    add_match_to_matches_dict(new_match, matches_dict, user_settings)
    wins, losses = evaluate_matches_dict(matches_dict, user_settings)
    if wins + losses == 0:
        session_wr = 0
    else:
        session_wr = round(wins / (wins + losses) * 100, 0)

    player_data["wins"] = wins
    player_data["losses"] = losses
    player_data["division"] = division.capitalize()
    player_data["rank"] = rank
    player_data["lp"] = lp
    player_data["session_wr"] = session_wr
    print(f"UPDATED PLAYER DATA: {player_data}")
