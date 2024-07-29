import time
import requests
import selectorlib
import smtplib, ssl
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

connection = sqlite3.connect("app10-scraping-tours-sql.db")


class Event:
    def scrape(self, url):
        """Scrap the page scource from the URL"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465
        sender_email = "danish.twilio@gmail.com"
        reciver_email = "chaudharydanish024@gmail.com"
        sender_pass = "afmbdbtjakbmymeb"
        # message = "Subject: Next Upcoming Tour reminder \n\n" + message
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, reciver_email, message)
        print("Email Sent!!! ")


class Database:
    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = connection.cursor()
        cursor.execute("insert into events values(?,?,?)", row)
        connection.commit()

    def read_data(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        extracted = event.extract(event.scrape(URL))
        print(extracted)
        if extracted.lower() != "no upcoming tours":
            db = Database()
            if not db.read_data(extracted):
                db.store(extracted)
                email = Email()
                # email.send(message="Hey, new event was found")
        time.sleep(3)
