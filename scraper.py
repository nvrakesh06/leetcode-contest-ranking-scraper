from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import csv

def find_element_with_retry(driver, locator, retries=5):
    for _ in range(retries):
        try:
            element = driver.find_element(*locator)
            return element
        except NoSuchElementException as e:
            print(f"Element not found. Retrying in 0.5 seconds. Error: {e}")
            time.sleep(0.2)
    raise NoSuchElementException("Element not found even after retries")

csvfile = open('C:\\Users\\Rakesh Reddy NV\\OneDrive\\Documents\\OWN\\Projects (after getting placed)\\Random\\Leetcode-contest-rank-search\\contest_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csvfile)
csv_writer.writerow(['Rank', 'Name', 'Country', 'Score', 'Finish Time', 'Q1(3)', 'Q1(4)', 'Q1(5)', 'Q1(6)'])

url = 'https://leetcode.com/contest/weekly-contest-392/ranking'
driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get(url)
    contest_name = find_element_with_retry(driver,(By.XPATH, "/html/body/div[2]/div/div/div/div/h1/span/a")).text
    print("Contest Name:", contest_name)

    pages_nav = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div/div/nav/ul/li")
    no_of_pages = int(driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div/nav/ul/li[{len(pages_nav)-1}]/a").text)
    print(f"No of Pages: {no_of_pages}")

    for i in range(1, no_of_pages + 1):
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


            print(f"Rank: {rank:<5} | Name: {name:<25} | Country: {country:<20} | Score: {score:<10} | Finish Time: {finish_time:<10} | Q1(3): {Q1_3:<10} | Q1(4): {Q1_4:<10} | Q1(5): {Q1_5:<10} | Q1(6): {Q1_6:<10}")
            csv_writer.writerow([rank, name, country, score, finish_time, Q1_3, Q1_4, Q1_5, Q1_6])


        pages_nav = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div/div/nav/ul/li")
        next_page_nav = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div/nav/ul/li[{len(pages_nav)}]/span")
        next_page_nav.click()


except Exception as e:
    print("Error:", e)

finally:
    driver.quit()