import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# Function to scrape data
def scrape_contest_data(url):
    data = []
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(url)
        contest_name = find_element_with_retry(driver,(By.XPATH, "/html/body/div[2]/div/div/div/div/h1/span/a")).text
        print("Contest Name:", contest_name)

        pages_nav = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div/div/nav/ul/li")
        no_of_pages = int(driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div/nav/ul/li[{len(pages_nav)-1}]/a").text)
        print(f"No of Pages: {no_of_pages}")

        for i in range(1, 1 + 1):
        # for i in range(1, no_of_pages + 1):
            print(f"Page: {i}")

            rows = driver.find_elements(By.XPATH, "//div[@class='table-responsive']//table/tbody/tr")
            row_len = len(rows)

            for row in range (1, row_len + 1):

                rank = find_element_with_retry(driver,(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[1]")).text
                name = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[2]/a").text
                country = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[2]/span").get_attribute("data-original-title")
                score = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[3]").text
                finish_time = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[4]").text
                Q1_3 = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[5]").text
                Q1_4 = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[6]").text
                Q1_5 = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[7]").text
                Q1_6 = driver.find_element(By.XPATH,f"/html/body/div[2]/div/div/div/div/div[2]/div[2]/table/tbody/tr[{row}]/td[8]").text

                data.append({
                    "Rank": rank,
                    "Name": name,
                    "Country": country,
                    "Score": score,
                    "Finish Time": finish_time,
                    "Q1(3)": Q1_3,
                    "Q1(4)": Q1_4,
                    "Q1(5)": Q1_5,
                    "Q1(6)": Q1_6
                })

                print(f"Rank: {rank:<5} | Name: {name:<25} | Country: {country:<20} | Score: {score:<10} | Finish Time: {finish_time:<10} | Q1(3): {Q1_3:<10} | Q1(4): {Q1_4:<10} | Q1(5): {Q1_5:<10} | Q1(6): {Q1_6:<10}")

            pages_nav = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div/div/nav/ul/li")
            next_page_nav = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div/nav/ul/li[{len(pages_nav)}]/span")
            next_page_nav.click()


    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()
    
    return pd.DataFrame(data)

def find_element_with_retry(parent_element, locator, retries=5):
    for _ in range(retries):
        try:
            element = parent_element.find_element(*locator)
            return element
        except NoSuchElementException as e:
            print(f"Element not found. Retrying in 0.5 seconds. Error: {e}")
            time.sleep(0.2)
    raise NoSuchElementException("Element not found even after retries")

def main():
    st.title("LeetCode Contest Scraper")

    if "contest_data" not in st.session_state:
        st.session_state.contest_data = None
    if "contest_name" not in st.session_state:
        st.session_state.contest_name = None

    contest_url = st.sidebar.text_input("Enter Contest URL")
    scrape_button_clicked = st.sidebar.button("Scrape Data")

    contest_data = None
    search_country = None
    search_name = None

    if scrape_button_clicked and contest_url:
        st.session_state.contest_name = contest_url.split('/')[-1]
        st.write(f"Contest Name: {st.session_state.contest_name}")
        contest_data = scrape_contest_data(contest_url + '/ranking')
        st.session_state.contest_data = contest_data
        st.dataframe(st.session_state.contest_data)


    if st.session_state.contest_data is not None:
        save_button = st.button("Save to CSV")
        if save_button:
            filename = st.text_input("Enter filename", value=f"{st.session_state.contest_name}_data.csv")
            st.session_state.contest_data.to_csv(filename, index=False)
            st.success("Data saved successfully!")

    if st.session_state.contest_data is not None:
        search_name = st.text_input("Search for a user by name")
        if search_name:
            filtered_data = st.session_state.contest_data[st.session_state.contest_data["Name"].str.contains(search_name, case=False)]
            st.dataframe(filtered_data)

        search_country = st.text_input("Search for users by country")
        if search_country:
            filtered_data = st.session_state.contest_data[st.session_state.contest_data["Country"].str.contains(search_country, case=False)]
            st.dataframe(filtered_data)


if __name__ == "__main__":
    main()
