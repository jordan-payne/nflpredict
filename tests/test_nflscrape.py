from context import nflscrape
import itertools

def test_pdfWrapper():
    pdf = nflscrape.pdfWrapper(filename='docs/56834.pdf', scrape_target='PLAYTIME_PERCENTAGE')
    assert pdf != None
    assert pdf.numPages == 1
    assert 'Carolina Panthers' in [v for k,v in pdf.teams.iteritems()]
    assert 'Remmers' in pdf.rosters['team1'][1][1]
    assert 'E' in pdf.rosters['team2'][0][0]
    assert 'T' == pdf.positions['team1'][0]
    assert 'G' == pdf.positions['team2'][0]
    assert 'Oher' in pdf.rows['team1'][0].text()

    pdf = nflscrape.pdfWrapper(filename='docs/56753.pdf', scrape_target='PLAYTIME_PERCENTAGE')
    assert pdf != None
    assert pdf.numPages == 2
    assert 'Kansas City Chiefs' in [v for k,v in pdf.teams.iteritems()]
    assert 'Crabtree' in pdf.rosters['team1'][6][1]
    assert 'J' in pdf.rosters['team2'][0][0]
    assert 'QB' == pdf.positions['team1'][3]
    assert 'WR' == pdf.positions['team2'][17]
