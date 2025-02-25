import time

from utils.logger import logger
from controller.scrape import scrape, scrape_sub_category
from controller.extract import extract_main_category_links, extract_products
from utils.file_handling import write_file
from termcolor import colored

def retry(func, start_time, *args, **kwargs):
    page_name = kwargs.get("page_name")
    logger.error(colored(f"{page_name} failed in: {time.time() - start_time} seconds", "light_red"))
    logger.info(colored(f"Retrying: {page_name}", "yellow"))
    func(kwargs.get("url"))

def worker(url):
    start_time = time.time()
    page_name = url.split("/")[-1].replace("-", "_")

    # get html
    html = scrape(url)

    # extract details
    logger.info(colored(f"Extracting Links from: {page_name}", "green"))
    body = extract_main_category_links(html, page_name)

    #retry
    if body == False:
        retry(worker, start_time, url=url, page_name=page_name)
        return

    # write to file
    write_file(f"./constant/constants.py", body, "a")
    stop_time = time.time()
    logger.info(colored(f"Link extraction for {page_name} completed in {(stop_time - start_time):.2f} seconds", "cyan"))

def worker_sub_category(url, cate_name,dest_dir):
    start_time = time.time()
    try:
        html = scrape_sub_category(url)
        sub_cate_name = url.split("/")[-1].replace("-", "_")

        logger.info(colored(f"Extracting products from sub-category: {sub_cate_name}"))
        products = extract_products(html,url)

        write_file(f"./{dest_dir}/{cate_name}/{sub_cate_name}.json", products)
    except Exception as e:
        logger.error(colored(f"Error encountered in sub-category {cate_name}/{sub_cate_name}: {str(e)}", "red", "on_red"))

        stop_time = time.time()
        logger.info(colored(f"Product extraction for {cate_name}/{sub_cate_name} completed in {(stop_time - start_time):.2f} seconds", "cyan"))

