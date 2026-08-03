''' 
FandomReader will access as file that has a link (for a valid fandom page) 
Currently this program is designed for a specific task of mine, however I hope to give the user more freedom with user input for elements and classes

This will send a request to fandom to grab the html on the page, using selenium, therefore an up-to-date chromium is required on the computer running the program

With this, we just need all the table and data nested within it, the rest can be deleted

Packages:
selenium: https://pypi.org/project/selenium/ - used to automate the process connecting to the web
beautifulsoup: http://pypi.org/project/beautifulsoup4/
'''

from selenium import webdriver

from bs4 import BeautifulSoup

import time
import datetime
import re # keeping this here in case a new need to find partial expressions

DELAY = 2 # 2 seconds
CLOUDFLARE_DELAY = 35

END = "/wiki/Special:AllPages"

INCLUDE_GALLERY_PAGES = False
GALLERY_TEXT = "/Gallery"

TYPE = "Citadel_of_" # the substring of the type of page you want | use "" to keep all pages

ELEMENT = "table"

FANDOM_NOT_FOUND = "This wiki does not exist | | Fandom"
CAP = 3
TARGET_OUTPUT_FILE = "output.txt"

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
    return str(current_timestamp)

'''
    The file manager class manages all related input and output
'''
class FileManager():
        def __init__(self) -> None:
            self.__full_output_list = []
        '''
            add_info that appends text to a special log, designed to be the desired output of the system.
        '''
        def add_all_info(self, info_list:list):
            self.__full_output_list = info_list
            self.__write_output(self.__full_output_list)
    
        '''
            __write_special_log writes the desired output of the system to a file.
        '''
        def __write_output(self, text_list:list):
            self.create_open_file(TARGET_OUTPUT_FILE, text_list)
    
        def clear_text_file(self, target_name: str):
            with open(target_name, "w") as file_log:
                file_log.write(f"{get_current_time()}\n")
        '''
            create_open_file is a function that opens, or creates a new .txt file, which it writes all the lines from iterating a list called list.
        '''
        def create_open_file(self, file_name:str, content_list: list):
            try:
                with open(file_name, "a") as file_log:
                    for content in content_list:
                        file_log.write(content)
            except:
                print("The latest log file failed, please try again.")
        


"""
This logger class handles documenting actions to ensure the program is running smoothly (will be particularly helpful for user input)
"""
class Logger():
    def __init__(self, file_manager: FileManager) -> None:
        self.__full_logs = []
        self.__file_manager = file_manager

    '''
    add_log is a function that appends a message and timestamps it
    '''
    def add_log(self, text:str):
        log_text = f"Log Action: {get_current_time} - {text}"
        self.__full_logs.append(log_text)


    '''
        write_log is a function that is designed for timestamp sensitive logs.
    '''
    def write_log(self):
        self.__file_manager.create_open_file(f"/logs/{get_current_time}_fandom_log.txt", self.__full_logs)



'''
    This class handles all user input within the program
'''
class InputHandler():
    '''
        As the program handles one option per request, it is assumed the user output is one output.
        input_hint should be lowercase to standardise the process
    '''
    def __init__(self) -> None:
        self.__current_wiki = ""
    def get_current_wiki(self) -> str:
        return self.__current_wiki
    def set_current_wiki(self, current_wiki:str) -> None:
        self.__current_wiki = current_wiki 

    def handle_input(self, input_hint: str, desired_output: list) -> str:
        user_output = ""
        if desired_output != []:
            while user_output not in desired_output:
                user_output = input(input_hint).lower()
            return user_output
        else:
            while user_output == "":
                user_output = input(input_hint)
            return user_output

    '''
        This will handle user request to ensure that they are targeting a valid fandom page.
    '''
    def handle_user_request(self, hint:str):
        user_output = ""
        title_check = "" # this is currently volatile because if fandom changes the title structure this does not work
        soup = ""
        while title_check == "" or title_check == FANDOM_NOT_FOUND:
            user_output = self.handle_input(hint, [])
            user_fandom = self.build_url(END, fandom=user_output)

            self.set_current_wiki(user_fandom)

            current_driver = setup_chrome_drivers()
            soup = request_page_html(f"{user_fandom}{END}", current_driver)
            title_check = current_driver.title
            end_chrome_driver_session(current_driver)
        return soup

    def display_disclaimer(self, disclaimer_text:str):
            print(f"\n!INFO!\n------- \n{disclaimer_text}\n------\n")
    '''
    Dynamic build a string if required
    '''
    def build_string(self, pre: str, content:list, end: str) -> str:
        feh = pre 
        for string in content:
            feh = f"{feh} {string},"
        return f"{feh} {end}"

    def build_url(self, end_tag:str, fandom="") -> str:
        if(self.get_current_wiki() != ""):
            return f"{self.get_current_wiki()}{end_tag}"
        else:
            return f"https://{fandom}.fandom.com"


