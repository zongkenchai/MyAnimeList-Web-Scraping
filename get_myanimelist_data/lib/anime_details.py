import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from lib.logging_config import logger

class AnimeDetail:
    """_summary_
    To get the details of the anime from a specific anime page.    

    Returns:
        VOID
    """
    @staticmethod
    def obtain_anime_detail(driver:WebDriver, anime_link:str)->list:
        """_summary_

        Args:
            driver (Webdriver): The web driver to use
            anime_link (str): Link of the anime

        Returns:
            list(tuple):  containing the information of the anime (column name, value)
        """
        
        driver.get(anime_link)
        
        section = [i.text for i in driver.find_elements(by=By.XPATH,value="//div[@class='leftside']//h2")]
        if section[-1]=="Statistics":
            middle = driver.find_elements(by=By.XPATH,value="//div[@class='leftside']//h2[contains(text(), 'Information')]/following-sibling::div")
        else:
            before = driver.find_elements(by=By.XPATH,value="//div[@class='leftside']//h2[contains(text(), 'Information')]/following-sibling::div")
            after = driver.find_elements(by=By.XPATH,value=f"//div[@class='leftside']//h2[contains(text(), '{section[section.index('Statistics')+1]}')]/preceding-sibling::div")
            middle = [elem for elem in after if elem in before]
        
        information = [tuple([i[0],i[1].lstrip()])for i in [elem.text.split(":") for elem in middle if elem.text !=""]]
        # for i in information:
        #     row[i[0]] = i[1]
        # row = pd.DataFrame(row.to_dict(),index=[rank])
        logger.info(information)
        return information
        