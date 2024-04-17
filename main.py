import argparse
from get_donamonya_text import save_text
import os
from datetime import datetime, date
import re
from renamefilename_fullwidth_to_halfwidth import fullwidth_to_halfwidth 


parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default="doya_text_download")
parser.add_argument("--start_date", type=str, default='')
parser.add_argument("--end_date", type=str, default='20301201')
args = parser.parse_args()


def formatted_date(date_str):
    numbers = re.findall(r'\d+', date_str)

    year = numbers[0]
    month = numbers[1]
    day = numbers[2]

    new_date = f'{year}年{month}月{day}日'
    return new_date


if args.start_date == '':
    # Represent an empty string as the minimum date
    most_recent_date = date(year=1990, month=1, day=1)
    if os.path.exists(args.path):
        for file_name in os.listdir(args.path):
            # Extract the date part from the file name
            file_name_date_str = re.split('[（(　『「]', file_name)[0]
            new_file_name_date_str = fullwidth_to_halfwidth(file_name_date_str)

            new_file_name_date_str = new_file_name_date_str.replace('某', '01')
            new_file_name_date_str = formatted_date(new_file_name_date_str)

            # Convert the date part to a datetime object
            file_date = datetime.strptime(new_file_name_date_str, '%Y年%m月%d日').date()
            
            if file_date > most_recent_date:
                most_recent_date = file_date
            
    end_date_datetime = datetime.strptime(args.end_date, '%Y%m%d')
    print(most_recent_date,most_recent_date,args.path)
    break
    save_text(most_recent_date, end_date_datetime, args.path)
else:
    start_date_datetime = datetime.strptime(args.start_date, '%Y%m%d')
    end_date_datetime = datetime.strptime(args.end_date, '%Y%m%d')
    save_text(start_date_datetime, end_date_datetime, args.path)