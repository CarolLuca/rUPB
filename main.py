import requests
from bs4 import BeautifulSoup

def getgood(s):
    output = ""
    for line in s.splitlines():
        if line.startswith("Pentru cele mai importante ştiri ale zilei") == True:
            return output
        output += line
    return output

def process_tags(list_tags):
    list_tags = list_tags.strip("Taguri:")
    tags = ""
    for tag in list_tags.split(","):
        new_tag = ""
        for character in tag:
            if character.lower() in "qwertyuiopasdfghjklzxcvbnm -":
                new_tag += character
        tags += new_tag.strip(" ")
        tags += ","
    tags = tags.strip(",")
    return tags


def analyse(category, title, link):
    if len(link) < 5:
        return

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    safesummary = soup.find('p', class_='chapeau')
    if not safesummary:
        return

    summary = soup.find('p', class_='chapeau').text.strip()
    taggs = soup.find('dl', class_='a-tags').text.strip()
    text = ''
    for paragraph in soup.find_all('p', class_=None):
        text += paragraph.text.strip() + '\n'

    summary = getgood(summary)
    text = getgood(text)

    out = open("dataset.csv", "a", encoding="utf-8")
    # print("Titlu: \n" + title + '\n')
    title = title.replace("\"", "\'")
    out.write(title + "|")
    # print("Link: \n" + link + '\n')
    out.write(link + "|")
    # print("Categorie: \n" + category + '\n')
    out.write(category + "|")
    # print("Rezumat: \n" + summary + '\n')
    summary = summary.replace("\"", "\'")
    out.write(summary + "|")
    # print("Continut: \n" + text + '\n')
    text = text.replace("\"", "\'")
    out.write(text + "|")
    # print("Taguri: \n" + taggs + '\n')
    taggs = process_tags(taggs)
    out.write(taggs + "|\n")

    out.close()


if __name__ == "__main__":
    categories = ["politic", "economic", "social", "externe", "sanatate", "sport",
                  "life-inedit", "meteo", "healthcare-trends", "economia-digitala"]
    nr_page = [24, 14, 38, 53, 4, 13,
               4, 4, 8, 1]

    page_limit = 1

    out = open("dataset.csv", "w", encoding="utf-8")
    out.write("title|link|category|summary|text|taggs\n")
    out.close()

    id = -1
    for category in categories:
        id += 1
        for page_number in range(1, nr_page[id] + 1):
            url = "https://www.mediafax.ro/" + category + "/page/" + str(page_number) + "/"
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")

                news = soup.find_all("a", {"class": "title"})

                for article in news:
                    title = article.text.strip()
                    link = article.get("href")
                    if link.startswith("http") and "LIVE TEXT" not in link and "razboiul-din-ucraina-anul" not in link:
                        analyse(category, title, link)
            except:
                continue
