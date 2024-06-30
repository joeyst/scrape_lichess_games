Appends all games played after the date of the latest game in local PGN file at provided path. 

If file at provided path doesn't exist, creates empty file and downloads all games from user. 

Example: 
```python
from scrape_lichess_games import scrape_lichess_games 
scrape_lichess_games("joeyst.pgn", "joeyst")
```

Install: 

`python -m pip install -U git+https://github.com/joeyst/scrape_lichess_games.git`