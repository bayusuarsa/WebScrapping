import pandas as pd
from bs4 import BeautifulSoup
import requests


url = "https://www.audible.com/search?keywords=book&node=18573211011"
response = requests.get(url=url)
# print(response)
soup = BeautifulSoup(response.text, "html.parser")
# print(soup)

new_data = {
    "book_title": [],
    "author": [],
    "release_date": [],
    "rating": [],
    "regular_price": [],
}

raw_data = soup.find_all("li", attrs={"class":"bc-list-item productListItem"})
# print(raw_data)

for data in raw_data:
    title = data.find("h2", attrs={"class":"bc-heading bc-color-base bc-text-bold"}).get_text()
    new_data["book_title"].append(title)

    author = data.find(class_="bc-list-item authorLabel").get_text().split()[1:]
    n_author = " ".join(author)
    new_data["author"].append(n_author)

    date = data.find(class_="bc-list-item releaseDateLabel").get_text().split()[2]
    new_data["release_date"].append(date)

    rating = data.find(class_="bc-list-item ratingsLabel").get_text().lstrip("\n").rstrip()
    if rating == "Not rated yet":
        rating = 0
    else:
        rating = rating.split()[5]
    new_data["rating"].append(rating)

    price = data.find(class_="buybox-regular-price").get_text().split()[2]
    new_data["regular_price"].append(price)

filename = "audible_book.csv"
csv_export = (pd.DataFrame.from_dict(new_data))
csv_export.to_csv(filename)


