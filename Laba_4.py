import datetime
import time
from queue import Queue
from threading import Thread
import requests
from bs4 import BeautifulSoup


def get_posts(link, ququ):
    while True:
        html = requests.get(link).text
        soup = BeautifulSoup(html, "html.parser")
        kek = []
        for i in soup.find_all("div", "txt"):
            title = []
            desc = []

            for titles in i.find_all("div", "digestTitle"):
                title = titles.get_text()
            for descr in i.find_all("div", "digestDesc"):
                desc = descr.get_text()
            if title:
                kek.append({"Title:": title, "Annotation:": desc})
                if title not in all_titles:
                    all_titles.add(title)

                    ququ.put({'Title:': title,
                                'Annotation:': desc})
    time.sleep(300)  # каждые 5 минут проверяет новые новости


ququ = Queue()
link = 'https://www.tomsk.kp.ru/'
thread = Thread(target=get_posts, args=(link, ququ))
thread.start()
all_titles = set()
while True:
    if ququ.empty():
        time.sleep(300)  # проверяет очередь на новости каждые 5 минут
        print("Новых новостей нет! Проверьте чуть позже" + "\n\n\t\t\t\t\t *******")

    else:
        while not ququ.empty():
            print(ququ.get())
            print(datetime.datetime.now())
