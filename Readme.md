# ✨ **Tops Scraper** ✨

## 🚀 **Project Overview**

This project is a web scraping assignment to extract product data from **Tops Online**: [Tops Online](https://www.tops.co.th/en). The main goal is to scrape product details from various categories and store the data in a structured format.

## 🗺️ **Approach**

### ➡️ **Step 1: Extract Main Categories Links**

- The main category URLs are stored in `constant.py`.
- Extract "view all" URLs of sub-categories for each main category.
- Store these URLs as lists in `constants.py`.

### ➡️ **Step 2: Extract Products Info (Without Details)**

- Visit each sub-category page and scroll to the bottom to get all products of that sub-category.
- Extract basic product information (name, one image, price, etc.) and store it in the `Result` folder, categorized by main category.
- Combine all data from the `Result` folder into a single `all_data.json` file.

### ➡️ **Step 3: Extract Full Product Details**

- Visit each product page to get all images and full product descriptions.
- Loop over the URLs in `all_data.json` in batches and store the detailed data in the `final` folder.
- Implement a retry mechanism to ensure data is fetched even if initial attempts fail.

### ➡️ **Step 4: Combine and Filter Data**

- Combine all data from the `final` folder into a single `final_data.json` file.
- Filter out unique products from `final_data.json`.

## ⚙️ **Dependencies**

- Required Python packages are listed in `requirements.txt`.

## 🚀 **How to Run the Script**

1. **Install the required packages:**

   ```sh
   pip install -r requirements.txt

   ```

2. Ensure the following before running the script:

   - Delete the [final](http://_vscodecontentref_/0) and [Result](http://_vscodecontentref_/1) folders if they exist. They will be auto-generated.
   - Delete [constants.py](http://_vscodecontentref_/2) (not [constant.py](http://_vscodecontentref_/3)). Ignore the yellow line in [main.py](http://_vscodecontentref_/4) at line 48.

3. Run the main script:

   ```sh
   python main.py
   ```

## Challenges Faced

- **Scrolling to Bottom**: Ensuring all products are loaded by scrolling to the bottom of each sub-category page.
- **Retry Mechanism**: Implementing a retry mechanism to handle failed requests and ensure data completeness.

## Performance and Extraction Metrics

This section provides an overview of the performance and estimated extraction times for various stages of the web scraping process. With approximately 14,000 products to extract, the time and reliability for extracting product data can vary based on the extraction method used.

### Extracting Main Categories Links:

- **Time:** ~3 minutes
- **Description:** Extracting all category links, including sub-categories, takes around 3 minutes to complete.

### Extracting Products Info (Without Product Description and all images):

- **Time:** ~30 minutes
- **Description:** Extracting basic product information (name, one image, price) without product details takes approximately 30 minutes.

### Extracting Full Product Details (Including All Images and Descriptions):

- **Time:** ~1 hour
- **Description:** Retrieving full product details, including all images and descriptions, requires about 1 hour. This is due to sending 14,000 requests to the server, plus retries for failed attempts.

### Product Detail Extraction Success Rate:

- **Every 1,000 products:** On average, 3 product details are not successfully extracted.

### Time to Extract 1,000 Product Data:

- **Time:** ~2.5 minutes
- **Description:** Scraping data for 1,000 products (after acquiring direct product URLs) takes approximately 2.5 minutes.

These time metrics reflect the performance of the script during various stages of the extraction process. By optimizing the retry mechanism and managing requests efficiently, data extraction can be completed smoothly, even for large product datasets like the one from Tops Online.

## Sample Output

Here is a sample output of 5 products:

```json
[
  {
    "Product_Name": "Singha Drinking Water 600ml. Pack 12",
    "Product_Images": [
      "https://assets.tops.co.th/SINGHA-SinghaDrinkingWater600mlPack12-8850999321028-1?$JPEG$"
    ],
    "Quantity": "600ml",
    "Barcode_Number": "8850999321028",
    "Product_Detail": "Properties:Stay hydrated throughout the day with SINGHA Drinking Water, purified drinking water that features breakthrough technology such as Smart Micro Filter, making Singha Drinking Water is more than just clean but packed with vital minerals for your body.\u2022 SINGHA Drinking Water\u2022 Meticulous manufacturing process\u2022 SINGHA's breakthrough technology Smart Micro Filter that ensures the best drinking water quality for consumers\u2022 More than just clean but packed with vital minerals for your body\u2022 Calcium: maintains strong bones and prevents osteoporosis\u2022 Magnesium: regulates muscle and nerve function\u2022 Silica: helps oxygenate the skin and improve skin elasticityThe product received may be subject to package modification and quantity from the manufacturer.We reserve the right to make any changes without prior notice.*The images used are for advertising purposes only.",
    "Labels": ["Beverages /// Bottled Water /// Drinking Water", "SINGHA"],
    "Price": "55",
    "URL": "https://www.tops.co.th/en/singha-drinking-water-600ml-pack-12-8850999321028",
    "Category": "beverages",
    "Sub_Category": "bottled_water"
  },
  {
    "Product_Name": "Singha Drinking Water 1.5ltr. Pack 6",
    "Product_Images": [
      "https://assets.tops.co.th/SINGHA-SinghaDrinkingWater15ltrPack6-8850999320021-1?$JPEG$"
    ],
    "Quantity": "1.5l",
    "Barcode_Number": "8850999320021",
    "Product_Detail": "Properties:Stay hydrated throughout the day with SINGHA Drinking Water, purified drinking water that features breakthrough technology such as Smart Micro Filter, making Singha Drinking Water is more than just clean but packed with vital minerals for your body.\u2022 SINGHA Drinking Water\u2022 Meticulous manufacturing process\u2022 SINGHA's breakthrough technology Smart Micro Filter that ensures the best drinking water quality for consumers\u2022 More than just clean but packed with vital minerals for your body\u2022 Calcium: maintains strong bones and prevents osteoporosis\u2022 Magnesium: regulates muscle and nerve function\u2022 Silica: helps oxygenate the skin and improve skin elasticityThe product received may be subject to package modification and quantity from the manufacturer.We reserve the right to make any changes without prior notice.*The images used are for advertising purposes only.",
    "Labels": ["Beverages /// Bottled Water /// Drinking Water", "SINGHA"],
    "Price": "55",
    "URL": "https://www.tops.co.th/en/singha-drinking-water-15ltr-pack-6-8850999320021",
    "Category": "beverages",
    "Sub_Category": "bottled_water"
  },
  {
    "Product_Name": "Pure Life Drinking Water 600ml. Pack 12",
    "Product_Images": [
      "https://assets.tops.co.th/PURELIFE-PureLifeDrinkingWater600mlPack12-8850124003874-1?$JPEG$",
      "https://assets.tops.co.th/PURELIFE-PureLifeDrinkingWater600mlPack12-8850124003874-2?$JPEG$",
      "https://assets.tops.co.th/PURELIFE-PureLifeDrinkingWater600mlPack12-8850124003874-3?$JPEG$"
    ],
    "Quantity": "600ml",
    "Barcode_Number": "8850124003874",
    "Product_Detail": "Properties:The product received may be subject to package modification and quantity from the manufacturer.We reserve the right to make any changes without prior notice. *The images used are for advertising purposes only.",
    "Labels": ["Beverages /// Bottled Water /// Drinking Water", "PURE LIFE"],
    "Price": "66",
    "URL": "https://www.tops.co.th/en/pure-life-drinking-water-600ml-pack-12-8850124003874",
    "Category": "beverages",
    "Sub_Category": "bottled_water"
  },
  {
    "Product_Name": "Crystal Water 1.5ltr. Pack 6",
    "Product_Images": [
      "https://assets.tops.co.th/CRYSTAL-CrystalWater15ltrPack6-8851952350796-1"
    ],
    "Quantity": "1.5l",
    "Barcode_Number": "8851952350796",
    "Product_Detail": "Properties:The product received may be subject to package modification and quantity from the manufacturer.We reserve the right to make any changes without prior notice. *The images used are for advertising purposes only.",
    "Labels": ["Beverages /// Bottled Water /// Drinking Water", "CRYSTAL"],
    "Price": "55",
    "URL": "https://www.tops.co.th/en/crystal-water-15ltr-pack-6-8851952350796",
    "Category": "beverages",
    "Sub_Category": "bottled_water"
  },
  {
    "Product_Name": "Crystal Water 600ml. Pack 12",
    "Product_Images": [
      "https://assets.tops.co.th/CRYSTAL-CrystalWater600mlPack12-8851952350789-1?$JPEG$",
      "https://assets.tops.co.th/CRYSTAL-CrystalWater600mlPack12-8851952350789-2?$JPEG$",
      "https://assets.tops.co.th/CRYSTAL-CrystalWater600mlPack12-8851952350789-3?$JPEG$",
      "https://assets.tops.co.th/CRYSTAL-CrystalWater600mlPack12-8851952350789-4?$JPEG$"
    ],
    "Quantity": "600ml",
    "Barcode_Number": "8851952350789",
    "Product_Detail": "Properties:The product received may be subject to package modification and quantity from the manufacturer.We reserve the right to make any changes without prior notice. *The images used are for advertising purposes only.",
    "Labels": ["Beverages /// Bottled Water /// Drinking Water", "CRYSTAL"],
    "Price": "59",
    "URL": "https://www.tops.co.th/en/crystal-water-600ml-pack-12-8851952350789",
    "Category": "beverages",
    "Sub_Category": "bottled_water"
  }
]
```
