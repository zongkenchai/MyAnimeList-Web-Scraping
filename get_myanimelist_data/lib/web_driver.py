
# Selenium and Undetected Chromedriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import undetected_chromedriver as uc
from urllib.parse import urlparse, urlunparse
import os
import time
import json
import subprocess

# Custom modules
from lib.logging_config import logger

# malaysia, thailand, philippines, vietnam, indonesia

class WebDriver:
    default_option_list = [
        '--window-size=1920,1080',
        '--headless=new',
        '--no-sandbox',
        '--enable-extensions'
        '--allow-extensions-in-incognito',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-notifications',
        '--disable-popup-blocking',
        '--disable-blink-features=AutomationControlled'
    ]
    
    driver = None

    def start_driver(self, implicitly_wait_time=2, **kwargs):
        """Starting the driver with options

        Args:
            implicitly_wait_time (int, optional): Waiting time before continue the next action . Defaults to 15.
        """
        logger.info('Starting Web Driver')

        option_list = kwargs.get('option_list', []) + self.default_option_list
                
        options = uc.ChromeOptions()
        for option in option_list :
            options.add_argument(option)
        
        #* Setting preference for network logs
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        #* Setting the request for location to be not allow by default
        
        prefs = {
            'profile.default_content_setting_values': {
                'cookies': 2,  # 2 = block cookies
                # 'images': 2,  # 2 = block images
                'plugins': 2,  # 2 = block plugins
                'popups': 2,  # 2 = block popups
                'geolocation': 2,  # 2 = block geolocation
                'notifications': 2,  # 2 = block notifications
            },
            'profile.block_third_party_cookies': True,
            'profile.default_content_settings.popups': 0,
            # 'profile.managed_default_content_settings.images': 2,
            'disk-cache-size': 4096,
            'history.clear_on_exit': True,
            'browser.cache.disk.enable': False,
            'browser.cache.memory.enable': False,
            'browser.cache.offline.enable': False,
            'network.cookie.lifetimePolicy': 2
        }

        
        options.add_experimental_option("prefs", prefs)
        
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["timeouts"] = {"pageLoad": 10000, "script": 10000} 
        
        # self.driver = uc.Chrome(options=options, page_load_timeout=20)
        self.driver = uc.Chrome(options=options)
        self.driver.implicitly_wait(implicitly_wait_time)
        logger.debug('Started Web Driver')
        
    
    def enable_developer_tools(self):
        """
        Enabling the developer tools
        """
        self.driver.execute_cdp_cmd('Network.enable', {})
        
    def prevent_file_extension_fetch(self, 
        urls=[
            "*.png",
            "*.png?*",
            
            "*.jpg",
            "*.jpg?*",
            
            "*.jpeg",
            "*.jpeg?*",
            
            "*.gif",
            "*.gif?*",
            
            "*.mp4",
            "*.mp4?*",
            
            "*.webm",
            "*.webm?*",
            
            "*.css",
            "*.css?*",
            
            "*.svg",
            "*.svg?*",
            
            "*.ico",
            "*.ico?*",
            
            "*.webp",
            "*.webp?*",
            
            "*.woff",
            "*.woff?*",
            
            "*.woff2",
            "*.woff2?*",
            
            #* Google JS Fetch
            "https://www.google.com/xjs/_/js/*",
            "https://www.gstatic.com/og/_/js/*",
            "https://www.google.com/gen_204*",
            "https://www.googleadservices.com/",
            "https://www.youtube.com",
            "https://maps.googleapis.com",
            # GA JS Fetch
            "https://www.googletagmanager.com",
            "https://www.google-analytics.com",
            "*/gtm.js?*",
            # Other not needed JS
            "https://cdn.shopify.com",
            "https://*.cloudfront.net/*.js",
            "https://static.cloudflareinsights.com"
            "https://connect.facebook.net/*",
            "https://www.facebook.com",
            "https://static.zdassets.com",
            "https://d.oracleinfinity.io",
            "https://bat.bing.com/",
            "https://i8.amplience.net/i/jpl/*",
            "https://*.monetate.net",
            "https://*.criteo.com/*",
            "https://analytics.tiktok.com",
            "https://assets.gorgias.chat",
            "https://sdk.postscript.io",
            "https://script.hotjar.com",
            "https://cdn.judge.me",
            "https://cdn.jsdelivr.net",
            "https://consent.cookiebot.co",
            "https://static.klaviyo.com",
            "https://www.clarity.ms",
            
            "*/static/*.js",
            ]):
        """
        Prevent image and video from loading
        """
        self.driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": urls})
        
    def allow_file_extension_fetch(self):
        """
        Allow all kinds of file extension
        """
        self.driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": []})

    def set_headers(self, headers:dict):
        """
        Setting the headers of the browser

        Args:
            headers (dict): Headers of the browser
        """
        logger.debug(f'Headers : {headers}')
        self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})


    def quit_driver(self):
        """
        Close the driver
        """
        logger.debug('Closing Web Driver')

        try:
            self.driver.quit()
        except:
            subprocess.run('killall chrome', shell=True)
            subprocess.run('killall chromedriver', shell=True)
        
    
    def close_tab(self):
        """
        Close the tab
        """
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        
    def open_and_switch_tab(self):
        """
        Open a new tab and switch to that new tab
        """
        self.driver.execute_script(f"window.open('', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
    def get_network_log(self)-> list:
        """
        Obtaining the network log 

        Returns:
            list: List of network logs
        """
        fully_rendered = False
        tries = 0
        while not fully_rendered and tries <= 20:
            if self.driver.execute_script("return document.readyState") == "complete":
                fully_rendered = True
            time.sleep(0.5)
            tries+=1
        return self.driver.get_log("performance")
    
    
    @staticmethod
    def get_data_usage(logs:list[dict]) -> float:
        """
        To calculate the total data usage
        Args:
            logs (list[dict]): List of Network Logs

        Returns:
            float: total network used in mb
        """
        total_mb = 0
        for network_log in logs:
            network_message = json.loads(network_log['message'])['message']
            network_method = network_message['method']
            network_params = network_message['params']
            request_id = network_params.get('requestId')
            
            if "Network.loadingFinished" == network_method:
                total_mb += network_message["params"]["encodedDataLength"]/1024/1024
                
        return total_mb

    @staticmethod
    def check_driver_exists(driver)-> bool:
        """
        Check whether the driver still exists or not
        
        Args:
            driver (_type_): web driver

        Returns:
            bool: True if browser still exists
        """
        driver_exists = None
        try:
            if driver:
                driver.window_handles
                driver_exists = True
            else:
                driver_exists = False
        except Exception as e:
            driver_exists = False
            logger.debug(f'Driver not exists : {e}')
            
        return driver_exists
    
    @staticmethod
    def normalize_url(url):
        if url:
            parsed_url = urlparse(url)
            
            normalized_path = parsed_url.path if parsed_url.path else '/'
            
            normalized_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                normalized_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment
            ))
            
            return normalized_url
        else:
            return None
    
    def get_url(self, mode=['data_transfer', 'redirected_url'], **kwargs):

        url = kwargs.get('url')
        driver = kwargs.get('driver', self.driver)
        if url:
            # logger.info(self.driver.current_url)
            driver.set_page_load_timeout(10)
            try:
                driver.get(url)
            except TimeoutError:
                logger.debug('Timeout error')
                return (None, None)
        
        logs = self.get_network_log()
        
        if kwargs.get('dump_logs'):
            logger.debug('Dumping Logs')
            with open("brand_monitor_project/selenium_logs.txt", "w", encoding="utf-8") as log_file:
                for log in logs:
                    log_file.write(json.dumps(log, ensure_ascii=False) + "\n")
                    
                    
        total_mb = None
        
        redirected_url_dict = None
        page_frame_navigated_dict = None
        
        if 'data_transfer' in mode:
            total_mb = 0
            
        if 'redirected_url' in mode:
            redirected_url_dict = {}
            page_frame_navigated_dict = {}

        
        if len(mode) == 0:
            return (None, None) 
        
        
        for network_log in logs:
            network_message = json.loads(network_log['message'])['message']
            network_method = network_message['method']
            network_params = network_message['params']
            request_id = network_params.get('requestId')
            
            if 'data_transfer' in mode:
                if "Network.loadingFinished" == network_method:
                    total_mb += network_message["params"]["encodedDataLength"]/1024/1024
            
            if 'redirected_url' in mode:
                if network_method == "Network.requestWillBeSent":
                    
                    request_type = network_params.get("initiator", {}).get("type", {})                    
                    request_referer = network_params.get("request", {}).get("headers", {}).get("Referer")
                    request_location = network_params.get("request", {}).get("url", {})
                    redirect_response = network_params.get('redirectResponse', {})
                    redirect_response_status = redirect_response.get('status')
                    redirect_response_url = self.normalize_url(redirect_response.get('url'))
                    redirect_response_location = self.normalize_url(redirect_response.get('headers', {}).get('location'))
                    
                    
                    if request_type != 'parser':
                        
                        if request_referer in redirected_url_dict.keys():
                            redirected_url_dict[request_referer]['request_type'] = request_type
                        
                        if redirect_response and redirect_response_status in [301, 302] and network_params.get('type') == 'Document': 
                            redirected_url_dict[redirect_response_url] = redirected_url_dict.get(redirect_response_url, {})
                            redirected_url_dict[redirect_response_url]['status'] = redirect_response_status
                            redirected_url_dict[redirect_response_url]['type'] = 'Temporary redirect' if redirect_response_status in [302, 307] else 'Permanent redirect'
                            
                            redirected_url_dict[redirect_response_location] = redirected_url_dict.get(redirect_response_location, {})
                            
                        # if 
                        
                elif network_method == 'Page.frameNavigated':
                    frame_location = self.normalize_url(network_params.get("frame", {}).get("url", {}))
                    if frame_location.startswith('http'):
                        # print(f'Frame Location {frame_location}')
                        redirected_url_dict[frame_location] = redirected_url_dict.get(frame_location, {})

                elif network_method == 'Network.responseReceived':
                    response_status_code = network_params.get('response').get('status')                
                    response_url = self.normalize_url(network_params.get('response').get('url'))

                    if response_url in redirected_url_dict.keys():
                        redirected_url_dict[response_url]['status'] = response_status_code
                        
                elif network_method == 'Network.responseReceivedExtraInfo':
                    response_status_code = network_params.get('statusCode')               
                    response_url = network_params.get('headers').get('location') 
                    if response_url in redirected_url_dict.keys():
                        # print(response_url, response_status_code)
                        redirected_url_dict[response_url]['status'] = response_status_code
                
                
                elif network_method == 'Page.frameRequestedNavigation':
                    request_url = self.normalize_url(network_params.get('url'))
                    request_reason = network_params.get('reason')

                    page_frame_navigated_dict[request_url] = request_reason

                
                elif network_method == 'Page.WindowOpen':
                    request_url = self.normalize_url(network_params.get('url'))

                    redirected_url_dict[request_url] = redirected_url_dict.get(request_url, {})
                    redirected_url_dict[request_url]['request_type'] = 'new_window'
                    
            
        if 'redirected_url' in mode:
            for request_url, request_type in page_frame_navigated_dict.items():
                if request_url in redirected_url_dict.keys():
                    redirected_url_dict[request_url]['initiator'] = request_type
            
            redirected_url_dict = ({k: v for k, v in redirected_url_dict.items() if k is not None})
        
        logger.info(f'Total Network Transferred MB : {total_mb}')
        
        return (redirected_url_dict, total_mb)
        
    
    def set_window_to_desired(self, resolution:str):
        """
        Setting the chormedriver window to a specific resolution

        Args:
            resolution (str): width,height
        """
        resolution_split_list = resolution.split(',')
        width, height = resolution_split_list[0], resolution_split_list[1]
        self.driver.set_window_size(width=width, height=height)