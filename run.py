import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from configparser import ConfigParser

###################################

config_object = ConfigParser()

config_object.read("confg.ini")

# Get the password

userinfo = config_object["USERINFO"]

# Complete these 2 fields ==================
USERNAME = format(userinfo["put your Email or username"])
PASSWORD = format(userinfo["put your Password here"])
# ==========================================

TIMEOUT = 15
print("""________00000000000___________000000000000________
______00000000_____00000___000000_____0000000______
____0000000_____________000______________00000_____
___0000000_______________0_________________0000____
__000000____________________________________0000___
__00000_____________________________________ 0000__
_00000______________________________________00000__
_00000_____________________________________000000__
__000000_________________________________0000000___
___0000000______________________________0000000____
_____000000____________________________000000______
_______000000________________________000000________
__________00000_____________________0000___________
_____________0000_________________0000_____________
_______________0000_____________000________________
_________________000_________000___________________
_________________ __000_____00_____________________
______________________00__00_______________________
""")
config_object = ConfigParser()

config_object.read("confg.ini")

# CREATING DATABASE
def createdb():
    try:
        con = sqlite3.connect("database.db")
        curs = con.cursor()
        curs.execute("""CREATE TABLE accounts(
            id text NOT NULL PRIMARY KEY,
            name text NOT NULL,
            sent integer NOT NULL
        )""")
        con.commit()
        con.close()
        print(f'[INFO] DATABASE CREATED')
    except sqlite3.OperationalError as e:
        print(e)
        print('DATABASE, operational')


def insertdb(id, name, sent):
    try:
        con = sqlite3.connect("database.db")
        curs = con.cursor()
        curs.execute("INSERT INTO accounts VALUES (?,?,?)", (id, name, sent))
        con.commit()
        con.close()
        print(f'[INFO] Row Added To DATABASE, ID : {id}')
    except sqlite3.OperationalError as e:
        print(e)


def scrape():
    createdb()
    usr = format(userinfo["Whose followers do you want to scrape"])
    user_input = int(input('[Required] - How many followers do you want to scrape (60-10K recommended): '))

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(executable_path=CM().install(), options=options)
    bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')

    time.sleep(2)

    print("[Info] - Logging in...")

    user_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))

    user_element.send_keys(USERNAME)

    pass_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))

    pass_element.send_keys(PASSWORD)

    login_button = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]/button')))

    time.sleep(0.4)

    login_button.click()

    time.sleep(5)

    bot.get('https://www.instagram.com/{}/'.format(usr))

    time.sleep(3.5)

    WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[2]/a'))).click()

    time.sleep(2)

    print('[Info] - Scraping...')

    users = set()

    for _ in range(round(user_input // 10)):

        ActionChains(bot).send_keys(Keys.END).perform()

        time.sleep(2)

        followers = bot.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')

        # Getting url from href attribute
        for i in followers:
            if i.get_attribute('href'):
                users.add(i.get_attribute('href').split("/")[3])
            else:
                continue

    for user in users:
        print(user)
        insertdb(f"{user}", f"{user}", 0)

    print('[Info] - Saving...')


if __name__ == '__main__':
    scrape()
