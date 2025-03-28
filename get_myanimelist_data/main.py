#* Description: Main script to get the data from MyAnimeList
import logging
import polars as pl
import time
import os
from argparse import ArgumentParser
from pathlib import Path
from lib.anime_ranking import AnimeRanking
from lib.anime_details import AnimeDetail
from lib.web_driver import WebDriver
from lib.logging_config import logger

#* Default values
lower_rank = 0
upper_rank = 50
chunk_size = 50

if __name__ == "__main__":
    args_parser = ArgumentParser(
        description='Get MyAnimeList Data')
    
    args_parser.add_argument("--rank",
                             help="seperate the lower and upper bound by -, if only a number being given will be assumed as the upper bound",
                             dest='rank',
                             action='store',
                             required=True)
    args_parser.add_argument("--mode",
                             help="- all: Get both the rank and the detail information\n"
                                  "- rank: Get the rank information only\n"
                                  "- detail: Get the detail information only",
                             dest='mode',
                             choices=['all', 'rank', 'detail'],
                             default='all',
                             action='store',
                             required=False)
    

    #* Parsing the arguments
    args = args_parser.parse_args()
    if args.rank is not None:
        if '-' in args.rank:
            lower_rank, upper_rank = map(int, args.rank.split('-'))
        else:
            upper_rank = int(args.rank)

    mode = args.mode


    #* Set paths to the folder
    root_dir = os.getcwd()
    data_folder = os.path.join(root_dir, 'data')
    raw_folder = os.path.join(data_folder, 'raw')
    output_folder = os.path.join(data_folder, 'output')

    #* Create the folder if it does not exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if not os.path.exists(raw_folder):
        os.makedirs(raw_folder) 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    #* Get the list of page to process
    page_limit_list = [i for i in range(lower_rank,upper_rank,50)]
    logger.debug(f'Page Limit List: {page_limit_list}')
    web_driver = WebDriver()
    web_driver.start_driver()

    #* Get the list of anime between the rank specified
    if mode == 'all' or mode == 'rank':
        for page_limit in page_limit_list:
            raw_file_name = f'{page_limit}_{page_limit+50}.feather'
            raw_save_path = os.path.join(raw_folder, raw_file_name)
            logger.debug(f'Raw Save Path: {raw_save_path}')
            logger.info(f'Obtaining Anime Information from {page_limit}')
            anime_ranking = AnimeRanking()
            anime_df = anime_ranking.obtain_data_from_page(driver=web_driver.driver, lower_bound=page_limit)
            filtered_anime_df = anime_df\
                .filter((pl.col("rank") >= lower_rank) & (pl.col("rank") <= upper_rank))

            filtered_anime_df.write_ipc(raw_save_path)

        logger.info('Completed saving of the rank file')

    #* Get the detail information for a specific anime
    if mode == 'all' or mode == 'detail':
        logger.info('Getting Detail Information')
        raw_df = pl.concat([pl.read_ipc(file) for file in Path(raw_folder).glob("*.feather")])

        raw_df = (
            raw_df.unique(subset=["rank", "name"])
            .filter((pl.col("rank") >= lower_rank) & (pl.col("rank") <= upper_rank))
            .sort("rank")
        )

        logger.info(raw_df)
        no_of_rows = raw_df.height  

        for start in range(0, no_of_rows, chunk_size):
            detail_file_name = f"{start}_{start + chunk_size}.feather"
            detail_save_path = os.path.join(output_folder, detail_file_name)

            tmp_df = raw_df.slice(start, chunk_size)  

            details = []

            for row in tmp_df.iter_rows(named=True):
                rank = row["rank"]
                link = row["link"]
                logger.info(f"Getting Detail for {rank}")

                detail_dict = AnimeDetail.obtain_anime_detail(
                    driver=web_driver.driver, anime_link=link, rank=rank
                )

                row.update({k: v for k, v in detail_dict})

                details.append(row)
                time.sleep(10)

            pl.DataFrame(details).write_ipc(detail_save_path)
        
    
    web_driver.driver.quit()
    web_driver.driver = None