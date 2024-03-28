from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from utils.selenium_utils import get_chromedriver_without_proxy

from exceptions.product import ProductUnavailable


def get_product_information(driver:webdriver.Chrome, product_link: str) -> dict[str, str]:
    # my_driver = get_chromedriver_without_proxy()
    
    try:
        driver.get(product_link)
    except:
        ProductUnavailable(product_link)

    try:
        mrp = float(driver.find_element(By.CLASS_NAME, 'css-u05rr').find_element(By.TAG_NAME, 'span').get_attribute('innerText').strip().strip('₹').replace(',', ''))
        sp = float(driver.find_element(By.CLASS_NAME, 'css-1jczs19').get_attribute('innerText').strip().strip('₹').replace(',', ''))

        return {
            'mrp': mrp,
            'sp': sp
        }
    
    except:
        raise ProductUnavailable(product_link)
    finally:
        # driver.close()
        pass
