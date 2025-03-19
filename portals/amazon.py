import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from exceptions.product import ProductUnavailable
from utils.captcha import solve_text_captcha, report_incorrect

CAPTCHAS_SOLVED = 0


def check_for_reload(driver: webdriver.Chrome) -> None:
    alerts = driver.find_elements(By.CLASS_NAME, 'a-alert')

    for alert in alerts:
        if 'reload' in alert.get_attribute('innerText').lower():
            print('reload')
            driver.refresh()
            check_for_reload(driver)

    return


def check_for_captcha(driver: webdriver.Chrome) -> bool:
    try:
        driver.find_element(By.XPATH, '//h4[text()="Type the characters you see in this image:"]')
        return True
    except:
        return False


def solve_captcha(driver: webdriver.Chrome, logger, current_try: int = 1):
    global CAPTCHAS_SOLVED

    if current_try > 5:
        logger.error('Failed to solve captcha after 5 attempts')
        return

    if not os.path.exists('captchas'):
        os.makedirs('captchas')
    
    captcha_img = driver.find_element(By.CSS_SELECTOR, '.a-row img')
    captcha_path = os.path.join(os.getcwd(), 'captchas', 'captcha.png')
    captcha_img.screenshot(captcha_path)

    code, captcha_id = solve_text_captcha(captcha_path, logger)

    driver.find_element(By.ID, 'captchacharacters').send_keys(code)
    driver.find_element(By.TAG_NAME, 'button').click()

    time.sleep(0.5)

    if check_for_captcha(driver):
        report_incorrect(captcha_id, logger)
        return solve_captcha(driver, logger)
    else:
        logger.info('Captcha solved successfully')
        CAPTCHAS_SOLVED += 1
        return


def get_product_information(driver: webdriver.Chrome, product_link: str, logger) -> dict[str, str]:
    
    try:
        driver.get(product_link)
    except Exception:
        ProductUnavailable(product_link)

    if check_for_captcha(driver):
        solve_captcha(driver, logger)

    # check_for_reload(driver)

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
