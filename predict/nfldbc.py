import nfldb

try:
    dbc = nfldb.connect()
except:
    dbc = None
