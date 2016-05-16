from context import nflscrape

def test_pdfWrapper():
    pdf = nflscrape.pdfWrapper(filename='docs/56834.pdf', scrape_target='PLAYTIME_PERCENTAGE')
    assert pdf != None
    assert pdf.numPages == 1
    assert 'Carolina Panthers' in [v for k,v in pdf.teams.iteritems()]
    pdf = nflscrape.pdfWrapper(filename='docs/56753.pdf', scrape_target='PLAYTIME_PERCENTAGE')
    assert pdf != None
    assert pdf.numPages == 2
    assert 'Kansas City Chiefs' in [v for k,v in pdf.teams.iteritems()]
