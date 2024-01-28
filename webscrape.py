import psycopg2
from bs4 import BeautifulSoup
import requests
from typing import List
import json

# Connect to PostgreSQL
connection = psycopg2.connect(
    user="jeremysu",
    password="jeremy509",
    host="localhost",
    port=5432,
    database="jeremysu"
)
cursor = connection.cursor()

def scrape():
    # Link to the Clothes
    BASE_URL = 'https://global.musinsa.com/us/sale?category1DepthCode=001&page=1&sex=M&sortCode=RECOMMEND'
    HM_URL = 'https://www2.hm.com/en_us/women/new-arrivals/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=824'

    # The name of each column in our CSV file export (The data we are scraping from each project)
    HEADERS = ['Product Name', 'Price', 'Image URL', 'Web URL']

    def scrape(verbose: bool=False) -> List[List]:
        """
        Scrapes all of the submissions for Hack at UCI 2022 and return the data as a list of lists.
        Each i-th inner list represents the data scraped from the i-th project.
        
        If verbose set to True, will output all scraped data to the console.
        """
        
        project_gallery_data: List[List] = []    
        
        # There are two pages in the project gallery. Let's scrape each one
        for i in range(1):
            
            # Construct the full URL of the page we want to scrape
            url = BASE_URL
            urlHM = HM_URL
            # Make a GET request to the url to retrieve the page HTML
            page = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            pageHM = requests.get(urlHM, headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})

            # Read the page HTML into BeautifulSoup
            soup = BeautifulSoup(page.text, 'html.parser')

            print(soup.find_all('li', class_='sc-iAEawV'))

            # Loop through all of the project "tiles"
            count=0
            for project in soup.find_all('li', attrs={'class': 'sc-iAEawV'}):
                data = []
                count+=1
                print('hi')
                Product_Name = project.findChild('a', class_ = 'link').text.strip()
                Price = project.findChild('span', class_="price regular").text.strip()
                Web_URL = project.findChild('a', class_="link").get('href')
                Image_URL = project.findChild('img', class_="item-image").get('data-altimage')
                # Project Name
                data.append(Product_Name)
                # Project description
                data.append(Price)
                # Number of likes
                data.append('https:' +Image_URL)
                # Number of comments
                data.append('https://wwww.uniqlo.com' + Web_URL)
                # Link to thumbnail image           
                # Add this project's data to our list of all project data
                project_gallery_data.append(data)
                
                if verbose:
                    print('Product Name:', Product_Name)
                    print('Price:', Price)
                    print('Image URL:', 'https:' +Image_URL)
                    print('Web_URL:', 'https://wwww.uniqlo.com' + Web_URL)
        return project_gallery_data
        
    project_data = scrape(verbose=True)

    for row in project_data:
        # Split each row into words using a comma as the delimiter    
        # Now 'words' is a list containing the words in the row
        product_name = row[0]
        price = row[1]
        image_url = row[2]
        web_url = row[3]
        gender = 'female'
        print(row)
        # Insert data into the PostgreSQL table
        #cursor.execute("INSERT INTO scrapedclothes3 (product_name, price, image_url, web_url, gender) VALUES (%s, %s, %s, %s, %s)",
                #(product_name, price, image_url, web_url, gender))
    
    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()

#Once scraped, convert the images to type and color to be uploaded to database
def addColorTypes():
    with open('/Users/jeremysu/Downloads/colors-5.json') as json_file:
        data = json.load(json_file)
    count = 1

    for item in data:
        print(item)
    for item in data:
        if len(item) == 0:
            name = ''
            colors = []
        else:
            name, colors = list(item.items())[0]  # Extract 'name' and 'colors'

        # Update the 'colors' column for the specified row (where 'type' matches specified_type)
        update_query = "UPDATE scrapedclothes3 SET type = %s, colors = %s WHERE index_column = %s;"
        cursor.execute(update_query, (name, colors, count))
        count += 1

    print(count)

    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()

#Use when necessary
#scrape()
#addColorTypes()