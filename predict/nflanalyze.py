# ANALYSIS MODULE FOR NFL PREDICT

import nfldb, nfldbc, nflgame
import json

dbc = nfldbc.dbc

def get_team(team_name):
    with nfldb.Tx(dbc) as cursor:
        cursor.execute('SELECT * FROM team WHERE team_id = %s', [team_name,])
        return cursor.fetchone()

def get_all_teams():
    with nfldb.Tx(dbc) as cursor:
        cursor.execute('SELECT * FROM team;')
        return cursor.fetchall()

def get_stats_categories():
    return nfldb.stat_categories

def fuzzy_search(name, limit=1, team=None, position=None):
    return nfldb.player_search(dbc, name, limit=limit, team=team, position=position)

def get_player(last_name, first_name, team):
    with nfldb.Tx(dbc) as cursor:
        cursor.execute(
            '''SELECT * FROM player WHERE last_name = %s AND first_name = %s AND team = %s''',
            [last_name,first_name, team])
        player = cursor.fetchone()
        if player == None:
            team = 'UNK'
            cursor.execute(
                '''SELECT * FROM player WHERE last_name = %s AND first_name = %s AND team = %s''',
                [last_name,first_name, team])
            return cursor.fetchone()
        else:
            return player

def get_player_all_time_stats(last_name, first_name, team):
    player = get_player(last_name, first_name, team)
    q = nfldb.Query(dbc)
    q.play_player(player_id=player['player_id'])
    return q.limit(1).as_aggregate()[0]

def get_team_roster(team):
    q = nfldb.Query(dbc)
    players = q.player(team=team, status='Active').as_players()
    return players

def ratio_of_snaps(last_name, first_name, team, year, week):
    browser = webdriver.PhantomJS()
    browser.get('http://nflgsis.com')
    print browser.title
    print dir(browser)
    name_input = browser.find_element_by_name('Name')
    password_input = browser.find_element_by_name('Password')
    login_button = browser.find_element_by_name('Login')
    print name_input
    print password_input
    print login_button
    name_input.send_keys('media')
    password_input.send_keys('media')
    login_button.click()
    accept_button = browser.find_element_by_name('btnAccept')
    print accept_button
    accept_button.click()
    print browser.title
    browser.switch_to_frame('BodyNav')
    year_dropdown = browser.find_element_by_xpath("//select[@name='selectSeason']/option[text()='2015']")
    print year_dropdown
    year_dropdown.click()
    link = browser.find_elements_by_link_text('5')[1]
    link.click()
    # <a href="../2015/Reg/05/56577/Gamebook.pdf" target="_blank">PDF</a>
    browser.switch_to_default_content()
    browser.switch_to_frame('Body')
    gamebook_link = browser.find_element_by_xpath("//a[@href='../2015/Reg/05/56577/Gamebook.pdf']")
    session = requests.Session()
    cookies = browser.get_cookies()

    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get('http://nflgsis.com/2015/Reg/05/56577/Gamebook.pdf')
    print response
    newFileByteArray = bytearray(response.content)
    f = open('gamebook.pdf', 'w')
    f.write(newFileByteArray)
    # gamebook_link.click()
    # print gamebook_link
    browser.quit()
