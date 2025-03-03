import requests
import json
import sqlite3


def extracting_from_api():
    url = "https://api.worldbank.org/v2/country/ZAF/indicator/NY.GDP.MKTP.CD?date=2000:2023&format=json"

    # url = "https://api.worldbank.org/v2/indicator?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        with open("gdp_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            
        print("JSON data saved successfully")
    else:
        print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
    
def clean_json():
    with open("gdp_data.json", "r") as file:
        data = json.load(file)
        
    cleaned_data = [{"year": entry["date"], "gdp": entry["value"]}
                    for entry in data[1] if entry["value"] is not None]
    
    with open("cleaned_gdp_data.json", "w") as file:
        json.dump(cleaned_data, file, indent=4)
        
    print("Data was cleaned successfully")
    return cleaned_data
    
def load_to_db(cleaned_data):
    
    conn = sqlite3.connect("finance.db")
    cursor =  conn.cursor()
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS gdp_data (
                       year INTEGER PRIMARY KEY,
                       gdp REAL
                   )
                   """)
    
    for entry in cleaned_data:
        cursor.execute("""
                       INSERT OR REPLACE INTO gdp_data (year, gdp) VALUES (?, ?)
                       """, (entry["year"], entry["gdp"]))
        
    conn.commit()
    conn.close()
    
    
import sqlite3

def view_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gdp_data")
    rows = cursor.fetchall()

    for row in rows:
        print(row)  

    conn.close()

    
        
if __name__ == "__main__":
    extracting_from_api()
    cleaned = clean_json()
    load_to_db(cleaned)
    view_db()
