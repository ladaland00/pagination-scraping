import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import urllib.parse as urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# proxy
# define custom options for the Selenium driver
options = Options()

options.add_argument('--disable-blink-features=AutomationControlled')
# Define search parameters
searchPhrase = "laptop"
homeUrl = 'https://secure.lni.wa.gov/verify/Results.aspx#%7B%22firstSearch%22%3A1%2C%22searchCat%22%3A%22Name%22%2C%22searchText%22%3A%22cleaning%20services%22%2C%22Name%22%3A%22cleaning%20services%22%2C%22pageNumber%22%3A0%2C%22SearchType%22%3A2%2C%22SortColumn%22%3A%22Rank%22%2C%22SortOrder%22%3A%22desc%22%2C%22pageSize%22%3A100%2C%22ContractorTypeFilter%22%3A%5B%5D%2C%22SessionID%22%3A%22dwfuo5ldipvdrwvpofnpz1eb%22%2C%22SAW%22%3A%22%22%7D'
redirectUrl = "https://secure.lni.wa.gov/verify/Detail.aspx?"
redirectUrlVi = "https://secure.lni.wa.gov/verify/Violation.aspx?"
# Initialize an instance of the chrome driver (browser)
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)
# Visit your target site
print("Go to Home Page")
print("Loading...")
driver.get(homeUrl)
cardData = []


def scrapData(indexPage):
    listInfo = []
    print("Start scrap page", indexPage)
    print("Scraping data")
    listAllData = driver.find_elements(
        By.XPATH, "//*[contains(@id, 'resultsArea')]/div")
    for index, listData in enumerate(listAllData):
        queryStr = listData.get_attribute('id')
        companyName = listData.find_element(
            By.XPATH, "./table/tbody/tr[1]/td[1]")
        companyNameText = companyName.text
        # Store the current window handle
        main_window = driver.current_window_handle
        driver.execute_script("window.open('', '_blank');")  # Open a new tab
        driver.switch_to.window(driver.window_handles[-1])
        if queryStr.startswith("VIO="):
            driver.get(redirectUrlVi+queryStr)
            print("Go to ", redirectUrlVi+queryStr)
            try:
                # wait.until(EC.visibility_of_element_located(
                #     (By.XPATH, "//*[contains(@id, 'other')]/span/a[contains(@class, 'imgArrow')]")))
                time.sleep(5)
                try:
                    lblViolator = driver.find_element(
                        By.ID, "lblViolator").text
                    lblViolator = lblViolator.split("\n")
                    if (len(lblViolator) == 2):
                        lblViolator = lblViolator[1]
                    else:
                        lblViolator = lblViolator[0]
                except NoSuchElementException:
                    lblViolator = ""
                # if lblViolator == "":
                #     return
                try:
                    dataCategory = driver.find_element(
                        By.XPATH, "//*[contains(@id, 'violation')]/div[1]/span").text
                except NoSuchElementException:
                    dataCategory = ""
                try:
                    dataCategoryDetail = driver.find_element(
                        By.XPATH, "//*[contains(@id, 'violation')]/div[2]/span").text
                except NoSuchElementException:
                    dataCategoryDetail = ""
                try:
                    ViolationDate = driver.find_element(
                        By.XPATH, "//*[contains(@class, 'dataItem')][2]").text
                except NoSuchElementException:
                    ViolationDate = ""
                try:
                    City = driver.find_element(
                        By.XPATH, "//*[contains(@class, 'dataItem')][3]").text
                except NoSuchElementException:
                    City = ""

                print("INFO", {"BusinessDbaName": lblViolator or companyNameText,
                               "ViolationNo": dataCategory,
                               "ViolationType": dataCategoryDetail,
                               "ViolationDate": ViolationDate,
                               "City": City.split(' ')[0],
                               "State": City.split(' ')[1],
                               })
                listInfo.append({
                    "BusinessDbaName": lblViolator or companyNameText,
                    "ViolationNo": dataCategory,
                    "ViolationType": dataCategoryDetail,
                    "ViolationDate": ViolationDate,
                    "City": City.split(' ')[0],
                    "State": City.split(' ')[1],
                })

            except NoSuchElementException:
                print("No data", index)
            except TimeoutException:
                print("Time out", index)
            # After you are done with the new tab, close it
            driver.close()
            # Switch back to the main tab
            driver.switch_to.window(main_window)
        else:
            driver.get(redirectUrl+queryStr)
            print("Go to ", redirectUrl+queryStr)
            try:
                # wait.until(EC.visibility_of_element_located(
                #     (By.XPATH, "//*[contains(@id, 'other')]/span/a[contains(@class, 'imgArrow')]")))
                time.sleep(5)
                try:
                    UBINumber = driver.find_element(By.ID, "UBINumber").text
                except NoSuchElementException:
                    UBINumber = ""
                # if UBINumber == "":
                #     return
                try:
                    BusinessDbaName = driver.find_element(
                        By.XPATH, "//*[contains(@id, 'BusinessDbaName')]").text
                except NoSuchElementException:
                    BusinessDbaName = ""
                try:
                    EffectiveDate = driver.find_element(
                        By.ID, "EffectiveDate").text
                except NoSuchElementException:
                    EffectiveDate = ""
                try:
                    ExpirationDate = driver.find_element(
                        By.ID, "ExpirationDate").text
                except NoSuchElementException:
                    ExpirationDate = ""
                try:
                    Address1 = driver.find_element(
                        By.ID, "Address1").text
                except NoSuchElementException:
                    Address1 = ""
                try:
                    City = driver.find_element(
                        By.ID, "City").text
                except NoSuchElementException:
                    City = ""
                try:
                    State = driver.find_element(
                        By.ID, "State").text
                except NoSuchElementException:
                    State = ""
                try:
                    Zip = driver.find_element(
                        By.ID, "Zip").text
                except NoSuchElementException:
                    Zip = ""
                print("INFO", {"UBINumber": UBINumber,
                               "BusinessDbaName": BusinessDbaName or companyNameText,
                               "EffectiveDate": EffectiveDate,
                               "ExpirationDate": ExpirationDate,
                               "Address1": Address1,
                               "City": City,
                               "State": State,
                               "Zip": Zip})
                listInfo.append({
                    "UBINumber": UBINumber,
                    "BusinessDbaName": BusinessDbaName or companyNameText,
                    "EffectiveDate": EffectiveDate,
                    "ExpirationDate": ExpirationDate,
                    "Address1": Address1,
                    "City": City,
                    "State": State,
                    "Zip": Zip
                })

            except NoSuchElementException:
                print("No data", index)
            except TimeoutException:
                print("Time out", index)
            # After you are done with the new tab, close it
            driver.close()
            # Switch back to the main tab
            driver.switch_to.window(main_window)
    return listInfo


