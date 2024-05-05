from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import unicodedata

from bs4 import BeautifulSoup


def get_posts(output_path="posts.json"):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    # Open a webpage

    print("scraping ...")
    driver.get("https://www.threads.net/?hl=en")

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Decline optional cookies')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'mount_0_0_')]"))
        )

        print("waiting for page to load...")
        driver.execute_script("window.scrollBy(0, window.innerHeight);")

        driver.implicitly_wait(2)
        time.sleep(1)

        driver.execute_script("window.scrollBy(0, window.innerHeight);")

        driver.implicitly_wait(2)
        time.sleep(1)
        print("page loaded")

        post_list = driver.find_element(By.XPATH, "//div[starts-with(@id, 'mount_0_0_')]/div/div/div[2]/div/div/div/div/div/div/div")
        posts = post_list.find_elements(By.XPATH, "./div")

        p = ""

        for c, post in enumerate(posts): 
            html = ""
            try:
                # try to get someting
                html = post.get_attribute("innerHTML")
            except:
                post_list = driver.find_element(By.XPATH, "//div[starts-with(@id, 'mount_0_0_')]/div/div/div[2]/div/div/div/div/div/div/div")
                posts = post_list.find_elements(By.XPATH, "./div")

            html = post.get_attribute("innerHTML")
            p += html

        # close the driver
        driver.quit()
        print("done scraping")
        print("finding posts ....")

        k = ""
        soup = BeautifulSoup(p, "html.parser")
        classname = " ".join(soup.find("div")['class'])
        post_list = soup.find_all("div", class_=classname)

        output = []

        for c, post in enumerate(post_list):
            try:
                k = post.find_all("div", recursive=False)[0]\
                    .find_all("div", recursive=False)[0]\
                    .find_all("div", recursive=False)[1]\
                    .find_all("div", recursive=False)[3]\
                    .find_all("div", recursive=False)[0]\
                    .find_all("div", recursive=False)[0]\
                    .find_all("span", recursive=False)[0]\
                    .text

                k = unicodedata.normalize('NFKD', k).encode('ascii', 'ignore').decode('ascii')
                k = k.replace("\n", "").replace("\t", "")
                k = k.strip()
                
                if len(k) > 15:
                    output.append({"text": k, "sentiment": ""})

            except Exception as e:
                print(e)

        with open(output_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            data["posts"] += output

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("posts found and exported")

    except Exception as e:
        print("error", str(e))