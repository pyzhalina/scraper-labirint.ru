import json
import random
import time

import requests
import datetime
from bs4 import BeautifulSoup
import csv


books_data = []
def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f'{cur_time}_labirint.csv', 'w', encoding='windows 1251') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Book's title",
                "Author",
                "Publishing",
                "New price",
                "Old price",
                "Sale",
                "Status"
            )
        )

    headers = {
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 100.0.4896.88Safari / 537.36',
        'accept': 'text / html, * / *;q = 0.01'
    }
    url = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display = table & page = 1'.replace(' ', '')
    responce = requests.get(url, headers=headers)
    soup = BeautifulSoup(responce.text, 'lxml')

    pages_count = int(soup.find_all('a', class_='pagination-number__text')[-1].text)
    for page in range(1, pages_count + 1):
        url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display = table & page = {page}'.replace(' ', '')
        responce = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(responce.text, 'lxml')

        books_items = soup.find('tbody', class_="products-table__body").find_all('tr')

        for bi in books_items:
            book_data = bi.find_all('td')
            try:
                book_title = book_data[0].find('a').text.strip()
            except:
                book_title = 'No title'
                
            try:
                book_author = book_data[1].find('a').text.strip()
            except:
                book_author = 'No author'
                
            try:
                book_publishing = book_data[2].find('a').text.strip()
            except:
                book_publishing = 'No publishing'
                
            try:
                book_new_price = int(
                    book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
            except:
                book_new_price = "No new price"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = "No old price"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "No sale"

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "No status"

            books_data.append(
                {
                    'book_title': book_title,
                    'book_author': book_author,
                    'book_publishing': book_publishing,
                    'book_new_price': book_new_price,   
                    'book_old_price': book_old_price,
                    'book_sale': book_sale,
                    'book_status': book_status
                }
            )
            with open(f'{cur_time}_labirint.csv', 'a', encoding='windows 1251') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )
            time.sleep(random.randrange(1, 3))
        with open(f'{cur_time}_labirint.json', 'w', encoding='windows 1251') as file:
            json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()

if __name__ == '__main__':
    main()
