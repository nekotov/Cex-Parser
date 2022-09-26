import requests
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

cur .execute("CREATE TABLE IF NOT EXISTS products (boxId TEXT, boxName TEXT, categoryName TEXT, categoryFriendlyName TEXT, superCatName TEXT, superCatFriendlyName TEXT, sellPrice REAL)")
con.commit()

def run_job(num):
    global con, cur
    response = requests.get(f'https://wss2.cex.nl.webuy.io/v3/boxlists/hotproducts?superCatId=*&firstRecord={num}&count=50')
    data = response.json()
    for item in data["response"]["data"]['boxlistsBoxes']:
        cur.execute(
            "INSERT INTO products (boxId, boxName, categoryName, categoryFriendlyName, superCatName, superCatFriendlyName, sellPrice) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (item["boxId"], item['boxName'], item['categoryName'], item['categoryFriendlyName'], item['superCatName'],
             item['superCatFriendlyName'], item['sellPrice']))
    con.commit()
    print(f'Inserted {num} - {num + 50}')

if __name__ == '__main__':
    max_items = requests.get("https://wss2.cex.nl.webuy.io/v3/boxlists/hotproducts?superCatId=*&firstRecord=1&count=1").json()["response"]["data"]["totalRecords"]
    for i in range(max_items//50+1):
        run_job(i*50)

