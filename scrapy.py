import requests
from bs4 import BeautifulSoup
import csv
#from lxml import etree
#from lxml import html


#DEBUG = 1
# Function to collect archive links
def pal_index(start_id, end_id, base_url="https://game8.co/games/Palworld/archives/"):
    archive_links = []
    for archive_id in range(start_id, end_id + 1):
        url = f"{base_url}{archive_id}"
        response = requests.get(url)
        if response.status_code == 200:
            archive_links.append(url)
            #print(response.content)
            '''
            if archive_id == 439909:
                #print(response.content)
            
                with open(f"archive_{archive_id}.html", "w", encoding="utf-8") as file: 
                    file.write(response.text)
            
            if DEBUG:
                if archive_id == 439909:
                    with open(f"archive_{archive_id}.html","w",encoding="utf-8")as file:
                        file.write(response.text)
            '''
        else:
            print(f"Failed to retrieve {url}: Status {response.status_code}")
    return archive_links


'''
# Function to scrape details from a single URL
def scrape_pal_details(url):
    attributes = {"Name":"N/A","HP": "N/A", "Atk": "N/A", "Def": "N/A"}
    response = requests.get(url)
    tree = etree.HTML(response.content)
    Name = tree.xpath("/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[1]/tbody/tr[2]/td[1]/b[1]/text()")
    print(response.content)
    with open(f"lapma.html", "w", encoding="utf-8") as file: 
        file.write(response.text)
    print("tree:",tree)
    print("Name:",Name)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')

    # General selector for all rows in the table, replace 'table.a-table...' with the correct selector for your table
    rows = soup.select('table.a-table > tbody > tr')

    tables = soup.find_all("tr")
    for row in tables:
        header = row.find("th", {"class": "center"})
        if header and header.text.strip() in attributes:
            value = row.find("div", {"class": "a-label"}).text
            attributes[header.text.strip()] = value

    if DEBUG:
        print(Name)
    print(attributes)
    return attributes
'''
'''
def scrape_pal_details(url):
    attributes = {"Name":"N/A", "HP": "N/A", "Atk": "N/A", "Def": "N/A"}

    response = requests.get(url)

    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    
    element_name = soup.select_one('align')

    table1 = soup.find_all("div")
    for row in table1:
        if element_name:
            Pal = element_name.get_text(strip=True)
            #Pal = element_name.get_text
            attributes["Name"] = Pal
        #if Pal and not Pal.startswith('#'):
                #attributes["Name"] = Pal

    tables = soup.find_all("tr")
    for row in tables:
        header = row.find("th", {"class": "center"})
        if header and header.text.strip() in attributes:
            value = row.find("div", {"class": "a-label"}).text
            attributes[header.text.strip()] = value
    if DEBUG:
        print(attributes)
    return attributes
'''

def scrape_pal_details(url):
    attributes = {"Name":"N/A", "HP": "N/A", "Atk": "N/A", "Def": "N/A"}

    response = requests.get(url)

    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    #doc = html.fromstring(response.content)
    
    element_name = soup.select_one('.align')

    if element_name:
        img_element = element_name.find('img')
        if img_element:
            name = img_element.get('alt')
            #attributes["Name"] = name
            if name and name.startswith('Palworld'):
                #name = img_element.get('alt')
                if name != "N/A":
                    attributes["Name"] = name
            #if DEBUG:
                #print(name)
    #attributes["Name"] = name
    
    '''
    name_elements = doc.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[4]/table[3]/tbody/tr/th/div/text()')
    if name_elements:
        name = name_elements[0].strip()  # Assume the first matching element is the name
        if name and not name.isdigit():  # Check if it's not a number (to exclude serial numbers)
            attributes["Name"] = name
    '''
    tables = soup.find_all("tr")
    for row in tables:
        header = row.find("th", {"class": "center"})
        if header and header.text.strip() in attributes:
            value = row.find("div", {"class": "a-label"}).text
            attributes[header.text.strip()] = value
    #if DEBUG:
        #print(attributes)
    return attributes
# Use the functions to collect data and write to a CSV
start_id = 439909
#end_id = 440041
end_id = 439928
archive_links = pal_index(start_id, end_id)

events_data = []
for url in archive_links:
    event_detail = scrape_pal_details(url)
    if event_detail:
        events_data.append(event_detail)

# Writing the data to a CSV file
csv_filename = 'pal_index.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Atk', 'HP', 'Def'])
    writer.writeheader()
    for event in events_data:
        writer.writerow(event)

print(f"Data written to {csv_filename}")
