import time
import requests 
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
import json

counter = 1
start_url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
driver = Chrome()

def get_all_products_urls(start_url):
    urls = []
    html = requests.get(start_url)
    if html.status_code == 200:
        soup = bs(html.text,'html.parser')
        section = soup.find('section',{'class':'cmp-category__main-content'})
        item_urls = section.find_all('a',{'class':'cmp-category__item-link'})
        for item_url in item_urls:
            urls.append('https://www.mcdonalds.com/' + item_url['href'])
        return urls
    else:
        pass

def getProductDetailInfoHtml(url):
    try:
        driver.get(url=url)
        time.sleep(4)
        html = driver.page_source
        return bs(html,'html.parser')
    except Exception as ex:
        print(ex)
        
        


def get_product_detail_info(url):
    soup = getProductDetailInfoHtml(url)
    
    info_array = soup.find_all('li',{"class":'cmp-nutrition-summary__heading-primary-item'})
    
    add_info_array = soup.find('div',{'class':'cmp-nutrition-summary cmp-nutrition-summary--nutrition-table'}).find_all('li',{'class':'label-item'})
    
    desc_list = get_list_of_description(info_array)
    
    add_desc_list = get_add_list_of_description(add_info_array)
    
    name = soup.find('span',{'class':'cmp-product-details-main__heading-title'}).text
    description = soup.find('div', {'class':'cmp-product-details-main__description'}).find('div',{'class':'cmp-text'}).text.replace('\n','').replace('\t','')
    calories = desc_list[0]
    fats = desc_list[1]
    carbs = desc_list[2]
    proteins = desc_list[3]
    unsaturated_fats = add_desc_list[0]
    sugar = add_desc_list[1]
    salt = add_desc_list[2]
    portion = add_desc_list[3]
    
    data = {
        'name': name,
        'description':description,
        'calories':calories,
        'fats':fats,
        'carbs':carbs,
        'proteins':proteins,
        "unsaturated_fats":unsaturated_fats,
        'sugar':sugar,
        'salt':salt,
        'portion':portion
    }
    
    return data


def get_add_list_of_description(add_info_array):
    list_of_text = []
    currentString = str()
    list_of_add_descriptions = []
    for element in add_info_array:
        list_of_text.append(element.find('span',{'class':'sr-only'}).text)

    for element in list_of_text:
        currentString = element.replace('\n','').replace('\t','').replace('  ','')
        list_of_add_descriptions.append(currentString)
    return list_of_add_descriptions


def get_list_of_description(info_array):
    list_of_text = []
    currentString = str()
    list_of_descriptions = []
    for element in info_array:
        list_of_text.append(element.find('span',{'class':'sr-only sr-only-pd'}).text)

    for element in list_of_text:
        currentString = element.replace('\n','').replace('\t','').replace('  ','')
        list_of_descriptions.append(currentString)
    return list_of_descriptions


def get_all_products_info(urls):
    full_data = {}

    global counter

    for url in urls:
        full_data[counter] = get_product_detail_info(url)
        counter += 1

    with open('data.json', 'w') as file:
        json.dump(full_data, file,skipkeys=False, ensure_ascii=True,
                   check_circular=True, allow_nan=True, cls=None, indent=None,
                     separators=None, default=None, sort_keys=False,)
    driver.close()
    driver.quit()
    

get_all_products_info(get_all_products_urls(start_url))
             

