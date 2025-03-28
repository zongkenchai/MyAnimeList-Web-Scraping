import pandas as pd
import polars as pl
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from lib.logging_config import logger

class AnimeRanking:
    """
    To get the list of animes from the top anime page from myanimelist.net
    """


    def __init__(self):
        self.base_link = 'https://myanimelist.net/topanime.php'

    def __get_link(self, lower_bound):
        """
        Returns the link to the page with the anime ranking
        """
        return f'{self.base_link}?limit={lower_bound}'


    def obtain_data_from_page(self, driver:WebDriver, lower_bound:int) -> pl.DataFrame:
        """_summary_

        Args:
            driver (WebDriver): The web driver to use
            lower_bound (int): If the value is 50, means that the first anime in the page is the 51th anime in the ranking

        Returns:
            pl.DataFrame: The list of animes within that page
        """
        link = self.__get_link(lower_bound=lower_bound)
        
        driver.get(link)
        rank_of_anime = [int(i.text) for i in driver.find_elements(by=By.CSS_SELECTOR, value="tr.ranking-list .rank span")]
        name_of_anime = [i.text for i in driver.find_elements(by=By.CSS_SELECTOR, value="tr.ranking-list div.detail .di-ib h3 a")]
        link_of_anime = [i.get_attribute("href") for i in driver.find_elements(by=By.CSS_SELECTOR, value="tr.ranking-list div.detail .di-ib h3 a")]
        scores = [float(i.text) for i in driver.find_elements(by=By.CSS_SELECTOR, value="tr.ranking-list td.score span.score-label")]
        anime_df = pl.DataFrame({
            "rank": rank_of_anime,
            "name": name_of_anime,
            "link": link_of_anime,
            "score": scores
        })


        return anime_df

    