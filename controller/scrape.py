import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.file_handling import write_file
from termcolor import colored
from utils.logger import logger
import requests
import time

# Define headers as a constant (change this as needed)
HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://www.tops.co.th',
    'Referer': 'https://www.tops.co.th/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-algolia-api-key': '74c36eaa211b83d1a2575f9d7bdbf5dc',
    'x-algolia-application-id': 'L7MUX9U4CP',
    'Cookie': 'affinity="b847a6d59dd2597e"'
}

def configure_driver():
    # Configure Options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    # Configure Service
    service = Service()
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape(url):
    logger.info(f"Scraping: {url}")
    driver = configure_driver()
    
    try:
        res = driver.get(url)
        time.sleep(10)
        
        html = driver.page_source
        logger.info(f"Page-loaded: {driver.current_url}")       
        return html
    except Exception as e:
        logger.error(colored(f"Error scraping {url}: {str(e)}", "red", "on_red"))
        return None
    finally:
        driver.quit()

def scroll_to_bottom(driver):
    # Scroll to the bottom of the page and wait for script to finish
    script = '''
    window.scrollFinished = false;
    let scrollInterval = setInterval(() => {
        console.log("Scrolling...");
        window.scrollTo(0, document.body.scrollHeight - 1500);
    }, 250);

    let x = 0;
    let stop_script = setInterval(() => {
        console.log(`Checking scroll position: x = ${x}, window.scrollY = ${window.scrollY}`);
        if (x !== window.scrollY) {
            x = window.scrollY;
            console.log("Scroll position updated");
        } else {
            clearInterval(scrollInterval);
            clearInterval(stop_script);
            console.log("Interval cleared");
            window.scrollFinished = true;
        }
    }, 2500);
    '''
    driver.execute_script(script=script)
    
    # Wait for the JavaScript script to set window.scrollFinished to true
    start_time = time.time()
    timeout = 120  # Maximum wait time in seconds
    while True:
        is_scroll_finished = driver.execute_script("return window.scrollFinished;")
        if is_scroll_finished:
            break
        
        if time.time() - start_time > timeout:
            logger.warning("Warning: Scrolling script timeout exceeded. Proceeding...")
            break # Timeout to prevent infinite loop in case of issues
        
        time.sleep(3) # Check every 1 second

def scrape_sub_category(url):
    '''Scrapes data from a website that loads more data on scrolling using Selenium and waits for script completion.'''
    logger.info(f"Scraping: {url}")
    driver = configure_driver()

    try:
        driver.get(url)
        time.sleep(10)

        scroll_to_bottom(driver)
        time.sleep(1)
        
        html = driver.page_source
        return html
    finally:
        driver.quit()

async def get_html(product: dict, session: aiohttp.ClientSession, max_attempts: int = 20) -> tuple :
    """
    Attempts to fetch the HTML for the given URL up to max_attempts times.
    Logs each attempt and on failure logs the error.
    """
    url = product["URL"]
    for attempt in range(max_attempts):
        
        # logger.info(f"Scraping: {url} - Attempt {attempt + 1}")
        try:
            async with session.get(url, headers=HEADERS) as response:
                response.raise_for_status()  # Raise exception for non-200 responses
                html = await response.text()
                return (product,html)
        except Exception as e:
            # logger.error(f"Error scraping {url} on attempt {attempt + 1}: {str(e)}")
            if attempt < max_attempts - 1:
                logger.info(f"Retrying to scrape: {url} - Attempt {attempt + 1}")
                await asyncio.sleep(1)  # Optional delay before retrying
            else:
                logger.error(f"Failed to scrape {url} after {max_attempts} attempts.")
                return None

async def scrape_all_products(products):
    """
    Creates an aiohttp client session and concurrently executes get_html
    for all URLs provided.
    """
    # Set an overall timeout for each request if needed (adjust as per your scenario)
    timeout = aiohttp.ClientTimeout(total=160)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [get_html(product, session) for product in products]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

