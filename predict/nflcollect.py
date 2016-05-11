from selenium import webdriver
import requests

def main():
    driver = get_driver()
    driver = login_nflgsis(driver)
    for year in range(2006,2016):
        gamebooks = get_gamebooks_for_year(year, driver)
        write_gamebooks(gamebooks)


def get_gamebooks_for_year(year, driver):
    driver.switch_to_default_content()
    driver.switch_to_frame('BodyNav')
    gamebooks = []
    xpath = "//select[@name='selectSeason']/option[text()='%s']" % (year)
    year_dropdown = driver.find_element_by_xpath(xpath)
    year_dropdown.click()
    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    # Do weeks 1-5 seperately due to the structure of the page including pre and post-season
    for week in range(1,6):
        link = driver.find_elements_by_link_text(str(week))[1]
        link.click()
        driver.switch_to_default_content()
        driver.switch_to_frame('Body')
        gamebook_links = driver.find_elements_by_link_text('PDF')
        for l in gamebook_links:
            url = l.get_attribute('href')
            response = session.get(url)
            gamebook = {'url': url, 'content': response.content}
            gamebooks.append(gamebook)
        driver.switch_to_default_content()
        driver.switch_to_frame('BodyNav')
    # Do weeks 1-18
    for week in range(6,18):
        link = driver.find_elements_by_link_text(str(week))[0]
        link.click()
        driver.switch_to_default_content()
        driver.switch_to_frame('Body')
        gamebook_links = driver.find_elements_by_link_text('PDF')
        for l in gamebook_links:
            url = l.get_attribute('href')
            response = session.get(url)
            gamebook = {'url': url, 'content': response.content}
            gamebooks.append(gamebook)
        driver.switch_to_default_content()
        driver.switch_to_frame('BodyNav')
    # Finally get the post-season gamebooks not including all-pro game
    for week in range(1,5):
        link = driver.find_elements_by_link_text(str(week))[2]
        link.click()
        driver.switch_to_default_content()
        driver.switch_to_frame('Body')
        gamebook_links = driver.find_elements_by_link_text('PDF')
        for l in gamebook_links:
            url = l.get_attribute('href')
            response = session.get(url)
            gamebook = {'url': url, 'content': response.content}
            gamebooks.append(gamebook)
        driver.switch_to_default_content()
        driver.switch_to_frame('BodyNav')
    return gamebooks

def write_gamebooks(gamebooks):
    for gamebook in gamebooks:
        filename = derive_gamebook_name(gamebook['url'])+ '.pdf'
        f = open('docs/%s' % (filename), 'w')
        newFileByteArray = bytearray(gamebook['content'])
        f.write(newFileByteArray)
        f.close()

def derive_gamebook_name(url):
    values = url.split('/')
    return str(values[6])


def get_driver():
    return webdriver.PhantomJS()

def login_nflgsis(driver):
    driver.get('http://nflgsis.com')
    name_input = driver.find_element_by_name('Name')
    password_input = driver.find_element_by_name('Password')
    login_button = driver.find_element_by_name('Login')
    name_input.send_keys('media')
    password_input.send_keys('media')
    login_button.click()
    accept_button = driver.find_element_by_name('btnAccept')
    accept_button.click()
    return driver

if __name__ == "__main__":
    main()
