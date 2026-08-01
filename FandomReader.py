''' 
FandomReader will access as file that has a link (for a valid fandom page) 
Currently this program is designed for a specific task of mine, however I hope to give the user more freedom with user input for elements and classes

This will send a request to fandom to grab the html on the page, using selenium, therefore an up-to-date chromium is required on the computer running the program

With this, we just need all the table and data nested within it, the rest can be deleted

Packages:
request: https://pypi.org/project/requests/
selenium: https://pypi.org/project/selenium/ - used to automate the process connecting to the web
beautifulsoup: http://pypi.org/project/beautifulsoup4/
'''

from selenium import webdriver

from bs4 import BeautifulSoup

import time
import datetime
import re # keeping this here in case a new to find partial expressions

DELAY = 2 # 2 seconds
CLOUDFLARE_DELAY = 35

WIKI_TYPE = "atos"
END = "/wiki/Special:AllPages"
FANDOM_SPECIAL = f"https://{WIKI_TYPE}.fandom.com"
FULL_STRING = f"{FANDOM_SPECIAL}/{END}"

INCLUDE_GALLERY_PAGES = False
GALLERY_TEXT = "/Gallery"

TYPE = "Citadel_of_" # the substring of the type of page you want | use "" to keep all pages

ELEMENT = "table"

'''
    delay_request will pause actions for a desired amount of time (time_delay)
'''
def delay_request(time_delay: int) -> None:
    time.sleep(time_delay) 

'''
    setup_chrome_drivers will create the webdrivers to start the scraping process
'''
def setup_chrome_drivers():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

'''
    request_page_html will grab the html source and return a 'soupified' version using Beautiful Soup
'''
def request_page_html(page_url: str, driver):
    driver.get(page_url)
    html_soupified = BeautifulSoup(driver.page_source, 'html.parser') 
    return html_soupified

'''
    end_chrome_driver_session will stop the current web driver
'''
def end_chrome_driver_session(driver):
    delay_request(DELAY)
    driver.quit()
    del driver

'''
    get_current_time returns the current date and time
'''
def get_current_time():
    current_timestamp = datetime.datetime.now()
    return current_timestamp

"""
This logger class handles file I/O while documenting actions to ensure the program is running smoothly (will be particularly helpful for user input)
"""
class Logger():
    def __init__(self) -> None:
        self.__full_logs = []
        self.__special_info = []

    '''
    add_log is a function that appends a message and timestamps it
    '''
    def add_log(self, text:str):
        log_text = f"Log Action: {get_current_time} - {text}"
        self.__full_logs.append(log_text)

    '''
        create_open_file is a function that opens, or creates a new .txt file, which it writes all the lines from iterating a list called list.
    '''
    def create_open_file(self, file_name:str, location_dir: str, list: list):
        try:
            with open(f"{location_dir}{file_name}", "x") as file_log:
                for line in list:
                    file_log.write(line)
        except:
            print("The latest log file failed, please try again.")

    '''
        write_log is a function that is designed for timestamp sensitive logs.
    '''
    def write_log(self):
        self.create_open_file(f"{get_current_time}_fandom_log.txt", "/logs/", self.__full_logs)

    '''
        add_info that appends text to a special log, designed to be the desired output of the system.
    '''
    def add_info(self, text:str, subject:str):
        self.__special_info.append(text)
        self.__write_special_log(self.__special_info, subject)

    '''
        __write_special_log writes the desired output of the system to a file.
    '''
    def __write_special_log(self, text_list:list, subject:str):
        self.create_open_file(f"{subject}.txt", "/info_output/", text_list)

Action_Logger = Logger()

current_driver = setup_chrome_drivers()
soup = request_page_html(FULL_STRING, current_driver)
end_chrome_driver_session(current_driver)
valid_links = []
for link in soup.find_all('a'):
    if TYPE == "": 
        valid_links.append(link.get('href'))
    elif TYPE in str(link):
        valid_links.append(link.get('href')) if INCLUDE_GALLERY_PAGES else valid_links.append(link.get('href')) if not INCLUDE_GALLERY_PAGES and GALLERY_TEXT not in str(link) else print("Not a valid link")

# check
print("\n ---------")

current_URL = "https://atos.fandom.com/wiki/Citadel_of_Aesthetical_Ascension"
current_driver = setup_chrome_drivers()
current_driver.get(current_URL)
delay_request(DELAY)
new_soup = BeautifulSoup(current_driver.page_source, 'html.parser')
va = new_soup.find(ELEMENT, class_="wikitable mw-collapsible mw-made-collapsible")
if va != None:
    for th in va.find_all("th"):
        print(th.text)
        Action_Logger.add_info(th.text, current_URL)

current_driver.quit()