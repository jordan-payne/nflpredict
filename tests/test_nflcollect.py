from context import nflcollect

def test_get_driver():
    assert nflcollect.get_driver()

def test_login_nflgsis():
    driver = nflcollect.get_driver()
    driver = nflcollect.login_nflgsis(driver)
    assert driver.title == 'NFL GSIS'

def test_get_gamebooks_for_year():
    driver = nflcollect.get_driver()
    driver = nflcollect.login_nflgsis(driver)
    gamebooks = nflcollect.get_gamebooks_for_year(2014, driver)
    assert gamebooks != None

def test_write_gamebooks():
    driver = nflcollect.get_driver()
    driver = nflcollect.login_nflgsis(driver)
    gamebooks = nflcollect.get_gamebooks_for_year(2014, driver)
    nflcollect.write_gamebooks(gamebooks)

def test_derive_gamebook_name():
    name = nflcollect.derive_gamebook_name('http://nflgsis.com/2014/Reg/01/56170/Gamebook.pdf')
    assert name == '56170'
