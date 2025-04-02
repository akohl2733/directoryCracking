import requests
from bs4 import BeautifulSoup
import re
import pymysql

url = "https://www.lsu.edu/pdc/about/staff.php"
headers = {"User-Agent": "Mozilla/5.0"}  # avoid bot detection

# Get Page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Target keywords (case-insensitive)
keywords = re.compile(r'executive|planning|space|facilities|campus', re.IGNORECASE)

# Ensure connection management with 'with' statements
with pymysql.connect(
    host="localhost",
    user="root",
    password="root",  # Ensure this is the correct password
    database="he_leads"
) as db:  # This ensures the connection is automatically closed when the block ends
    # Using 'with' for cursor to ensure proper handling
    with db.cursor() as cursor:
        # Test insert to verify connection is working
        sql = "INSERT INTO staff (name, title, email, university) VALUES (%s, %s, %s, %s)"

        # Extract staff data from the webpage
        for row in soup.select('table tr')[1:]:  # Skip header row
            cols = row.select('td')
            if len(cols) >= 3:  # Ensure it's a valid row
                name = cols[0].get_text(strip=True)
                title = cols[1].get_text(strip=True)
                email = cols[2].get_text(strip=True)

                if keywords.search(title):  # Filter by role
                    values = (name, title, email, "LSU")
                    cursor.execute(sql, values)

        # Commit the scraped data
        db.commit()
        print(f"Inserted {cursor.rowcount} rows of staff data.")
