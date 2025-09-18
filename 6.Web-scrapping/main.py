import requests
import bs4
import re
from pprint import pprint
from time import sleep
from fake_headers import Headers

## Определяем список ключевых слов:
KEYWORDS = ["дизайн", "фото", "web", "python", "додд", "организма"]
# число попыток згрузить список статей
NUMBER_OF_ATTEMPTS_LIST = 5
# число попыток згрузить каждую статью
NUMBER_OF_ATTEMPTS = 3


## Ваш код
def find(text: str, kws):
    l_text = text.lower()
    for kw in kws:
        kw = kw.lower()
        pos = l_text.find(kw)

        # вариант 1 - любой фрагмент
        if pos >= 0:
            return kw

        # вариант 2 - отдельное слово
        # if (
        #     pos >= 0
        #     and (pos == 0 or not l_text[pos - 1].isalpha())
        #     and (pos + len(kw) == len(l_text) or not l_text[pos + len(kw)].isalpha())
        # ):
        #     return kw

        # можно попробовать выделять регулярками
        # words = re.findall(r"\b\w+\b", title)
        # print(words)
        # words = re.findall(r"(\w[\w'-.]*\w|\w)", title)
        # print(words)


headers = Headers(browser="chrome", os="mac").generate()

site = "https://habr.com"

sleep_time = 0
arts_textless = []
# Делаем NUMBER_OF_ATTEMPTS_LIST попыток згрузить список статей
for i in range(0, NUMBER_OF_ATTEMPTS_LIST):
    try:
        response = requests.get(site + "/ru/all/", headers=headers)
        if response.status_code != 200:
            raise (Exception(f"Status code {response.status_code}"))
        else:
            soup = bs4.BeautifulSoup(response.text, features="lxml")
            arts = soup.find_all("article")
            # иногда хабр отдает только заголовки статей без текстов, тогда тоже пробуем повиторить
            if not len(arts):
                raise Exception("Не обнаружен список статей")
            elif not arts[0].find(
                "div",
                class_="article-formatted-body article-formatted-body article-formatted-body_version-2",
            ):
                # получен список статей без текстов
                break  # продолжим рабрту с ним
                # либо можем продолжить попытки загрузть полный список
                # еcли убрать break
                arts_textless = arts
                raise Exception("Не обнаружено текстов статей")
            else:
                # Список успешно загружен
                break
    except Exception as e:
        print(f"    {e}")
    if i < NUMBER_OF_ATTEMPTS_LIST - 1:
        print(f"Не получилось загрузить список статей, повторяем попытку {i+2}/20")
    elif len(arts_textless):
        # Загрузили только список заголовков со ссылками
        arts = arts_textless
        print(f"Не получилось загрузить полный список статей")
    else:
        print(f"Не получилось загрузить список статей, завершаем программу")
        exit()
    # в случае неудачи делаем паузу, каждый раз увеличивая на секунду
    sleep(sleep_time)
    sleep_time += 1


parsed_data = []
for i, art in enumerate(arts):
    link = (
        "https://habr.com"
        + art.find("a", class_="tm-title__link").attrs["href"].strip()
    )
    title = art.find("a", class_="tm-title__link").find("span").text.strip()
    text = art.find(
        "div",
        class_="article-formatted-body article-formatted-body article-formatted-body_version-2",
    )
    text = text.text if hasattr(text, "text") else ""
    hubs = art.find_all("a", class_="tm-publication-hub__link")
    hubs_text = ""
    for hub in hubs:
        hubs_text += " " + hub.text

    time = art.find("time").attrs["title"]
    parsed_data.append(
        {
            "title": title,
            "link": link,
            "text": text,
            "time": time,
            "hubs": hubs_text,
        }
    )

for i, page in enumerate(parsed_data):
    found = find(page["title"], KEYWORDS)
    if not found:
        found = find(page["hubs"], KEYWORDS)
    if not found:
        found = find(page["text"], KEYWORDS)
    if not found:
        # Загружаем статью отдельно
        sleep_time = 1
        for i in range(0, NUMBER_OF_ATTEMPTS):
            if i > 0:
                sleep(sleep_time)
                sleep_time += 1
            try:
                response = requests.get(page["link"], headers=headers)
                if response.status_code != 200:
                    raise (Exception(f"Status code {response.status_code}"))
                else:
                    soup = bs4.BeautifulSoup(response.text, features="lxml")
                    text = soup.find("div", class_="article-formatted-body")
                    tags = soup.find_all("a", class_="tm-tags-list__link")
                    tags_text = ""
                    for tag in tags:
                        tags_text += " " + tag.text
                    page["tags"] = tags_text
                    found = find(text.text, KEYWORDS)
                    if not found:
                        found = find(tags_text, KEYWORDS)
                    break
            except Exception as e:
                print(f"    {e}")

    if found:
        print(f"{page['time']} - {page['title']} - {page['link']}")
