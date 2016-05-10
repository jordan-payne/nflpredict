from selenium import webdriver
import requests



def get_gamebooks():
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