def scrapePage():
    global cardData
    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, 'resultItem')]")))
        try:
            itemsShowing = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@class, 'currentNumber')]")))
            indexPage = itemsShowing.get_attribute('value')
            pageCardData = scrapData(indexPage)
            cardData = cardData+pageCardData
            try:
                nextBtn = driver.find_element(
                    By.XPATH, "//*[contains(@class,'nextButton')]")
                actions.move_to_element(nextBtn)
                actions.click(nextBtn)
                actions.perform()
                scrapePage()
            except NoSuchElementException:
                print("No Btn next")
            except TimeoutException:
                print("Not Showing")
        except TimeoutException:
            print("Time out")
        except NoSuchElementException:
            print("Not Showing")
    except TimeoutException:
        print("Time out")
    except NoSuchElementException:
        print("Not Showing")


# Start scraping from the initial page
scrapePage()
print(cardData)

# Save the scraped data to a file
outputFileName = "scrapedData.json"
with open(outputFileName, "w", encoding='utf-8') as file:
    json.dump({"data": cardData}, file, indent=4, ensure_ascii=False)

print("Data saved to", outputFileName)
df = pd.DataFrame(cardData)
df.to_csv('scrapedData.csv', index=False)

print("Data saved to", cardData)
# Release the resources allocated by Selenium and shut down the browser
print("Close browser")
driver.quit()
