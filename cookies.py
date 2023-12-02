import os
import pickle


def save_cookies(driver, location):
    with open(location, "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookies(driver, location, url=None):
    with open(location, "rb") as cookiesfile:
        cookies = pickle.load(cookiesfile)
        if url:
            driver.get(url)
        for cookie in cookies:
            driver.add_cookie(cookie)


def check_and_load_cookies(driver, location, url):
    if os.path.exists(location):
        load_cookies(driver, location, url)
    else:
        if url:
            driver.get(url)
