from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from exceptions.product import ProductUnavailable


def get_product_information(driver: webdriver.Chrome, product_link: str) -> dict[str, str]:
    try:
        driver.get(product_link)
    except Exception:
        ProductUnavailable(product_link)

    try:
        sp = float(WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '._30jeq3._16Jk6d')
            )
        ).get_attribute('innerText').strip().strip('₹').replace(',', ''))
        try:
            mrp = float(driver.find_element(By.CSS_SELECTOR, '._3I9_wc._2p6lqe').get_attribute('innerText').strip().strip('₹').replace(',', ''))
        except Exception: 
            mrp = 'NA'

        seller = driver.find_element(By.ID, 'sellerName').find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').get_attribute('innerText').strip()

        return {
            'mrp': mrp,
            'sp': sp,
            'seller': seller
        }
    
    except Exception:
        raise ProductUnavailable(product_link)
