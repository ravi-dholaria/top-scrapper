import json
import time
import concurrent.futures

from termcolor import colored
from utils.file_handling import combine_json_files_in_subdirs, combine_all_json_files, write_file
from constant.constant import main_urls
from controller.worker import worker, worker_sub_category
from utils.logger import logger
from utils.filter import filter_unique_products
from controller.batch_worker import start_main_process


def process_main_category(category,cate_name,dest_dir):
    # time start
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for i in range(len(category)):
            executor.submit(worker_sub_category, category[i],cate_name,dest_dir)
            
    # time stop
    stop_time = time.time()
    logger.info(colored(f"Finished processing {cate_name} category in {(stop_time - start_time):.2f} seconds", "cyan"))
    
if __name__ == "__main__":
    
    DEST_DIR = "./Result"
    TEMP_DEST_FILE = "all_data"
    DEST_FILE = "final_data"
    start_time = time.time()
    
    # "$OPTIONAL: COMMENT OUT REGION 1 IF YOU HAVE ALREADY CONSTANTS FILE (view:"./constant/constants.py")"
    #region 1. Extract categories links 2.5 mins
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        for i in range(len(main_urls)):
            executor.submit(worker, main_urls[i])
            
    # time stop
    stop_time = time.time()
    logger.info(colored(f"Total time: {(stop_time - start_time):.2f} seconds", "blue"))
    
    #endregion
    
    #region 2. Extract all products for each sub-category from categories (Without all_image_links and product_details) 30 mins
    #Category wise stored details in Result Directory 
    
    import constant.constants as main_categories
    category_names = [
        attr for attr in dir(main_categories)
        if not attr.startswith('__') and isinstance(getattr(main_categories, attr), list)
    ]
    
    start_time_1 = time.time()
    
    for name in category_names:
        category = getattr(main_categories, name)
        logger.info(f"Starting to process category (Extracting all products url from this category): {name}")
        process_main_category(category, name, DEST_DIR)
    
    stop_time = time.time()
    logger.info(colored(f"Finished all categories in: {(stop_time - start_time_1):.2f} seconds", "blue"))
    #endregion
    
    #region 3. Combines all json files from Result directory into single json file (all_data.json)
    combine_json_files_in_subdirs(DEST_DIR, TEMP_DEST_FILE)
    #endregion
    
    # "$OPTIONAL: COMMENT OUT REGION 4 & 5 IF: one product image is sufficient and product's full description not required"
    
    #region 4. Extract all products details from all_data.json file (with all_image_links and product_details) 20 mins 
    start_main_process(TEMP_DEST_FILE,f"./final/{DEST_FILE}")
    #endregion
    
    #region 5. combine batch json files into single json file and filter unique products (view: final_data.json)
    data = combine_all_json_files(f'./final')
    write_file(f'{DEST_FILE}.json',json.dumps(data, indent=4))
    filter_unique_products(DEST_FILE, DEST_FILE)
    stop_time = time.time()
    #endregion
    
    logger.info(colored(f"Full Scrapped Top's site in {(stop_time - start_time):.2f} seconds", "green"))

    

