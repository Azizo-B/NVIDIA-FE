import random
import threading
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# variables
path = r"C:\Program Files (x86)\geckodriver.exe"
uas = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (X11; U; Linux x86_64; ru-RU) AppleWebKit/533.3 (KHTML, like Gecko) Leechcraft/0.4.55-13-g2230d9f Safari/533.3",
    "Mozilla/5.0 (X11; U; Linux x86_64; ru-RU) AppleWebKit/533.3 (KHTML, like Gecko) Leechcraft/0.3.95-1-g84cc6b7 Safari/533.3",
    "Mozilla/5.0 (X11; U; Linux x86_64; ru-ru) AppleWebKit/525.1+ (KHTML, like Gecko, Safari/525.1+) midori",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.13) Gecko/20060413 Red Hat/1.0.8-1.4.1 Firefox/1.0.8",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.6 Safari/525.13",
]
nvidia_api = (
    "https://api.store.nvidia.com/partner/v1/feinventory?skus=FR~NVGFT070~NVGFT080~NVGFT090~NVLKR30S~NSHRMT01~NVGFT060T~187&locale=FR"
)

bot = {"authorization": "<BOT_AUTH_TOKEN>"}


def discord(message):
    requests.post("https://discord.com/api/v9/channels/<CHANNEL_ID>/messages", data=message, headers=bot)


bought_3090, bought_3080, bought_3070 = 0, 0, 0
given_link_3090 = 0
given_link_3080Ti = 0
given_link_3080 = 0
given_link_3070Ti = 0
given_link_3070 = 0
given_link_3060Ti = 0


discord({"content": "Starting up ..."})

# open api (firefox)
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", uas[random.randint(0, len(uas) - 1)])
ff = webdriver.Firefox(firefox_profile=profile, executable_path=path)
ff.get(nvidia_api)
ff.implicitly_wait(3)


