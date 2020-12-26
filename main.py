import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as pt


class Program:
    def __init__(self, username):
        if not os.path.isfile(os.path.join(os.getcwd(), "chromedriver.exe")):
            print("chromedriver.exe is not in your current working directory (details in README)")
            exit(-1)
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.username = username

    def goes_to_profile(self, password_given):
        self.driver.get("http://www.instagram.com")

        # 10 is the max time to wait
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        password.clear()

        # Write your username and password
        username.send_keys(self.username)
        password.send_keys(password_given)

        # Accept Cookies  (pt) comes from accept 
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'pt')]"))).click()

        # Log in
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "button[type='submit']"))).click()
        time.sleep(4)

        try:  # answer to "Save login password" questions with a Not now
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "sqdOP.yWX7d.y3zKF"))).click()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "aOOlW.HoLwm "))).click()
        except OSError:
            pass

        # it goes to your profile
        self.driver.get("http://www.instagram.com/" + self.username)

    # parameters can be only followers or following
    def get_f(self, f):
        # maximize the window
        pt.keyDown('winleft')
        pt.press('up')
        pt.keyUp('winleft')
        max_x, max_y = pt.size()
        pt.moveTo(max_x / 2, max_y / 2, duration=0.5)  # hover on it so it can scroll down

        href_f = "/" + self.username + "/" + f + "/"
        f_button = self.driver.find_element_by_xpath('//a[@href="' + href_f + '"]')
        f_amount = int(f_button.text.split()[0])  # num of followers or of following (parameter given)
        f_button.click()
        while True:
            # isgrP is the div where the ul with all the li (followers all followings are)
            html_list = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "isgrP")))
            if len(html_list.find_elements_by_tag_name("li")) == f_amount:
                break
            pt.scroll(-800)
        pt.leftClick(max_x / 4, max_y / 2)
        f_list = self.driver.find_elements_by_tag_name("a")
        f_list_text = [f.text for f in f_list]
        return list(filter(self.check_if_exist, f_list_text))

    # returns the people that you follow but they dont follow you back
    @staticmethod
    def compare_followers_following(followers_list, following_list):
        matches = set(followers_list) & set(following_list)
        not_followers = [f for f in following_list if f not in matches]
        return "".join(x + "\n" for x in not_followers)

    # check if the a tag in html is a person or not
    @staticmethod
    def check_if_exist(elem):
        return True if elem and not elem.isupper() and ' ' not in elem and not elem.isnumeric() else False


program = Program("your_username")
program.goes_to_profile("your_password")
followers = program.get_f("followers")
following = program.get_f("following")
print("The people that dont follow you but you follow:\n" + program.compare_followers_following(followers, following))
