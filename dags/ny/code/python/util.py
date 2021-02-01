import requests
import time
import logging


def get_county_response(county_url):
    try:
        start = time.time()
        logging.info("Trying to access url: {}".format(county_url))
        r = requests.get(url=county_url)
        logging.info("Status Code: {}".format(str(r.status_code)))
        if r.status_code == 200:
            data = r.json()
            end = time.time()
            logging.info("Time taken to get response from url {} is {} secs!".format(county_url, end-start))
            return data
        else:
            logging.info("Unable to extract the NY COVID 19 data from url: {} with status code: {}".format(
                county_url, r.status_code))
            raise NotImplemented
    except Exception as e:
        logging.error("Error occurred while accessing url: {} Error: {}".format(county_url, e))


def prepare_insert_sql(table, rows):
    data = str(rows).replace('[', '').replace(']', '')
    sql = """INSERT INTO
        {}(test_date, county, new_positives, cumulative_number_of_positives, 
            total_number_of_tests, cumulative_number_of_tests)
        VALUES 
        {}
    """
    return sql.format(table, data)
