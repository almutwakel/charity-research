import pandas
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By

filepath = "DATA/links.csv"
saved_links = ["https://www.gofundme.com/f/bharti-shahanis-astroworld-recovery-fund?qid=275c23b45a3fd34d5a4b57ddf9952735", "https://www.gofundme.com/f/help-henry-with-medical-expenses?qid=2daca84e727f6a2ae6e8c35baf33da8a",
"https://www.gofundme.com/f/prayers-and-support-for-balloutine-family?qid=2daca84e727f6a2ae6e8c35baf33da8a"]


def collect_links(existing=None):

    if existing is None:
        links = []
    else:
        links = existing

    url = "https://www.gofundme.com/discover/medical-fundraiser"

    driver = webdriver.ChromiumEdge()
    driver.get(url)
    show_more = driver.find_element(By.LINK_TEXT, "Show More")

    for x in range(100):
        print(x)
        try:
            show_more.click()
            print("successfully pressed")
            sleep(1)
        except NoSuchElementException:
            print("broke loop")
            break
        except ElementNotInteractableException:
            print("broke loop")
            break
        except ElementClickInterceptedException:
            print("cooldown")
            sleep(2)

    link_elements = driver.find_elements(By.CLASS_NAME, "fund_tile_card_link")
    for link_element in link_elements:
        links.append(link_element.get_attribute('href'))

    # page = urlopen(url)
    # soup = BeautifulSoup(page, "html.parser")
    #
    # containers = soup.find_all('a', attrs={"class": "fund_tile_card_link"})
    # print(containers)
    # for container in containers:
    #    link = str(re.findall('class="fund_tile_card_link" href="(.*)" id=', str(container))[0])
    #    if link not in links:
    #        links.append(link)

    return links


def save(links, overwrite=False):
    with open(filepath, 'a+') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])


def load(filepath):
    links = []
    with open(filepath, 'r') as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            links.append(line[0])

    return links[1:]


def scrape_links(links):
    data_collection = []
    fields = ["Url", "Title", "Text", "Donation", "Goal", "Time"]

    # Take csv file and convert to readable format

    for link in links:
        try:
            # Goes to Url
            url = link
            page = urlopen(url)
            # driver = webdriver.ChromiumEdge()
            # driver.get(url)
            # page = driver.page_source

            # Scrapes
            soup = BeautifulSoup(page, "html.parser")

            container = soup.find_all("div", {"class": "p-campaign"})
            social_container = soup.find_all("span", {"class": "text-stat-value text-underline"})
            info_string = container[0].text
            info_string = info_string.splitlines()
            info_string = list(filter(None, info_string))

            # print(info_string[0])
            # print(soup)

            title = str(re.findall('^(.*)\$.*? raised', info_string[0])[0])

            donation = int(re.findall('\$(.*)  raised', info_string[0])[0].replace(',', ''))

            goal = int(re.findall('of \$(.*?) goal', info_string[0])[0].replace(',', ''))
            # donor_string = re.findall('donors(.*?) donations', info_string[0])[0].replace('K', '000')
            # donors = int(donor_string)
            # print(donors)

            try:
                time = re.findall("Created (.*) ago", info_string[0])[0]
            except:
                try:
                    time = re.findall('<span class="m-campaign-byline-created a-created-date">Created (.*?)</span>', str(container))[0]

                except:
                    time = None

            text = ""

            for paragraph in info_string:
                if paragraph != "\xa0":
                    text += paragraph + " "

            try:
                text = re.findall("Medical, Illness & Healing(.*)Read more", text)[0].replace(" ", " ")
            except:
                text = re.findall("See top donationsSee top(.*)Read moreDonateShareDonations", text)[0].replace(" ", " ")
        except:
            continue

        row = [url, title, text, donation, goal, time]
        data_collection.append(row)
    # Opens csv into 'Write' mode
    with open("DATA/scraped_links.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data_collection)


def enumerate(string):
    if 'K' in string:
        string = string.replace('K', '')
        if '.' in string:
            query = re.findall('\.(.*)', string)[0]
        else:
            query = ""
        string = string.replace('.', '')
        string += "0" * (3 - len(query))

    return int(string)


def scrape_donors(urls):

    driver = webdriver.ChromiumEdge()
    donorslist = []
    for url in urls:
        try:
            # Goes to Url
            # page = urlopen(url)
            driver.get(url)
            page = driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            container = soup.find_all("div", {"class": "p-campaign"})
            info_string = container[0].text
            info_string = info_string.splitlines()
            info_string = list(filter(None, info_string))
            print(info_string[0])
            try:
                donor_string = re.findall('goal(.*?) donors', info_string[0])[0]
                donors = enumerate(donor_string)
            except:
                try:
                    donor_string = re.findall('donors(.*?) donations', info_string[0])[0]
                    donors = enumerate(donor_string)
                except:
                    try:
                        donor_string = re.findall('Donations \((.*?)\)', info_string[0])[0]
                        donors = enumerate(donor_string)
                    except:
                        donor_string = re.findall('raised(.*?) donations', info_string[0])[0]
                        donors = enumerate(donor_string)
        except:
            donors = 0
        print(donors)
        donorslist.append([donors])
        with open("DATA/donor_counts.csv", "w+") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Donors"])
            csvwriter.writerows(donorslist)


def conditionalAppendToCSV(file, links, data):

    validlinks = []
    with open(file, "r") as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            validlinks.append(row[0])

    dataToAppend = []

    for i in range(len(links)):
        if links[i] in validlinks:
            dataToAppend.append(data[i])

    return dataToAppend


if __name__ == "__main__":
    # links = collect_links()
    # save(links)
    links = load("DATA/links.csv")
    # print(len(loaded))
    # scrape_links(saved_links)
    # scrape_donors(loaded)
    # donordata = load("DATA/donor_counts.csv")
    # dataToAppend = conditionalAppendToCSV("DATA/scraped_links.csv", links, donordata)
    # df = pandas.read_excel("DATA/LIWC2015 Results (scraped_links_titles).xlsx")
    # df["Donors"] = dataToAppend
    # df.to_excel("DATA/LIWC_scraped_links_titles_donors.xlsx")

