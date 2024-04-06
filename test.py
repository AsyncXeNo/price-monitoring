#!venv/bin/python3

import utils.config as _

from loguru import logger

from pyvirtualdisplay import Display
from utils.selenium_utils import get_chromedriver_without_proxy, get_chromedriver_with_proxy
from portals.amazon import get_product_information as get_amazon_product_information
from portals.flipcart import get_product_information as get_flipcart_product_information
from portals.one_mg import get_product_information as get_one_mg_product_information
from portals.nykaa import get_product_information as get_nykaa_product_information
from portals.hyugalife import get_product_information as get_hyugalife_product_information
from utils.sheets import get_amazon_data, get_flipcart_data, get_1mg_data, get_nykaa_data, get_hyugalife_data, compile_data
from utils.mail import send_output_mail, send_error_mail
from exceptions.product import ProductUnavailable


HOST = 'brd.superproxy.io'
PORT = '22225'
USER = 'brd-customer-hl_8805587a-zone-pricemon_willthiswork'
PASS = '125h0s4vd7nh'


if __name__ == '__main__':
    logger.info('starting script')

    disp = Display()
    disp.start()
    
    driver = get_chromedriver_without_proxy()
    

    amazon_output = []
    flipcart_output = []
    one_mg_output = []
    nykaa_output = []
    hyugalife_output = []

    # Fetch data
    try:
        logger.info('loading data')
        amazon_data = get_amazon_data()[:5]
        flipcart_data = get_flipcart_data()[:5]
        one_mg_data = get_1mg_data()[:5]
        nykaa_data = get_nykaa_data()[:5]
        hyugalife_data = get_hyugalife_data()[:5]
    except Exception as e:
        logger.error(e)
        # send_error_mail('Error while loading data from google sheet')
        exit()

    driver.get(amazon_data[-1]['Url'])

    logger.info('scraping amazon data')
    for entry in amazon_data:
        try:
            ASIN = entry['ASIN']
            Product = entry['Product']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = entry['Url']
            if (Url.strip() == ''): 
                logger.earning(f'skipping amazon product, ASIN: {ASIN}')
                continue
            try:
                scraped = get_amazon_product_information(driver, Url)
                logger.debug(f'scraped amazon product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA', 'seller': 'NA'}
                logger.error(f'amazon product not found: {Url}')
            amazon_output.append({
                'ASIN': ASIN,
                'Product': Product,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'seller': scraped['seller'],
                'Url': Url
            })
        except KeyError:
            logger.error('Amazon data structure has been changed')
            # send_error_mail('Amazon sheet data structure has been changed')
            exit()
        
    driver.close()

    driver = get_chromedriver_with_proxy(HOST, PORT, USER, PASS)
        
    logger.info('scraping flipcart data')
    for entry in flipcart_data:
        try:
            Id = entry['Id']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = entry['Url']
            try:
                scraped = get_flipcart_product_information(driver, Url)
                logger.debug(f'scraped flipcart product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA', 'seller': 'NA'}
                logger.error(f'flipcart product not found: {Url}')
            flipcart_output.append({
                'Id': Id,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'seller': scraped['seller'],
                'Url': Url
            })
        except KeyError:
            logger.error('Flipkart data structure has been changed')
            # send_error_mail('Flipcart sheet data structure has been changed')
            exit()

    driver.close()

    driver = get_chromedriver_without_proxy()

    logger.info('scraping 1mg data')
    for entry in one_mg_data:
        try:
            Id = entry['Id']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = entry['Url']
            try:
                scraped = get_one_mg_product_information(driver, Url)
                logger.debug(f'scraped 1mg product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA'}
                logger.error(f'1mg product not found: {Url}')
            one_mg_output.append({
                'Id': Id,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'Url': Url
            })
        except KeyError:
            logger.error('1mg data structure has been changed')
            # send_error_mail('1mg sheet data structure has been changed')
            exit()
    
    logger.info('scraping nykaa data')
    for entry in nykaa_data:
        try:
            Id = entry['Id']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = entry['Url']
            try:
                scraped = get_nykaa_product_information(driver, Url)
                logger.debug(f'scraped nykaa product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA'}
                logger.error(f'nykaa product not found: {Url}')
            nykaa_output.append({
                'Id': Id,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'Url': Url
            })
        except KeyError:
            logger.error('Nykaa data structure has been changed')
            # send_error_mail('Nykaa sheet data structure has been changed')
            exit()
    
    logger.info('scraping hyugalife data')
    for entry in hyugalife_data:
        try:
            Id = entry['Id']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = entry['Url']
            try:
                scraped = get_hyugalife_product_information(driver, Url)
                logger.debug(f'scraped hyugalife product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA'}
                logger.error(f'hyugalife product not found: {Url}')
            hyugalife_output.append({
                'Id': Id,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'Url': Url
            })
        except KeyError:
            logger.error('Hyugalife data structure has been changed')
            # send_error_mail('Hyugalife sheet data structure has been changed')
            exit()
        
    driver.close()

    disp.stop()

    logger.info('data scraping complete, compiling...')
        
    compile_data(amazon_output, flipcart_output, one_mg_output, nykaa_output, hyugalife_output)

    logger.info('compilation complete, emailing...')

    # send_output_mail()

    logger.info('script has run to completion!')
