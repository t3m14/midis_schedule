from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
from PIL import Image
from io import BytesIO


class MidisSchedule:
    def __init__(self, login="", password="") -> None:
        assert login
        assert password
        self.login = login
        self.password = password
        self.cookie_path = f"./cookies/{login}.pkl"
        self.today_table_path = "./images/today.png"
        self.tomorrow_table_path = "./images/tomorrow.png"
        self.__driver = None
        self.__url = "http://portal.midis.info"

    def __load_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)

    def __login_and_get_cookie(self):
        login = self.__driver.find_element(By.NAME, "USER_LOGIN")
        password = self.__driver.find_element(By.NAME, "USER_PASSWORD")
        login.send_keys(self.login)
        password.send_keys(self.password)
        btn = self.__driver.find_element(By.CLASS_NAME, "btn")
        btn.click()
        pickle.dump(self.__driver.get_cookies(), open(self.cookie_path, "wb"))

    def __login_with_cookie(self):
        self.__driver.get(self.__url)
        self.__driver.delete_all_cookies()
        cookies = pickle.load(open(self.cookie_path, "rb"))
        for cookie in cookies:
            self.__driver.add_cookie(cookie)
        self.__driver.get(self.__url)

    def get_today_table(self) -> "PendingDeprecationWarning":
        self.__run()
        self.__driver.get(self.__url+"/schedule/")
        all_titles = self.__driver.find_elements(By.CLASS_NAME, "card-title")
        for title in all_titles:
            if "(Сегодня)" in title.text:
                screenshot = title.find_element(By.XPATH, "./..").screenshot_as_png
                image = Image.open(BytesIO(screenshot))
                image.save(self.today_table_path)
                print(title.text)
            
    def get_tommorow_table(self):
        self.__run()
        self.__driver.get(self.__url+"/schedule/")
        all_titles = self.__driver.find_elements(By.CLASS_NAME, "card-title")
        all_titles = iter(all_titles)
        for title in all_titles:
            if "(Завтра)" in title.text:
                screenshot = title.find_element(By.XPATH, "./..").screenshot_as_png
                image = Image.open(BytesIO(screenshot))
                image.save(self.tomorrow_table_path)
            elif "Суббота (Сегодня)" in title.text:
                title = next(all_titles)   
                screenshot = title.find_element(By.XPATH, "./..").screenshot_as_png
                image = Image.open(BytesIO(screenshot))
                image.save(self.tomorrow_table_path)

    def __run(self):
        self.__load_driver()
        try:
            self.__login_with_cookie()
        except:
            self.__login_and_get_cookie()
        