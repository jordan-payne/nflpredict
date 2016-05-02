from context import nfldbc

# Test database connection
def test_dbc():
    assert nfldbc.dbc != None
