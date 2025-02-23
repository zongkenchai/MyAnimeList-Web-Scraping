import logging
import pandas as pd
import time
import os
from argparse import ArgumentParser

from lib.anime_ranking import AnimeRanking
from lib.anime_details import AnimeDetail
from lib.web_driver import WebDriver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('get_myanimelist_data')

if __name__ == "__main__":
    args_parser = ArgumentParser(
        description='Get MyAnimeList Data')
    
    args_parser.add_argument("--rank",
                             help="seperate the lower and upper bound by -, if only a number being given will be assumed as the upper bound",
                             dest='rank', action='store')
    
    args = args_parser.parse_args()

    #* Default values
    lower_rank = 0
    upper_rank = 50
    root_dir = os.getcwd()
    data_folder = os.path.join(root_dir, 'data')
    raw_file_name = f'{int(time.time())}_{lower_rank}-{upper_rank}_raw.feather'
    raw_save_path = os.path.join(data_folder, raw_file_name)

    final_file_name = f'{int(time.time())}_{lower_rank}-{upper_rank}_final.feather'
    final_save_path = os.path.join(data_folder, final_file_name)


    main_anime_df = pd.DataFrame()

    if args.rank is not None:
        if '-' in args.rank:
            lower_rank, upper_rank = map(int, args.rank.split('-'))
        else:
            upper_rank = int(args.rank)

    
    page_limit_list = [i for i in range(lower_rank,upper_rank,50)]

    web_driver = WebDriver()
    web_driver.start_driver()

    for page_limit in page_limit_list:
        logger.info(f'Obtaining Anime Information from {page_limit}')
        anime_ranking = AnimeRanking()
        anime_df = anime_ranking.obtain_data_from_page(driver=web_driver.driver, lower_bound=page_limit)
        filtered_anime_df = anime_df[(anime_df['rank'] >= lower_rank) & (anime_df['rank'] <= upper_rank)]

        main_anime_df = pd.concat([main_anime_df, filtered_anime_df])


    main_anime_df.to_feather(raw_save_path)

    
    raw_df = pd.read_feather(raw_save_path)
    logger.info(raw_df)
    main_df = pd.DataFrame()
    
    for row in raw_df.iterrows():
        row = row[1]
        rank = row['rank']
        link = row['link']
        logger.info(f'Getting Detail for {rank}')

        
        detail_dict = AnimeDetail.obtain_anime_detail(
            driver=web_driver.driver,
            anime_link=link,
            rank=rank
        )

        for i in detail_dict:
            row[i[0]] = i[1]
        row = pd.DataFrame(row.to_dict(),index=[rank])
        main_df = pd.concat([main_df,row])
        time.sleep(10)

    main_anime_df.to_feather(final_save_path)
        
    web_driver.driver.quit()
    web_driver.driver = None