from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from utils.selenium_utils import get_chromedriver_without_proxy

from exceptions.product import ProductUnavailable


def get_product_information(driver:webdriver.Chrome, product_link: str) -> dict[str, str]:
    try:
        driver.get(product_link)
    except Exception:
        ProductUnavailable(product_link)

    try:
        sp = float(driver.find_element(By.XPATH, " //p[contains(text(), '₹')]").get_attribute('innerText').strip().strip('₹').replace(',', ''))
        mrp = float(driver.find_element(By.TAG_NAME, 'del').get_attribute('innerText').strip().strip('₹').replace(',', ''))

        if 'product is sold out' in driver.find_element(By.CLASS_NAME, 'product-select-options').get_attribute('innerText').strip().lower():
            return {
                'mrp': 'NA',
                'sp': 'NA'
            }

        return {
            'mrp': mrp,
            'sp': sp
        }
    
    except Exception:
        raise ProductUnavailable(product_link)
