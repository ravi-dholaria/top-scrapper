import json
from utils.logger import logger 
from utils.file_handling import write_file , read_file

def filter_unique_products(src_filename, dest_filename):
    """
    Read a JSON file containing product data and filter out duplicate products based on the barcode number.
    Write the filtered products to a new JSON file.
    """
    seen = set()
    final = []
    repeated = []

    data = read_file(f"{src_filename}.json")
    products = json.loads(data)

    for product in products:
        barcode = product["Barcode_Number"]
        if barcode in seen:
            repeated.append(barcode)
        else:
            final.append(product)
            seen.add(barcode)
    write_file(f"{dest_filename}.json", json.dumps(final, indent=4))
    logger.info(f"Total products: {len(products)}")
    logger.info(f"Repeated products: {len(repeated)}")
    logger.info(f"Unique products: {len(final)}")

