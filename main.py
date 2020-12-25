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
            raise Exception("chromedriver.exe is not in your current working directory")
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
        username.send_keys(self.username)
        password.send_keys(password_given)

        # Cookies  (pt) comes from accept in every language
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'pt')]"))).click()

        # Log in
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "button[type='submit']"))).click()
        time.sleep(4)

        # Not now
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sqdOP.yWX7d.y3zKF"))).click()

        # Not now 2
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "aOOlW.HoLwm "))).click()

        # go to your profile
        time.sleep(2)
        self.driver.get("http://www.instagram.com/" + self.username)

    # parameters can be only followers or following
    def get_f(self, f):
        time.sleep(4)

        # maximize the window
        pt.keyDown('winleft')
        pt.press('up')
        pt.keyUp('winleft')

        href_f = "/" + self.username + "/" + f + "/"
        f_button = self.driver.find_element_by_xpath('//a[@href="' + href_f + '"]')
        f_amount = int(f_button.text.split()[0])  # num of followers of following
        f_button.click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "isgrP"))).click()
        max_x, max_y = pt.size()
        pt.moveTo(max_x / 2, max_y / 2, duration=0.5)
        time.sleep(1)
        while True:
            html_list = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "PZuss")))
            if len(html_list.find_elements_by_tag_name("li")) == f_amount:
                break
            pt.scroll(-800)
            time.sleep(.6)
        f_list = self.driver.find_elements_by_tag_name("a")
        f_list_text = [f.text for f in f_list]
        f_names = list(filter(self.check_if_exist, f_list_text))
        pt.leftClick(max_x / 4, max_y / 2)
        return f_names

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
program.goes_to_profile("put_your_password")

# uncomment this line if you dont want the program to goes to your profile automatically and comment row 91
# input()  # Run the program, go yourself to your instagram_profile, comeback press a key, go back to the chrome_window

followers = program.get_f("followers")
following = program.get_f("following")
print("The people that dont follow you but you follow:\n" + program.compare_followers_following(followers, following))
