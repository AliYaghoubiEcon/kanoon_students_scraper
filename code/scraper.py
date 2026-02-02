from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
import re

# -----------------------------
# Settings
# -----------------------------

# Path to save Excel files
save_path = r"C:\Users\user\Desktop\Ra\ghaboli\1392"
os.makedirs(save_path, exist_ok=True)

# Path to chromedriver executable
chrome_path = r"C:\Users\user\Desktop\chromedriver-win64\chromedriver.exe"

# Base URL of the city page
base_url = "https://www.kanoon.ir/City/Cities/2"

# -----------------------------
# Configure Chrome WebDriver
# -----------------------------
options = Options()
options.add_argument('--start-maximized')  # Start Chrome maximized
driver = webdriver.Chrome(service=Service(executable_path=chrome_path), options=options)

# -----------------------------
# Open base page
# -----------------------------
driver.get(base_url)
time.sleep(2)

# -----------------------------
# Get list of city links
# -----------------------------
city_links = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/section/a")
num_cities = len(city_links)
print(f"Number of cities: {num_cities}")

# -----------------------------
# Loop through all cities
# -----------------------------
for i in range(1, num_cities + 1):
    driver.get(base_url)
    time.sleep(2)

    # -----------------------------
    # Access city page
    # -----------------------------
    try:
        city_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/section/a[{i}]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_element)
        raw_city_name = city_element.text.strip()
        city_name = raw_city_name.split('\n')[0]  # Clean city name
        driver.execute_script("arguments[0].click();", city_element)
        time.sleep(3)
    except Exception as e:
        print(f"⛔ Error accessing city #{i}: {e}")
        continue

    students = []

    # -----------------------------
    # Tabs XPaths and labels
    # -----------------------------
    tab_xpaths = [
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[1]/a",
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[2]/a",
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[3]/a",
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[4]/a",
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[5]/a",
    ]
    tab_labels = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"]

    # -----------------------------
    # Loop through each tab
    # -----------------------------
    for tab_xpath, tab_label in zip(tab_xpaths, tab_labels):
        try:
            tab_element = driver.find_element(By.XPATH, tab_xpath)
        except:
            print(f"❌ '{tab_label}' not found in city '{city_name}'.")
            continue

        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_element)
            driver.execute_script("arguments[0].click();", tab_element)
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error clicking '{tab_label}' in city '{city_name}': {e}")
            continue

        # -----------------------------
        # Loop through all students
        # -----------------------------
        student_index = 1
        while True:
            try:
                student_element = driver.find_element(By.XPATH,
                                                      f"/html/body/div[1]/div[2]/div[2]/div[2]/div[{student_index}]/div")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", student_element)
            except:
                break  # No more students in this tab

            # Helper function to get text safely
            def get_text(xpath):
                try:
                    return driver.find_element(By.XPATH, xpath).text.strip()
                except:
                    return ""

            # Extract student info
            name = get_text(f"/html/body/div[1]/div[2]/div[2]/div[2]/div[{student_index}]/div/h3[1]")
            school = get_text(f"/html/body/div[1]/div[2]/div[2]/div[2]/div[{student_index}]/div/h5")
            major = get_text(f"/html/body/div[1]/div[2]/div[2]/div[2]/div[{student_index}]/div/h3[2]")
            desc = get_text(f"/html/body/div[1]/div[2]/div[2]/div[2]/div[{student_index}]/div/span")

            students.append({
                "Name": name,
                "School": school,
                "Major": major,
                "Description": desc,
                "City": city_name,
                "Category": tab_label
            })

            student_index += 1

    # -----------------------------
    # Save to Excel if data exists
    # -----------------------------
    if students:
        df = pd.DataFrame(students)
        safe_city_name = re.sub(r'[\\/*?:"<>|\n\r]', "_", city_name)
        file_name = os.path.join(save_path, f"{safe_city_name}.xlsx")
        df.to_excel(file_name, index=False)
        print(f"✅ Saved: {file_name}")
    else:
        print(f"⚠️ No data found for city {city_name}.")

# -----------------------------
# Finish
# -----------------------------
driver.quit()
print("🎯 Finished scraping all cities.")
