import sys
import time
import multiprocessing
from pathos.multiprocessing import ProcessPool as Pool
from components.acm_scraper.processing import process_page, create_urls
from components.acm_scraper.csv_merger import concatenate_csv

def call_processes(url, name):
    multiprocessing.freeze_support()
    pages = process_page(url, find_pages=True, page_size=50)
    urls = create_urls(50, int(pages), url)
    
    start = time.time()
    p = Pool(multiprocessing.cpu_count() - 1)
    result = p.map(process_page, urls)
    end = time.time()
    print('Full Run: ', end - start)
    p.clear()
    
    concatenate_csv(name)
    
    return True



