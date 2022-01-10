from time import sleep
import getpass

# The selenium.webdriver module provides all the WebDriver implementations. get it online, [I got the module from here][1]
from selenium import webdriver
# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

HEADLESS = True
# USERNAME = "user"
USERNAME = getpass.getuser()
PASSWORD = "rudd"

DOMAIN = "http://" + 'webauth.login'
LOGIN_PORTAL = DOMAIN + "/auth1.html"
AUTH_PAGE = DOMAIN + '/auth.cgi'
HEARTBEAT = DOMAIN + '/usrHeartbeat.cgi'
LOGIN_STATUS = DOMAIN + '/loginStatusTop.html'
DYN_LOGIN_STATUS = DOMAIN + '/dynLoginStatus.html?1stLoad=yes'
LOGOUT = DOMAIN + '/logout.html'

CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = 'chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

DRIVER = None

def get_driver():
    global DRIVER
    if not DRIVER:
        if HEADLESS:
            DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options) #TODO: Singleton driver don't close everytime
        else:
            DRIVER = webdriver.Chrome()
    return DRIVER

def close_driver():
    global DRIVER
    if DRIVER:
        DRIVER.quit()

def login_and_set_time(durration, driver=None):
    if not driver:
        driver = get_driver()
    driver.switch_to.window(driver.window_handles[0])
    driver.get(LOGIN_PORTAL)
    assert "Sonic" in driver.title
    user = driver.find_element_by_name("userName")
    passwd = driver.find_element_by_name("pwd")
    user.send_keys(USERNAME)
    passwd.send_keys(PASSWORD)
    submit = driver.find_element_by_name("Submit")
    submit.click()
    
    driver.switch_to.window(driver.window_handles[1])
    errorText = driver.find_element_by_id("error_text")
    sError=errorText.get_attribute("innerHTML")
    print(f"Error was: {sError}")


    driver.get(LOGIN_STATUS)
    driver.switch_to.frame("loginStatus")
    time = driver.find_element_by_name("sessLimVal")
    time.send_keys(Keys.CONTROL, "a")
    time.send_keys(durration)
    update = driver.find_element_by_name("Update")
    update.click()

def block_connect(driver=None):
    while True:
        durration = '1'
        login_and_set_time(durration, driver)
        sleep(int((int(durration) * 60) / 2))

def logout(driver=None):
    if not driver:
        driver = get_driver()
    driver.get(LOGOUT)
    # close_driver()

if __name__ == "__main__":
    login_and_set_time("1")
    input("Logged. Press cont to logout...")
    logout()
    input("Press any key to Login")
    login_and_set_time("1")
    input("Press any key to logut")
    logout()
