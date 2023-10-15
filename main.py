import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime as date

def get_tajmahal():
    tj_menu = {
        "food":["butter chicken", "tikka masala", "tandoori", "lamb sheek",
                 "chicken madras", "tamarind potato", "veg masala", "paneer butter"],
        "price":[185, 179, 169, 179, 175, 160, 165, 175]
    }
    tajmahal_df = pd.DataFrame(tj_menu)
    return tajmahal_df

def get_bife():
    try:
        bife = requests.get("https://www.menicka.cz/4591-bife-restaurant.html")
        if str(bife) == "<Response [200]>":
            bife_content = bife.content
            bife_soup = BeautifulSoup(bife_content)
            b_soup = bife_soup.find_all("li", {"class": "polevka"})
            b_main_courses = bife_soup.find_all("li", {"class": "jidlo"})
            meals = []
            prices = []

            prices.append(b_soup[0].text.strip().split("   ")[1][-5:]) # takes the price of the soup
            meals.append(b_soup[0].text.strip().split("   ")[0]) #takes the name of the soup

            for meal in b_main_courses:
                prices.append(meal.text.strip()[-6:]) # the last 6 characters are the price + Kč
                meals.append(meal.text.strip().split("   ")[0]) #there's a big space between the meal name and alergens
            bife_df = pd.DataFrame(prices, meals)
        else:
            bife_text = ["something ain't right here dawg (response != 200)"]
            bife_df = pd.DataFrame(bife_text)
    except:
        bife_text = ["something ain't right here dawg - didn't get bife html"]
        bife_df = pd.DataFrame(bife_text)
        
    return bife_df

def get_formanka():
    try:
        formanka = requests.get("https://www.menicka.cz/2240-original-formanka-1869.html")
        if str(formanka) == "<Response [200]>":
            formanka_content = formanka.content
            formanka_soup = BeautifulSoup(formanka_content)
            f_soup = formanka_soup.find_all("li", {"class": "polevka"})
            f_main_courses = formanka_soup.find_all("li", {"class": "jidlo"})
            meals = []
            prices = []

            prices.append(f_soup[0].text.strip().split("\n")[1]) # takes the price of the soup
            meals.append(f_soup[0].text.strip().split("\n")[0]) #takes the name of the soup

            for meal in f_main_courses:
                prices.append(meal.text.strip().split("\n")[1]) 
                meals.append(meal.text.strip().split("\n")[0]) 
            formanka_df = pd.DataFrame(prices, meals)
        else:
            formanka_text = ["something ain't right here dawg (response != 200)"]
            formanka_df = pd.DataFrame(formanka_text)
    except:
        formanka_text = ["something ain't right here dawg - didn't get bife html"]
        formanka_df = pd.DataFrame(formanka_text)
        
    return formanka_df

def main():
    daytoday = date.today().strftime("%A")
    st.title(f'Menu kolem Seznamu - {daytoday}')

    # Run your custom function to process data
    tj_df = get_tajmahal()
    time.sleep(1)
    bife_df = get_bife()
    time.sleep(1)
    formanka_df = get_formanka()


    # Display the DataFrame
    st.write('Taj Mahal Express:')
    st.dataframe(tj_df)

    st.write("Bife:")
    st.dataframe(bife_df)

    st.write("Formanka:")
    st.dataframe(formanka_df)
    
    #time.sleep(21600)


if __name__ == '__main__':
    main()