# LDLC checkout bot
def checkout(naam, url):
    global bought_3090, bought_3080, bought_3070

    done = 0
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", uas[random.randint(0, 151)])
    ldlc = webdriver.Firefox(firefox_profile=profile, executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    ldlc.get(url)
    ldlc.implicitly_wait(7)
    while done < 1:
        try:
            ldlc.find_element_by_id("cookieConsentAcceptButton").click()
            print("cookies")
            ldlc.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/div[3]/aside/div[2]/div[2]/button[2]").click()
            print("acheter")
            email_field = ldlc.find_element_by_xpath('//*[@id="Email"]')
            email_field.clear()
            email = "<EMAIL>"
            for x in email:
                email_field.send_keys(x)
            print("email")

            ww = ldlc.find_element_by_xpath('//*[@id="Password"]')
            ww.clear()
            wachtwoord = "<PASSWORD>"
            for x in wachtwoord:
                ww.send_keys(x)
            print("pass")

            # connexion
            ldlc.find_element_by_xpath("/html/body/div[3]/div/form/button").click()
            ldlc.implicitly_wait(1)
            print("con")

            # go to BE
            ldlc.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div[1]/div[2]/a").click()
            ldlc.implicitly_wait(1)
            print("BE")

            # payM select
            ldlc.find_element_by_xpath("/html/body/div[3]/div/div[4]/div[2]/div[1]/form/div/div/label").click()
            ldlc.implicitly_wait(1)
            print("payment method")

            cn = ldlc.find_element_by_xpath('//*[@id="CardNumber"]')
            cn.clear()
            cn.send_keys("<CARD_NUMBER>")
            print("cn")
            date = ldlc.find_element_by_xpath('//*[@id="ExpirationDate"]')
            date.clear()
            date.send_keys(0)
            print("0")
            date.send_keys(524)
            print("date - 0")
            name = ldlc.find_element_by_xpath('//*[@id="OwnerName"]')
            name.clear()
            name.send_keys("<CARD_HOLDER>")
            print("name")
            cvv = ldlc.find_element_by_xpath('//*[@id="Cryptogram"]')
            cvv.clear()
            cvv.send_keys("<CVV>")
            print("cvv")

            # buy btn
            ldlc.find_element_by_xpath("/html/body/div[3]/div/div[4]/div[2]/div[1]/div/div/form/div[8]/div/button").click()
            print("buy")

            buy_message = {"content": naam + " bought"}
            discord(buy_message)

            if naam == "3090FE":
                bought_3090 += 1
            elif naam == "3080FE":
                bought_3080 += 1
            else:
                bought_3070 += 1
            done += 1

        except:
            ldlc.refresh()
            time.sleep(2)


# loop and check for changes while changing user agent
while bought_3090 < 1 and bought_3080 < 1 and bought_3070 < 1:

    start = time.time()
    timer = random.randint(1200, 1740)

    def nvidia3090():
        global bought_3090, bought_3080, bought_3070, given_link_3090
        i = 1
        while i > 0:
            try:
                if (
                    '"https://www.ldlc.com/fiche/PB56901355.html"'
                    == ff.find_element_by_id("/listMap/2/product_url").text.replace("product_url", "").strip()
                    and '"false"' == ff.find_element_by_id("/listMap/2/is_active").text.replace("is_active", "").strip()
                ):
                    time.sleep(random.randint(3, 7))
                else:
                    message_3090 = {
                        "content": "3090 FE in stock: "
                        + ff.find_element_by_id("/listMap/2/product_url").text.replace("product_url", "").strip()
                    }
                    discord(message_3090)
                    if bought_3090 < 1 and bought_3080 < 1 and bought_3070 < 1:
                        checkout(
                            "3090FE",
                            ff.find_element_by_id("/listMap/2/product_url").text.replace("product_url", "").strip().replace('"', ""),
                        )
                    i -= 1
                    given_link_3090 += 1
            except:
                i -= 1

    def nvidia3080Ti():
        global given_link_3080Ti
        i = 1
        while i > 0:
            try:
                if (
                    '"https://www.ldlc.com/fiche/PB60235897.html"'
                    == ff.find_element_by_id("/listMap/5/product_url").text.replace("product_url", "").strip()
                ):
                    time.sleep(random.randint(3, 7))
                else:
                    message_3080Ti = {
                        "content": "3080Ti FE in stock: "
                        + ff.find_element_by_id("/listMap/5/product_url").text.replace("product_url", "").strip()
                    }
                    discord(message_3080Ti)
                    i -= 1
                    given_link_3080Ti += 1
            except:
                i -= 1

    def nvidia3080():
        global bought_3090, bought_3080, bought_3070, given_link_3080
        i = 1
        while i > 0:
            try:
                if (
                    '"https://www.ldlc.com/fiche/PB50154869.html"'
                    == ff.find_element_by_id("/listMap/3/product_url").text.replace("product_url", "").strip()
                    and '"false"' == ff.find_element_by_id("/listMap/3/is_active").text.replace("is_active", "").strip()
                ):
                    time.sleep(random.randint(3, 7))
                else:
                    message_3080 = {
                        "content": "3080 FE in stock: "
                        + ff.find_element_by_id("/listMap/3/product_url").text.replace("product_url", "").strip()
                    }
                    discord(message_3080)
                    if bought_3090 < 1 and bought_3080 < 1 and bought_3070 < 1:
                        checkout(
                            "3080FE",
                            ff.find_element_by_id("/listMap/3/product_url").text.replace("product_url", "").strip().replace('"', ""),
                        )
                    i -= 1
                    given_link_3080 += 1
            except:
                i -= 1

    def nvidia3070Ti():
        global given_link_3070Ti
        i = 1
        while i > 0:
            try:
                if (
                    '"https://www.ldlc.com/fiche/PB59740155.html"'
                    == ff.find_element_by_id("/listMap/6/product_url").text.replace("product_url", "").strip()
                ):
                    time.sleep(random.randint(3, 7))
                else:
                    message_3070Ti = {
                        "content": "3070Ti FE in stock: "
                        + ff.find_element_by_id("/listMap/6/product_url").text.replace("product_url", "").strip()
                    }
                    discord(message_3070Ti)
                    i -= 1
                    given_link_3070Ti += 1
            except:
                i -= 1

    def nvidia3060Ti():
        global given_link_3060Ti
        i = 1
        while i > 0:
            try:
                if (
                    '"https://www.ldlc.com/fiche/PB78876460.html"'
                    == ff.find_element_by_id("/listMap/4/product_url").text.replace("product_url", "").strip()
                ):
                    time.sleep(random.randint(3, 7))
                else:
                    message_3060Ti = {
                        "content": "3060Ti FE in stock: "
                        + ff.find_element_by_id("/listMap/4/product_url").text.replace("product_url", "").strip()
                    }
                    discord(message_3060Ti)
                    i -= 1
                    given_link_3060Ti += 1
            except:
                i -= 1

    def newthread(target):
        bot = threading.Thread(target=target)
        bot.start()

    if given_link_3090 < 2:
        newthread(nvidia3090)
    if given_link_3080 < 2:
        newthread(nvidia3080)
    if given_link_3070Ti < 2:
        newthread(nvidia3070Ti)
    if given_link_3060Ti < 2:
        newthread(nvidia3060Ti)

    i = 1
    while i > 0:
        current = time.time()
        passed = current - start
        if passed < timer:
            try:
                if (
                    '"https://www.ldlc.com/fiche/PB68945690.html"'
                    == ff.find_element_by_id("/listMap/7/product_url").text.replace("product_url", "").strip()
                    and '"false"' == ff.find_element_by_id("/listMap/7/is_active").text.replace("is_active", "").strip()
                ):
                    ff.refresh()
                    time.sleep(random.randint(3, 7))
                else:
                    message_3070 = {
                        "content": "3070 FE in stock: "
                        + ff.find_element_by_id("/listMap/7/product_url").text.replace("product_url", "").strip()
                    }
                    discord(message_3070)
                    if bought_3090 < 1 and bought_3080 < 1 and bought_3070 < 1:
                        checkout(
                            "3070FE",
                            ff.find_element_by_id("/listMap/7/product_url").text.replace("product_url", "").strip().replace('"', ""),
                        )
                    ff.refresh()
                    time.sleep(5)
                    ff.refresh()
                    i -= 1

            except:
                i -= 1
        else:
            i -= 1

    ff.quit()

    time.sleep(2)

    pf = webdriver.FirefoxProfile()
    pf.set_preference("general.useragent.override", uas[random.randint(0, 151)])
    ff = webdriver.Firefox(firefox_profile=pf, executable_path=path)
    ff.get(nvidia_api)
    ff.implicitly_wait(3)

ff.quit()
message_finished = {"content": "FE_bot terminating...."}
discord(message_finished)