File_Handler = FileManager()
Action_Logger = Logger(file_manager=File_Handler)
File_Handler.clear_text_file(TARGET_OUTPUT_FILE)
Input_Handler = InputHandler()

FANDOM_HINT = "Please type the Fandom (the part before .fandom) that you want to read: "
ALLPAGES_HINT = "Please enter a substring, if you wish to search all pages, then enter N/A: "

ELEMENT_HINT = "Select your desired target element ( "
ACCEPTED_HTML_ELEMENTS = ["table", "body", "div", "a", "ol", "li"]
NESTED_ELEMENTS = ["table"]
NESTED_TABLE_ELEMENTS = ["th", "tr"]
NESTED_HINT = "Your chosen element is nested, would you like to go deeper (Y/N): "
END_HINT = "html ): "

ASK_FOR_CLASS = "Is there a class that you would want to be selected (Y/N): "
ASK_WHAT_CLASS = "What class would you like to select: "
YES_NO = ["y", "n"]

DEBUG_HINT = "No info to print, perhaps you mistyped the class?"
DOWNLOAD_HINT = f"Remember to save your {TARGET_OUTPUT_FILE} elsewhere if you plan on re-running this program"

soup = Input_Handler.handle_user_request(FANDOM_HINT)
Input_Handler.display_disclaimer(f"The selected wiki [{Input_Handler.get_current_wiki()}] found a {END} page, \nto decrease the time it takes to read all pages, \nthe following prompt will ask for a substring of desired pages, \nplease enter one if applicable")
all_pages = Input_Handler.handle_input(ALLPAGES_HINT, [])


full_element_hint = Input_Handler.build_string(ELEMENT_HINT, ACCEPTED_HTML_ELEMENTS, END_HINT)
element = Input_Handler.handle_input(full_element_hint, ACCEPTED_HTML_ELEMENTS)
nested_element = "" 
if element in NESTED_ELEMENTS:
    deep_search = True if Input_Handler.handle_input(NESTED_HINT, YES_NO) == "y" else False if Input_Handler.handle_input(ASK_FOR_CLASS, YES_NO) == "n" else False
    if deep_search:
        full_nested_element_hint = Input_Handler.build_string(ELEMENT_HINT, NESTED_TABLE_ELEMENTS, END_HINT)
        nested_element = Input_Handler.handle_input(full_nested_element_hint, NESTED_TABLE_ELEMENTS)

is_class = True if Input_Handler.handle_input(ASK_FOR_CLASS, YES_NO) == "y" else False if Input_Handler.handle_input(ASK_FOR_CLASS, YES_NO) == "n" else False 
user_class = ""
if is_class:
    user_class = Input_Handler.handle_input(ASK_WHAT_CLASS, [])

valid_links = []
for link in soup.find_all('a'):
    if all_pages == "" or all_pages == "n/a": 
        valid_links.append(link.get('href'))
    elif all_pages in str(link):
        valid_links.append(link.get('href')) if INCLUDE_GALLERY_PAGES else valid_links.append(link.get('href')) if not INCLUDE_GALLERY_PAGES and GALLERY_TEXT not in str(link) else print("")

# check
print("\n ---------")
url_cap = 0
full_output = []
for href in valid_links:
    if url_cap < CAP:
        current_URL = Input_Handler.build_url(href)
        current_driver = setup_chrome_drivers()
        delay_request(DELAY)
        current_driver.get(current_URL)
        new_soup = BeautifulSoup(current_driver.page_source, 'html.parser')
        target_element = new_soup.find(element, class_=user_class)
        if target_element != None and nested_element != "":
            for th in target_element.find_all(nested_element):
                full_output.append(th.text)
        else:
            print(DEBUG_HINT)
        current_driver.quit()
        url_cap += 1
File_Handler.add_all_info(full_output)
Input_Handler.display_disclaimer(DOWNLOAD_HINT)

    