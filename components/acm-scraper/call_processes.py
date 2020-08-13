import sys
import time
import multiprocessing
from csv_merger import concatenate_csv
from pathos.multiprocessing import ProcessPool as Pool
from processing import process_page, create_urls, parse_search_term

def call_processes(url, pages):
    urls = create_urls(50, int(pages), url)
    
    start = time.time()
    p = Pool(multiprocessing.cpu_count() - 1)
    result = p.map(process_page, urls)
    end = time.time()
    print('Full Run: ', end - start)
    p.clear()


if __name__ == "__main__":
    multiprocessing.freeze_support()

    search_term = sys.argv[1]
    pages = sys.argv[2]

    call_processes(search_term, pages)


