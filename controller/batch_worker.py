import asyncio
import json
import time
import concurrent.futures

from termcolor import colored
from utils.file_handling import read_file, write_file
from controller.extract import extract_product  # your 
from controller.scrape import scrape_all_products   # your scraping function
from utils.logger import logger

#region Function that will be passed to pool Executor
def process_extraction(item):
    """
    calls extract_product.
    This function runs in a separate process.
    It extracts the product info from the HTML and returns the extracted product.
    """
    old_product, html = item
    product_name = old_product["URL"].split("/")[-1].replace("-", "_")
    start_time = time.time()
    
    try:
        extracted = extract_product(html)
        
        # Add the category and sub-category to the extracted product. 
        extracted["Category"] = old_product.get("Category")
        extracted["Sub_Category"] = old_product.get("Sub_Category")
        
        elapsed = time.time() - start_time
        return (product_name, extracted, elapsed)
    except Exception as e:
        return (product_name, None, f"Error: {str(e)}")
#endregion

#region Function will create 8 processes for extracting data from html
def start_process_extraction_using_ProcessPoolExecutor(items_to_process, dest_filename):
    """
    Starts the process of extracting product information using a ProcessPoolExecutor.
    This function processes a list of items in parallel using multiple processes to speed up the extraction process.
    It logs the extraction status of each product and writes the successfully extracted products to a JSON file.
    Args:
        items_to_process (list): A list of items to be processed.
        dest_filename (str): The destination filename (without extension) where the extracted products will be saved.
    Returns:
        None
    """
    start_time = time.time()
    extracted_products = []
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as process_executor:
    # Use executor.map to process the items in parallel.
        for product_name, extracted, duration in process_executor.map(process_extraction, items_to_process):
            if extracted is not None:
                extracted_products.append(extracted)
                # logger.info(colored(f"Extracted {product_name} in {duration:.2f} seconds", "cyan"))
            else:
                logger.error(colored(f"Extraction failed for {product_name}: {duration}", "red"))
    
    total_time = time.time() - start_time
    logger.info(colored(f"All Products Processed in {total_time:.2f} seconds", "blue"))
    
    # STEP 3: Write final products to file.
    if extracted_products:
        write_file(f"{dest_filename}.json", json.dumps(extracted_products, indent=4), "w")
        logger.info(colored(f"Total products extracted: {len(extracted_products)}", "blue"))
#endregion

#region Main batch worker that will process all products batch-wise
def start_main_process(src_filename,dest_filename):
    """
    Starts the main process for scraping and processing products.
    This function reads product data from a source file, scrapes the data using
    a ThreadPoolExecutor, and then processes the scraped data using a ProcessPoolExecutor.
    The processed data is saved to a destination file.
    Args:
        src_filename (str): The path to the source file containing product data.
        dest_filename (str): The base path for the destination files where processed data will be saved.
    Returns:
        None
    """
        
    st = time.time()
    batch_size = 1000
    data = json.loads(read_file(f"{src_filename}.json"))
    
    for i in range(0,len(data),batch_size):
        products = data[i:i+batch_size]
        start_time = time.time()

        # get html for all products of a batch
        results = asyncio.run(scrape_all_products(products))
        items_to_process = [res for res in results if isinstance(res,tuple)]
        logger.info(colored(f"Scraping complete. Total items scraped: {len(items_to_process)} in {time.time() - start_time}sec", "blue"))

        # process 
        start_process_extraction_using_ProcessPoolExecutor(items_to_process, f"{dest_filename}{i}")
        
    logger.info(colored(f"All Files Processed {time.time()-st}sec", "green"))
#endregion