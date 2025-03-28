# **MyAnimeList Project**  
A web scraping tool that extracts anime data from MyAnimeList and provides insights using Power BI and Neo4j.  

## **Table of Contents**  
- [Overview](#overview)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [Running the Web Scraper](#running-the-web-scraper)  
  - [Power BI Report](#power-bi-report)  
  - [Neo4j Cypher Queries](#neo4j-cypher-queries)  
- [Notes](#notes)  
  - [Setting up ChromeDriver](#setting-up-chromedriver)  


## **Overview**  
This project scrapes anime data from MyAnimeList using **Python** and **Selenium**, then processes and visualizes it:  
✅ Extracts anime titles, ratings, and descriptions  
✅ Provides a **Power BI report** for analysis  
✅ Supports **Neo4j Cypher queries** for graph-based exploration  


## **Installation**  

### **1. Clone the repository**  
    ```bash
    git clone https://github.com/zongkenchai/MyAnimeList-Web-Scraping.git
    cd MyAnimeList-Web-Scraping
    ```

### **2. Create the conda environment**  
    ```bash
    conda env create -f conda.yml
    conda activate myanimelist-env
    ```
### **3. Set up ChromeDriver**
Follow the [Setting up ChromeDriver section](#setting-up-chromedriver) to install and configure it properly.

## **Usage**
### **Running the Web Scraper**
Use the following command :

    ```bash
    python get_myanimelist_data/main.py --rank <rank> --mode <mode>
    ```
#### **Arguments**
- `--rank` (Required) 
    - Rank range to scrape (use `-` for a range, e.g., `0-1000`)
- `--mode` (Optional, default: all)
    - `all` → Get both rank and detailed information
    - `rank` → Get only rank information
    - `detail` → Get only detailed information

**Example Usage**
```
python get_myanimelist_data/main.py --rank 0-2000
python get_myanimelist_data/main.py --rank 0-2000 --mode rank
```

#### *Output*
- Scraped data is saved in:
    - `data/raw/*.feather`
    - `data/output/*.feather`
- To clean and preprocess data:
    1. Open eda.ipynb
    2. Run all the notebook cells
    3. Outputs:
        - Cleaned data: `data/cleaned/anime_cleaned.parquet`
        - Neo4j CSV files: `data/neo4j/*.csv`

---

### **Power BI Report**
1. Open `MyAnimeList_Report.pbix` in Power BI Desktop
2. Load the cleaned data: `data/cleaned/anime_cleaned.parquet`
3. Explore visualizations and insights

---

### **Neo4j Cypher Queries**
1. Start your Neo4j database and ensure it’s running
2. Import CSV data from `data/neo4j/*.csv` using [create_tables.cypher](./cipher_queries/create_tables.cypher)
3. Use Cypher queries to analyze the data
- For more details, please refer to [neo4j.md](neo4j.md)

**Example Query**
- Find the most popular anime genres:
    ```cypher
    MATCH (a:Anime)-[:HAS_GENRE]->(g:Genre)
    RETURN g.name, COUNT(DISTINCT a.anime_id) AS anime_count
    ORDER BY anime_count DESC;
    ```

## **Notes**
- Ensure your **Chrome version** matches the ChromeDriver version
- Modify `get_myanimelist_data/main.py` to customize the scraper logic
- Power BI and Neo4j scripts are optimized for this dataset; adjust as needed

### **Setting up ChromeDriver**
#### 1. Installing Chrome:
    ```bash
    sudo apt-get update
    sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
    rm ./google-chrome-stable_current_amd64.deb

    google-chrome --version
    ```

#### 2. Install ChromeDriver:
    1. Find the latest ChromeDriver version : [this list](https://googlechromelabs.github.io/chrome-for-testing/)
    2. Download and install
    ```bash
    wget https://storage.googleapis.com/chrome-for-testing-public/<<134.0.6998.88>>/linux64/chromedriver-linux64.zip

    unzip chromedriver-linux64.zip
    sudo mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver

    rm chromedriver-linux64.zip
    rm google-chrome-stable_current_amd64.deb
    rm -r chromedriver-linux64
    ```
