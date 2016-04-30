from context import nflanalyze


def test_get_team():
    assert nflanalyze.get_team('ARZ') == 'ARZ'
