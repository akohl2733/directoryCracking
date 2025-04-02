import requests
from bs4 import BeautifulSoup
import re
import pymysql

# url for Jacksonville State's capital planning and facilities department
url = "https://www.jsu.edu/physicalplant/staff.html"
headers = {"User-Agent": "Mozilla/5.0"}  # avoid bot detection

# Get Page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Target keywords (case-insensitive)
keywords = re.compile(r'executive|planning|space|facilities|campus|Director', re.IGNORECASE)

# Ensure connection management with 'with' statements
db_connection = pymysql.connect(
    host="localhost",  # usually 'localhost' or the host of your MySQL server
    user="root",  # your MySQL username
    password="root",  # your MySQL password
    database="he_leads"  # the name of the database you created
)
cursor = db_connection.cursor()

staff_listing = soup.find_all("div", class_='content')

d = {}

for staff in staff_listing:
    if staff.find('h2'):
        name = "Name: " + staff.find('h2').text.strip()

    p_tags = staff.find_all('p')

    if p_tags:
        if len(p_tags) > 1:

            job = p_tags[1].text.strip()
            new_job = job.split("Telephone: ")

            if keywords.search(new_job[0]):
                print(name)
                print("job: ", new_job[0])
                print("Telephone: ", new_job[1])
                print()
