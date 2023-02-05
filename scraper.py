from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = 'https://idbop.mylicense.com/verification/Search.aspx'
cdPath = Service('C:/Users/asus/Downloads/chromedriver.exe') #ChromeDriver loc
driver = webdriver.Chrome(service=cdPath)
driver.get(website)

f_name = []
m_name = []
l_name = []
lic_no = []
lic_type = []
status = []
orig = []
expiry = []
renewed = []

time.sleep(5)

##### Fill necessary fields #####
licenseType = Select(driver.find_element(By.ID, 't_web_lookup__license_type_name'))
licenseType.select_by_value('Pharmacist') #option for selecting License Type

lastNameClear = driver.find_element(By.ID, 't_web_lookup__last_name').clear()
lastNameSearch = driver.find_element(By.ID, 't_web_lookup__last_name').send_keys("L") #option for Last Name input

search = driver.find_element(By.ID, 'sch_button')
search.click()

time.sleep(5)

##### Function for table searching and updating of list ##### 
def table_search():
    names_from_table = driver.find_elements(By.XPATH, "//table[starts-with(@id, 'datagrid_results')]/tbody/tr/td/table/tbody/tr/td/a")

    for name_from_table in names_from_table:
        name_from_table.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
            
        f_name.append(driver.find_element(By.XPATH, "//span[contains(@id, 'first_name')]").text)
        m_name.append(driver.find_element(By.XPATH, "//span[contains(@id, 'm_name')]").text)
        l_name.append(driver.find_element(By.XPATH, "//span[contains(@id, 'last_name')]").text)
        lic_no.append(driver.find_element(By.XPATH, "//span[contains(@id, 'license_no')]").text)
        lic_type.append(driver.find_element(By.XPATH, "//span[contains(@id, 'license_type')]").text)
        status.append(driver.find_element(By.XPATH, "//td[2]/span[contains(@id, 'status')]").text)
        orig.append(driver.find_element(By.XPATH, "//td[4]/span[contains(@id, 'issue_date')]").text)
        expiry.append(driver.find_element(By.XPATH, "//td[6]/span[contains(@id, 'expiry')]").text)
        renewed.append(driver.find_element(By.XPATH, "//td[6]/span[contains(@id, 'last_ren')]").text)

        close_button = driver.find_element(By.ID, 'btn_close')
        close_button.click()
        driver.switch_to.window(driver.window_handles[0])
            
        time.sleep(5)
    return

##### Initial execution of function #####
table_search()

pages = driver.find_elements(By.XPATH, '//table/tbody/tr[42]/td/a')
maxPg = (len(pages))


##### Iteration to get every data per page results #####
for page_selector in range(maxPg):
    nav = page_selector + 1
    driver.find_element(By.XPATH, "//table/tbody/tr[42]/td/a[{}]".format(int(nav))).click()
    time.sleep(5)

    table_search()

time.sleep(5)
driver.quit()

##### Creation of Data Frame #####
df = pd.DataFrame({
    'First Name': f_name, 
    'Middle Name': m_name, 
    'Last Name': l_name, 
    'License Number': lic_no, 
    'License Type': lic_type, 
    'Status': status, 
    'Original Issued Date': orig, 
    'Expiry': expiry, 
    'Renewed': renewed})

df.to_csv('Idaho_License.csv', index=True)
print(df) # Display output .csv file