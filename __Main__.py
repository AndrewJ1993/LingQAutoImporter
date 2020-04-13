from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import requests


# Retrieves links from archive website.
def get_links():
    page_file = urllib.request.urlopen("https://www.dw.com/de/top-thema-mit-vokabeln-archiv-2018/a-42001639")
    page_html = page_file.read()
    page_file.close()
    soup = BeautifulSoup(page_html, "html.parser")
    soup_all = soup.findAll("a")

    links_list = []
    for href in soup_all:
        links_list.append("https://www.dw.com" + quote(href.get("href")))

    i = 0
    for link in links_list:
        print(str(i) + " " + link)
        i += 1

    return links_list[219:322]


# Tests that links are correctly sliced.
def test_slices(links_list):
    print(links_list)
    question = input("Is the URL correctly set? Are slices correctly set? Is the collection correctly set? Y or N: ")
    if question == "N" or question == "n":
        quit()
    elif question == "Y" or question == "y":
        return

# Scrape information from desired links.
def get_information(in_link):
    page_file = urllib.request.urlopen(in_link)
    page_html = page_file.read()
    page_file.close()
    soup = BeautifulSoup(page_html, "html.parser")
    title = soup.h1.string
    original_url = in_link

    # Retrieves text.
    contents = soup.find_all("div", 'dkTaskWrapper tab3')
    full_content = ""
    new_content = []
    for content in contents:
        [x.extract() for x in content.find_all("span")]
        full_content = list(content.strings)
    text = ''.join( new_content) + "\n\n\n" + "(Wenn Sie einen Problem mit dieser Lektion haben, schicken Sie mir bitte eine Nachricht.)"

    # Retrieves download link to collect audio link and duration
    contents = soup.find_all("div", "linkList overlayIcon")
    download_link = ""
    for content in contents:
        link = content.find_all("a")
        download_link_variable = [x.get("href") for x in link]
        download_link += "https://www.dw.com" + quote(download_link_variable[0])

    # Retrieve audio links.
    page_file = urllib.request.urlopen(download_link)
    page_html = page_file.read()
    page_file.close()
    soup = BeautifulSoup(page_html, "html.parser")

    audio_links = []
    for current_link in soup.find_all('a'):
        audio_links.append(current_link.get("href"))
        for this_link in audio_links:
            if "radiodownload" in this_link:
                final_audio = this_link
    external_audio = final_audio

    # Retrieve audio duration
    duration_minutes = soup.find_all("span", "basicteaser__mediaduration")
    for duration in duration_minutes:
        duration_total_minutes = duration.string
    minutes = int(duration_total_minutes[:2])
    seconds = int(duration_total_minutes[3:5])
    total_seconds = str(minutes * 60 + seconds)

    collection = "424850"

    return title, text, collection, original_url, external_audio, total_seconds


# Posts information to LingQ course. Change this information to scraped information when retreived.
def post_information(in_information):
    print(in_information)
    api_key = "put_api_key_here"
    data = {"title": in_information[0],
            "text": in_information[1],
            "collection": in_information[2],
            "original_url": in_information[3],
            "external_audio": in_information[4],
            "duration": in_information[5]
            }
    requests.post('https://www.lingq.com/api/v2/de/lessons/', data=data, headers={'Authorization': 'Token ' + api_key})


links = get_links()
test_slices(links)
i = 0
for link in links:
    information = get_information(link)
    print(i)
    print(information)
    #post_information(information)
    i += 1
