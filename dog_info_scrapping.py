import requests
from dog_name import *
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import pandas as pd
import numpy as np
import time
   

def extract(dog_name):
    url = f'https://www.akc.org/dog-breeds/{dog_name}/'
   
    driver = Chrome(executable_path= '/Applications/chromedriver')
    driver.get(url)
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    h_w_life = soup.find_all(class_ = 'f-16 my0 lh-solid breed-page__hero__overview__subtitle')
    h = np.nan
    w = np.nan
    life = np.nan
    # Height, Weight, life
    h_list = []
    w_list = []
    life_list = []
    for i in h_w_life:
        if "inches" in i.text:
            h_list.append(i.text)
        elif "pounds" in i.text:
            w_list.append(i.text)
        elif "years" in i.text:
            life_list.append(i.text)
    if len(h_list) > 0:
        h = h_list[0]
    if len(w_list) > 0:
        w = w_list[0]
    if len(life_list) >0:
        life = life_list[0]

    job_result = {
    'dog' : dog_name,
    'height': h,
    'weight': w,
    'life_expectancy': life}

    # all traits
    traits = soup.find_all(class_ = "breed-trait-group__trait-all")
    for trait in traits:
        trait_name = trait.find(class_ = "breed-trait-group__header breed-trait-group__header-closed")
        score = str(trait).count("filled")
        if trait_name.text == 'Coat Type' or trait_name.text == 'Coat Length':
            properties = trait.find_all(class_= "breed-trait-score__choice--selected")
            result = ""
            for property in properties:
                if result == "":
                    result = property.text
                else:
                    result = result + "-" + property.text
            job_result[trait_name.text] = result     
        else:    
            job_result[trait_name.text] = score

    # Popularity, there are cases when no pop exists

    try:
        popularity_rank = soup.find('span',class_ =  "breed-page__popularity__custom-label")
        job_result["popularity_rank"] = popularity_rank.text
    except:
        job_result["popularity_rank"] = np.nan

    # color info
    colors_table = soup.find(class_ =  "breed-standard__table")
    colors = colors_table.find_all(class_ = "accordion-toggle")
    color_result = ""
    for color in colors:
        if color_result == "":
            color_result = color.find('td').text
        else:
            color_result = color_result + "-" + color.find('td').text
    job_result["color"] = color_result

    # marking, no marking exist
    marking_result = ""
    marking_table = soup.find(id =  "markings-t-h").find('tbody')
    try:
        marking_rows = marking_table.find_all('tr')
        marking_result = ""
        for marking in marking_rows:
            if marking_result == "":
                marking_result = marking.find('td').text
            else:
                marking_result = marking_result + "-" + marking.find('td').text
        job_result["marking"] = marking_result
    except:
        job_result["marking"] = np.nan

    # breed info
    breed_info = soup.find(class_ =  "breed-page__about__read-more__text")
    job_result["breed_info"] = breed_info.text

    # health, grooming, excercise, training, nutrition
    last_info = soup.find_all(class_ = "breed-table__accordion-padding__p")
    job_result["health"] = last_info[0].text
    job_result["grooming"] = last_info[1].text
    job_result["excercise"] = last_info[2].text
    job_result["training"] = last_info[3].text
    job_result["nutrition"] = last_info[4].text
    driver.quit()
    return job_result
    
def main():
    name_array[81] = 'cirneco-delletna'
    name_array[124] = 'Grand-Basset-Griffon-Vendeen'
    name_array[164] = 'Lowchen'
    name_array[193] = 'Petit-Basset-Griffon-Vendeen'
    whole_data = []
    for i in range(len(name_array)):
        print(f"{i}th dog {name_array[i]}")
        whole_data.append(extract(name_array[i]))
        if i %10 == 0:
            df = pd.DataFrame(whole_data)
            df.to_csv("dog_data.csv")
    df = pd.DataFrame(whole_data)
    df.to_csv("dog_data.csv")
    print("done")


if __name__ == "__main__":
    main()
    
