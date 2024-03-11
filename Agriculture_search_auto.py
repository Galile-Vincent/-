#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:02:56 2024

@author: vincent
"""

import requests
from bs4 import BeautifulSoup
import csv
import os

def fetch_data(year, item, crop):
    url = 'https://agr.afa.gov.tw/afa/pgricemeaqty_all.jsp'
    payload = {
        'accountingyear': year,
        'item': item,
        'crop': crop,
        'desc_asc': 'desc'
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

def save_to_csv(data, headers, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t')
        csv_writer.writerow(headers)
        for row in data:
            csv_writer.writerow(row)

# Loop over years
for year in range(97, 112):  # From 97 to 111
    year_str = str(year).zfill(3)  # Convert to string and pad with zeros
    
    # Loop over items
    for item in ['01', '02']:  # For both items 01 and 02
        # Loop over crops
        for crop in ['C01', 'C02', 'C03', 'C04', 'C05', 'C06']:  # For all crops from C01 to C06
            data = fetch_data(year_str, item, crop)
            
            if data:
                # Parse HTML content
                soup = BeautifulSoup(data, 'html.parser')

                # Extract headers
                headers = ["縣市鄉鎮名稱", "初步種植面積", "實際種植面積", "收穫面積", "無收穫面積", "稻穀總產量", "稻穀單位產量", "糙米總產量", "糙米單位產量"]

                # Extract data rows
                data_rows = []
                for tr in soup.find_all('tr'):
                    td_result_data = tr.find('td', class_='ResultData')
                    if td_result_data and td_result_data.text.strip() != '合計':
                        row = [td.text.strip() for td in tr.find_all('td', class_='ResultData')]
                        data_rows.append(row)

                # Define file path
                file_path = os.path.join('/Volumes/TOSHIBA EXT/Surprise', f"output_{year_str}_{item}_{crop}.csv")

                # Write to CSV
                save_to_csv(data_rows, headers, file_path)

                print(f'CSV file "{file_path}" has been generated.')
            else:
                print(f"Failed to fetch data for year {year_str}, item {item}, and crop {crop}.")
