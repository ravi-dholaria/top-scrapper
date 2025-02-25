import re
import json

from bs4 import BeautifulSoup
from termcolor import colored
from utils.logger import logger

def extract_quantity(product_name):
    """
    Extracts quantity from a product name using regex.

    Args:
        product_name: The name of the product (string).

    Returns:
        The quantity string if found (e.g., "200g", "250ml"), otherwise None.
    """
    quantity_regex = re.search(r'(\d+\.?\d*)([gG]|[mM][lL]|[kK][gG]|[lL]|[c][c])\.?', product_name)
    if quantity_regex:
        quantity_value = quantity_regex.group(1)
        quantity_unit = quantity_regex.group(2).lower()
        # print(product_name,"|-->",quantity_value, quantity_unit)

        if quantity_unit == 'g':
            return f"{quantity_value}g"
        elif quantity_unit == 'ml':
            return f"{quantity_value}ml"
        elif quantity_unit == 'kg':
            return f"{quantity_value}kg"
        elif quantity_unit == 'l':
            return f"{quantity_value}l"
        elif quantity_unit == 'cc':
            return f"{quantity_value}cc"
    return "null"

def extract_main_category_links(html, page_name):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find("div", {"class": "productlisting"}).find("div", {"class": "plp-carousels"}).find_all("a", {"class": "plp-carousel__link"})
    
    if not links:
        logger.info(colored(f"No links found in {page_name}", "red"))
        return False
    
    res_list = ["https://www.tops.co.th/en" + link.get("href", "") if not link.get("href", "").startswith("https://www.tops.co.th") else link.get("href", "") for link in links ]
    response = f"{page_name} = {json.dumps(res_list, indent=2)}\n"
    
    return response

def extract_products(html,url):
    soup = BeautifulSoup(html, 'lxml')
    
    # extract total products as li tags from ol tag
    ol_tag = soup.find("div",{"class":"algolia-search--plp"}).find("div", {"class": "hits"}).find("ol")
    main_category = url.split("/")[-2].replace("-","_")
    sub_category = url.split("/")[-1].replace("-","_")
    
    # li tag have article tag that contains product information
    article_tags = ol_tag.find_all("article")
    
    if len(article_tags) == 0: 
        raise Exception("Error: Something went wrong. No products found.")

    response = []
    for article in article_tags:
        product = {
            "Product_Name": article.get('data-product-name'),
            "Product_Images": [article.get('data-product-image-url')],
            "Quantity": extract_quantity(article.get('data-product-name')),
            "Barcode_Number": article.get('data-sku'),
            "Product_Detail": None,
            "Price": article.get('data-product-price'),
            "Labels": [article.get('data-product-categories'),article.get('data-product-brand')],
            "Stock": article.get('data-product-stock'),
            "URL": article.get('data-product-url'),
            "Category": main_category,
            "Sub_Category": sub_category
        }
        response.append(product)
    
    return json.dumps(response, indent=4)
    
def extract_product(html):
    
    if not html:
        raise Exception("Error: No HTML content found.")
    soup = BeautifulSoup(html, 'lxml')
    
    url = soup.find("meta", {"property": "og:url"}).get("content")
    sku = soup.find("body").get("data-sku")
    meta = soup.find("script", {"id":"meta-schema","type": "application/ld+json"}).text
    meta = json.loads(meta)
    name = meta["name"]
    price = meta["offers"]["price"]
    
    data_div = soup.find("div",{"class":"product-Details-page-root"})  
    #region Extract product images
    # document.querySelector("#default > div > div.large-5.column > div > div.xzoom-thumbs").querySelectorAll("div > a")
    links = data_div.find("div",{"class":"xzoom-thumbs"})
    images = []
    if not links:
        links = data_div.find("div",{"class":"xzoom-container"}).find("img",{"class":"xzoom"})
        images.append(links.get("src"))
    else:
        for link in links.find_all("a"):
            images.append(link.get("href"))
    #endregion        
   
    #region Extract product detail
    #document.querySelector("#panelsStayOpen-collapseOne > div").textContent
    product_detail = data_div.find("div",{"id":"panelsStayOpen-collapseOne"})
    if not product_detail:
        product_detail = "No product detail found."
    else:
        product_detail =  product_detail.text.replace("\n","").replace("\t","").replace("  ","")
    #endregion

    result = {
        "Product_Name": name,
        "Product_Images": images,
        "Quantity": extract_quantity(name),
        "Barcode_Number": sku,
        "Product_Detail": product_detail,
        "Labels": [data_div["data-product-categories"],data_div["data-product-brand"]],
        "Price": price,
        "URL": url
    }
    return result
