import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import pandas as pd
import numpy as np
import time

def add_height_weight_life(soup,dog_info_dict):

    h_w_life = soup.find_all(class_ = 'f-16 my0 lh-solid breed-page__hero__overview__subtitle')
    
    # There is a case when no height, weight or life on the description
    height = ""
    weight = ""
    life = ""

    for i in h_w_life: # choose the first text, there will be multiple
        if "inches" in i.text:
            height = height + "~" + i.text
        elif "pounds" in i.text:
            weight = weight + "~" + i.text
        elif "years" in i.text:
            life = i.text
    
    dog_info_dict['height'] = height
    dog_info_dict['weight'] = weight
    dog_info_dict['life'] = life
    
    return dog_info_dict

def add_traits(soup,dog_info_dict):
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
            dog_info_dict[trait_name.text] = result     
        else:    
            dog_info_dict[trait_name.text] = score
    return dog_info_dict

def add_popular_rank(soup,dog_info_dict):
    try:
        popularity_rank = soup.find('span',class_ =  "breed-page__popularity__custom-label")
        dog_info_dict["popularity_rank"] = popularity_rank.text
    except:
        dog_info_dict["popularity_rank"] = np.nan

    return dog_info_dict

def add_color(soup,dog_info_dict):
    # color info
    colors_table = soup.find(class_ =  "breed-standard__table")
    colors = colors_table.find_all(class_ = "accordion-toggle")
    color_result = ""
    for color in colors:
        if color_result == "":
            color_result = color.find('td').text
        else:
            color_result = color_result + "-" + color.find('td').text
    dog_info_dict["color"] = color_result
    return dog_info_dict

def add_mark(soup,dog_info_dict):
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
        dog_info_dict["marking"] = marking_result
    except:
        dog_info_dict["marking"] = np.nan
    return dog_info_dict

def add_breed_info(soup, dog_info_dict):

    # breed info
    breed_info = soup.find(class_ =  "breed-page__about__read-more__text")
    dog_info_dict["breed_info"] = breed_info.text

    return dog_info_dict

def add_last_info(soup,dog_info_dict):
    # health, grooming, excercise, training, nutrition
    last_info = soup.find_all(class_ = "breed-table__accordion-padding__p")
    dog_info_dict["health"] = last_info[0].text
    dog_info_dict["grooming"] = last_info[1].text
    dog_info_dict["excercise"] = last_info[2].text
    dog_info_dict["training"] = last_info[3].text
    dog_info_dict["nutrition"] = last_info[4].text
    return dog_info_dict


def extract(dog_name,driver):
    # instatiate dog info dictionary
    dog_info_dict = {'dog' : dog_name}

    url = f'https://www.akc.org/dog-breeds/{dog_name}/'
    # driver = Chrome(executable_path= '/Users/glee2/Downloads/chromedriver')
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # add info to dog_info_dict
    dog_info_dict = add_height_weight_life(soup,dog_info_dict)
    dog_info_dict = add_traits(soup,dog_info_dict)
    dog_info_dict = add_popular_rank(soup,dog_info_dict)
    dog_info_dict = add_color(soup,dog_info_dict)
    dog_info_dict = add_mark(soup,dog_info_dict)
    dog_info_dict = add_last_info(soup,dog_info_dict) # health, grooming, excercise, training, nutrition

    # driver.quit()
    return dog_info_dict
    
def main():
    dog_name_series = pd.read_csv('dog_name.csv', header= None)
    dog_name_list = [name[0] for name in dog_name_series.values]
    dog_data_dict = []

    driver = Chrome(executable_path= '/Users/glee2/Downloads/chromedriver')

    for i in range(len(dog_name_list)):
        print(f"{i}th dog {dog_name_list[i]}")
        dog_data_dict.append(extract(dog_name_list[i],driver))

    driver.quit()
    dog_data_df = pd.DataFrame(dog_data_dict)
    dog_data_df.to_csv("dog_data_09032022.csv")
    print("done")


if __name__ == "__main__":
    main()
    
