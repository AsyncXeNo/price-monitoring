import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from exceptions.product import ProductUnavailable


def check_for_reload(driver: webdriver.Chrome) -> None:
    alerts = driver.find_elements(By.CLASS_NAME, 'a-alert')

    for alert in alerts:
        if 'reload' in alert.get_attribute('innerText').lower():
            print('reload')
            driver.refresh()
            check_for_reload()

    return


def check_for_captcha(driver: webdriver.Chrome) -> bool:
    try:
        driver.find_element(By.XPATH, '//h4[text()="Type the characters you see in this image:"]')
        return True
    except:
        return False

def solve_captcha(driver: webdriver.Chrome) -> bool:
    time.sleep(5)
    driver.refresh()


def get_product_information(driver: webdriver.Chrome, product_link: str) -> dict[str, str]:
    
    try:
        driver.get(product_link)
    except Exception:
        ProductUnavailable(product_link)

    if check_for_captcha(driver):
        print('captcha')
        solve_captcha(driver)

    check_for_reload(driver)

    try:
        product_div = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.ID, 'ppd')
            )
        )
    except TimeoutException:
        driver.refresh()
        try:
            product_div = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.ID, 'ppd')
                )
            )
        except TimeoutException:
            raise ProductUnavailable(product_link)

    try:
        price_table = product_div.find_element(By.TAG_NAME, 'table')
        rows = price_table.find_elements(By.TAG_NAME, 'tr')

        try:
            mrp_row = rows[0]
            sp_row = rows[1]

            mrp = float(mrp_row.find_element(By.CLASS_NAME, 'a-offscreen').get_attribute('innerText').strip().strip('₹').replace(',', ''))
            sp = float(sp_row.find_element(By.CLASS_NAME, 'a-offscreen').get_attribute('innerText').strip().strip('₹').replace(',', ''))

            seller = driver.find_elements(By.CLASS_NAME, 'tabular-buybox-text')[-1].get_attribute('innerText').strip()

            try:
                driver.find_element(By.CSS_SELECTOR, '#dealBadgeSupportingText')
                deal_tag = 'Yes'
            except Exception:
                deal_tag = 'No'

            expiry_date = driver.find_element(By.CSS_SELECTOR, '#expiryDate_feature_div').get_attribute('innerText').strip().split(':')[-1].strip()
            
            return {
                'mrp': mrp,
                'sp': sp,
                'seller': seller,
                'deal tag': deal_tag,
                'expiry date': expiry_date
            }
        except Exception:
            sp_row = rows[0]
            sp = float(sp_row.find_element(By.CLASS_NAME, 'a-offscreen').get_attribute('innerText').strip().strip('₹').replace(',', ''))

            seller = driver.find_elements(By.CLASS_NAME, 'tabular-buybox-text')[-1].get_attribute('innerText').strip()
            
            try:
                driver.find_element(By.CSS_SELECTOR, '#dealBadgeSupportingText')
                deal_tag = 'Yes'
            except Exception:
                deal_tag = 'No'

            expiry_date = driver.find_element(By.CSS_SELECTOR, '#expiryDate_feature_div').get_attribute('innerText').strip().split(':')[-1].strip()

            return {
                'mrp': 'NA',
                'sp': sp,
                'seller': seller,
                'deal tag': deal_tag,
                'expiry date': expiry_date
            }
        
    except Exception:
        try:
            center_col = product_div.find_element(By.ID, 'centerCol')
            sp = float(center_col.find_element(By.CLASS_NAME, 'a-price-whole').get_attribute('innerText').strip().strip('₹').replace(',', ''))
            mrp = float(center_col.find_elements(By.CSS_SELECTOR, '#centerCol .a-text-price .a-offscreen')[-1].get_attribute('innerText').strip().strip('₹').replace(',', ''))

            seller = driver.find_elements(By.CLASS_NAME, 'tabular-buybox-text')[-1].get_attribute('innerText').strip()

            try:
                driver.find_element(By.CSS_SELECTOR, '#dealBadgeSupportingText')
                deal_tag = 'Yes'
            except Exception:
                deal_tag = 'No'

            expiry_date = driver.find_element(By.CSS_SELECTOR, '#expiryDate_feature_div').get_attribute('innerText').strip().split(':')[-1].strip()
            
            return {
                'mrp': mrp,
                'sp': sp,
                'seller': seller,
                'deal tag': deal_tag,
                'expiry date': expiry_date
            }
        
        except Exception:
            raise ProductUnavailable(product_link)
