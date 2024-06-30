
import os, chess.pgn, datetime, requests 

def get_pgn_iterable(pgn):
  while game := chess.pgn.read_headers(pgn):
    yield game 

def get_number_of_games_in_pgn(path: str) -> int:
  with open(path) as pgn:
    return len(list(get_pgn_iterable(pgn)))

def get_latest_game_datetime(path: str) -> datetime.datetime | None:
  latest_date = None
  with open(path) as pgn:
    while game := chess.pgn.read_headers(pgn):
      if game.get("UTCDate") and game.get("UTCTime"):
        date = datetime.datetime.strptime(game["UTCDate"] + " " + game["UTCTime"], "%Y.%m.%d %H:%M:%S")
        if latest_date is None or date > latest_date:
          latest_date = date
  return latest_date

def get_games_since_datetime(lichess_username: str, datetime: datetime) -> list[chess.pgn.Game]:
  """
  Stored in Games/[lichess_username].png. 
  Gets what the latest local game datetime is. 
  Retrieves games that are after that datetime. 
  """
  if datetime:
    latest_local_in_milliseconds = int(datetime.timestamp()) * 1000
  else:
    latest_local_in_milliseconds = 0
  params = {
    "clocks": True, 
    "tags": True, # E.g. Player1Name = ...
    "ongoing": False, # Do NOT include a current game. 
    "opening": True, 
    "rated": True,
    "since": latest_local_in_milliseconds,
  }
  response = requests.get(f"https://lichess.org/api/games/user/{lichess_username}", params=params)
  response.raise_for_status()
  return response.text

def scrape_lichess_games(path, user, print_status=True):
  # Creating PGN if not exists. 
  if not os.path.exists(path):
    open(path, "w").close()
    
  number_of_games_in_pgn_before = get_number_of_games_in_pgn(path)

  latest_game_datetime = get_latest_game_datetime(path)
  
  since_latest_pgn_text = get_games_since_datetime(user, latest_game_datetime)
    
  with open(path, "a") as f:
    f.write(since_latest_pgn_text)

  # Printing finished + PGN path + number of games in PGN. 
  number_of_games_in_pgn_after = get_number_of_games_in_pgn(path)
  
  if print_status:
    print(f"Successfully downloaded {number_of_games_in_pgn_after - number_of_games_in_pgn_before} new games to PGN.")
    print(f"# games before: {number_of_games_in_pgn_before}")
    print(f"# games after : {number_of_games_in_pgn_after}")
    print(f"Saved to {path}")
    
  return since_latest_pgn_text