#This is Project 3 for Python Analytics

# Standard library imports
import csv
import pathlib 
import json
import logging
from collections import Counter

# External library imports (requires virtual environment)
import requests   # type: ignore
import pandas # type: ignore

# Local module imports
import utils_dobler.py
import dobler_project_setup.py

logging.basicConfig(level=logging.INFO)



def fetch_and_write_txt_data(folder_name, filename, url):
     try:
        response = requests.get(url)
        response.raise_for_status()
        write_txt_file(folder_name, filename, response.text)
     except requests.exceptions.RequestException as err:
        logging.error(f"Error fetching text data: {err}")


def write_txt_file(folder_name, filename, data):
        file_path = pathlib.Path(folder_name).join_path(filename) 
        with file_path.open('w') as file:
             file.write(data)
        logging.info(f"Text data saved to {file_path}")


def fetch_txt_data(folder_name, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
    
        file_path = pathlib.Path(folder_name) / 'data.txt'
        with open(file_path, 'w') as file:
            file.write(response.text)
        print(f"Text data saved to {file_path}")

    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")


def process_txt_file(dataset_name, filename, url):
    folder_path = create_folder('txt', dataset_name) 
    text_data = fetch_and_write_txt_data(folder_path, filename, url)
    if text_data:
        text_data = text_data.replace('-', ' ').replace('/', ' ')
        clean_text = re.sub(r'[^A-Za-z\s]', '', text_data).lower()
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        words = clean_text.split()
        word_count = len(words)
        unique_words = set(words)
        word_freq = Counter(words)
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        letter_count = sum(1 for char in text_data if char.isalpha())

        analysis = (
            f"Total Word Count: {word_count}\n"
            f"Unique Words Count: {len(unique_words)}\n"
            f"Total Letter Count: {letter_count}\n\n"
            "Top 10 Most Frequent Words:\n"
        )
        for word, freq in sorted_word_freq[:10]:
            analysis += f"{word}: {freq}\n"
        write_txt_file(folder_path, f"analysis_{filename}", analysis)



def fetch_and_write_excel_data(folder_name, filename, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        write_excel_file(folder_name, filename, response.content)
    except requests.exceptions.RequestException as err:
        logging.error(f"Error fetching Excel data: {err}")


####
#CSV
####
def fetch_and_write_csv_data(folder_name, filename, url):
    """Fetch csv data from the given URL and write it to a file."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        write_csv_file(folder_name, filename, response.content.decode('utf-8'))
    except requests.exceptions.RequestException as err:
        logging.error(f"Error fetching CSV data: {err}")

def write_csv_file(folder_name, filename, data):
    file_path = pathlib.Path(folder_name) / filename
    with file_path.open('w', newline='') as file:
        file.write(data)
    logging.info(f"CSV data saved to {file_path}")

def process_csv_file(folder_name, filename, output_filename):
    """Process CSV data to summarize row and column information."""
    file_path = pathlib.Path(folder_name) / filename
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = [row for row in reader]
            summary = f"Rows: {len(data)}\n"
            summary += f"Columns: {header}\n"
            with open(output_filename, 'w') as output_file:
                output_file.write(summary)
        logging.info(f"Processed CSV data saved to {output_filename}")
    except IOError as e:
        logging.error(f"I/O error({e.errno}): {e.strerror}")



def write_excel_file(folder_path, filename, data):
    file_path = folder_path.joinpath(filename)
    try:
        folder_path = pathlib.Path(folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(data)
            print(f"Excel data saved to {file_path}")
    except IOError as e:
        print(f"IOError while writing file: {e}")
    except OSError as e:
        print(f"OSError while creating directories: {e}")
    except Exception as e:
        print(f"Unexpected error while writing file: {e}")
    finally:
        print("Operation attempted.")
    return file_path


def main():
    ''' Main function to demonstrate module capabilities. '''

    print(f"Name: {yourname_attr.my_name_string}")

    txt_url = 'https://shakespeare.mit.edu/romeo_juliet/full.html'

    csv_url = 'https://raw.githubusercontent.com/MainakRepositor/Datasets/master/World%20Happiness%20Data/2020.csv' 

    excel_url = 'https://github.com/bharathirajatut/sample-excel-dataset/raw/master/cattle.xls' 
    
    json_url = 'http://api.open-notify.org/astros.json'

    txt_folder_name = 'data-txt'
    csv_folder_name = 'data-csv'
    excel_folder_name = 'data-excel' 
    json_folder_name = 'data-json' 

    txt_filename = 'data.txt'
    csv_filename = 'data.csv'
    excel_filename = 'data.xls' 
    json_filename = 'data.json' 

    fetch_and_write_txt_data(txt_folder_name, txt_filename, txt_url)
    fetch_and_write_csv_data(csv_folder_name, csv_filename,csv_url)
    fetch_and_write_excel_data(excel_folder_name, excel_filename,excel_url)
    fetch_and_write_json_data(json_folder_name, json_filename,json_url)

    process_txt_file(txt_folder_name,'data.txt', 'results_txt.txt')
    process_csv_file(csv_folder_name,'data.csv', 'results_csv.txt')
    process_excel_file(excel_folder_name,'data.xls', 'results_xls.txt')
    process_json_file(json_folder_name,'data.json', 'results_json.txt')

if __name__ == '__main__':
    main()
