import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path

driver = webdriver.Chrome()

driver.get("https://www.flipkart.com")
time.sleep(2)
try:
    cross = driver.find_element(By.XPATH, "/html/body/div[3]/div/span")
    cross.click()
    time.sleep(2)
except:
    print("Nothing to worry!")

search_box = driver.find_element(By.CLASS_NAME, "Pke_EE")
search_box.send_keys("mobiles")
search_btn = driver.find_element(By.XPATH, "//button[contains(@title, 'Search for Products, Brands and More')]")
search_btn.click()
time.sleep(2)

mobiles_names = []
mobile_Color = []
mobile_Storage = []
mobile_Rating = []
No_of_Ratings = []
No_of_Reviews = []
mobile_Prices = []
mobile_RAM = []
mobile_Display_Size = []
mobile_Front = []
mobile_Rear = []
No_of_cams = []
mobile_Battery_Capacity = []
for page in range(9):
    model_names = driver.find_elements(By.XPATH, "//div[@class = '_4rR01T']")
    info = driver.find_elements(By.XPATH, "//ul[@class = '_1xgFaf']")
    rate = driver.find_elements(By.XPATH, "//span[@class = '_1lRcqv']/div[@class = '_3LWZlK']")
    prices = driver.find_elements(By.XPATH, "//div[@class = '_30jeq3 _1_WHN1']")
    number_info = driver.find_elements(By.XPATH, "//span[@class = '_2_R_DZ']")
    # print("page ", page)
    # print(len(model_names), len(info), len(rate), len(number_info), len(prices))
    # print()
    for i in range(len(model_names)):
        # print("mobile phone : ", i + 1, "\n")
        ram = 0
        size_part = 0
        num_rear_cams = 0
        front_cam_mp = 0
        rear_cameras_mps = []
        battery_capacity = 0
        model_details = model_names[i].text
        color = "NULL"
        storage = 0
        if '(' in model_details:
            opening_index = model_details.find("(")
            closing_index = model_details.find(")")
            model = model_details[:opening_index].strip()
            color_rom = model_details[opening_index + 1:closing_index].strip()
            if 'B' in color_rom:
                parts = color_rom.split(',')
                color = parts[0].strip()
                # print(model_details, color, parts)
                # print(color, parts[1])
                storage = int(parts[1].split()[0])
        else:
            model = model_details
        rating_review = number_info[i].text
        parts = rating_review.split('&')
        # Extracting ratings and reviews
        ratings = int(parts[0].split()[0].replace(',', ''))
        reviews = int(parts[1].split()[0].replace(',', ''))
        # print("model name :", model, "\ncolor :", color, "\nstorage :", storage, "\nrating :", rate[i].text, "\nnumber of ratings :", ratings, "\nnumber of reviews :", reviews)
        # print("price :", prices[i].text)
        model_info = info[i].find_elements(By.XPATH, "li[@class = 'rgWa7D']")
        for j in range(len(model_info)):
            store = model_info[j].text
            if j == 0:
                if "RAM" in store:
                    if '|' in store:
                        store = store.split('|')
                        store = store[0].strip()
                    ind = store.find('B')
                    # print(store, ind)
                    if ind != -1:
                        ram += float(store[: ind - 2])
                # print("RAM :", ram)
            if j == 1:
                parts = store.split('(')
                size_part = float(parts[1].split(' inch)')[0])
                # print("Size:", size_part)
            if j == 2:
                if "Battery" in store:
                    sep = store.split()
                    battery_capacity += int(sep[0])
                elif '|' in store:
                    parts = store.split('|')
                    rear_cameras = parts[0].split('+')
                    front_cam_mp = float(parts[1].split('MP')[0])
                    rear_cameras_mps = [float(cam.split('MP')[0]) for cam in rear_cameras if "MP" in cam]
                else:
                    ind = store.find('M')
                    rear_cameras_mps.append(float(store[:ind]))
                num_rear_cams = len(rear_cameras_mps)
                # print("Number of rear cams :", num_rear_cams, "\nfront cam :", front_cam_mp, "\nrear cams :", rear_cameras_mps)
            if j == 3:
                if "Battery" in store:
                    sep = store.split()
                    battery_capacity += int(sep[0])
                # print("Battery Capacity :", battery_capacity)
        mobiles_names.append(model)
        mobile_Color.append(color)
        mobile_Storage.append(storage)
        mobile_Rating.append(float(rate[i].text))
        No_of_Ratings.append(ratings)
        No_of_Reviews.append(reviews)
        cost = int(prices[i].text[1:].replace(',', ''))
        # print(cost)
        mobile_Prices.append(cost)
        mobile_RAM.append(ram)
        mobile_Display_Size.append(size_part)
        mobile_Front.append(front_cam_mp)
        mobile_Rear.append(rear_cameras_mps)
        No_of_cams.append(num_rear_cams)
        mobile_Battery_Capacity.append(battery_capacity)
    print('page', page + 1, "is done")
    next_btn = driver.find_element(By.XPATH, "//span[text() = 'Next']")
    next_btn.click()
    time.sleep(5)

mobile_details = {
    "Mobile Name": mobiles_names,
    "Color": mobile_Color,
    "Storage (GB)": mobile_Storage,
    "Rating": mobile_Rating,
    "No. of Ratings": No_of_Ratings,
    "No. of Reviews": No_of_Reviews,
    "Price": mobile_Prices,
    "RAM (GB)": mobile_RAM,
    "Display Size (inch)": mobile_Display_Size,
    "Front (MP)": mobile_Front,
    "Rear (MP)": mobile_Rear,
    "No of cams": No_of_cams,
    "Battery Capacity (mAh)": mobile_Battery_Capacity
}

df = pd.DataFrame(mobile_details)
filepath = Path('Desktop/internship/flipkart.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath)

print("Data is successfully download")
