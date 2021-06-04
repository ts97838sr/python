import calendar,collections,csv,datetime,filecmp,os,shutil,time,zipfile
from typing import List,Dict,Union
import pandas as pd
import xlrd

def delete_empty_folders(path):
    """
    Utility function to delete the empty directories if all underlying directories are empty
    :param path: Path to be searched and deleted if empty
    :return: Success code [0 if successful / 1 if unsuccessful]
    """
    for root,directories,files in list(os.walk(path))[1:]:
        if len(directories) == 0 and len(files) == 0:
            try:
                os.rmdir(root)
            except Exception as e:
                exit(1)
            else:
                exit(0)

def delete_all_files(path):
    """
    Recursively deletes a folder
    :param path: Path from which files are to be deleted
    :return: Success code [0 if successful / 1 if unsuccessful]
    """
    for root,directories,files in list(os.walk(path))[1:]:
        if len(files) == 0:
            exit(0)
        else:
            for f in files:
                try:
                    os.remove(os.path.join(root,f))
                except Exception as e:
                    exit(1)
                else:
                    exit(0)

def delete_files_starting_ending_with(directory: str, pattern: str,flag: str):
    """
    Deletes all files in a directory ending with the provided pattern
    :param directory: Directory where to search
    :param pattern: Search pattern
    :param flag: start or end flag [Values S-> start , E-> end]
    :return:
    """
    if not os.path.exists(directory):
        return
    if not os.path.isdir(directory):
        raise Exception("Expected a directory")
        exit(1)
    for root,dirs,files in os.walk(directory):
        if flag == 'S':
            for file in [os.path.join(root,x) for x in files if x.endswith(pattern)]:
                os.remove(file)
        elif flag == 'E':
            for file in [os.path.join(root,x) for x in files if x.startswith(pattern)]:
                os.remove(file)
        else:
            raise Exception("Flag Value not matching start or end pattern")
            exit(1)

def zip_file(input_path: str,output_path: str):
    """
    Zips a file at the input path and writes it to output path
    :param input_path: The file to zip
    :param output_path: The target path of the zipped path
    :return: Success code [0 if successful / 1 if unsuccessful]
    """
    with zipfile.ZipFile(
        file=output_path,
        mode='w',
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9
    ) as zf:
        try:
            zf.write(input_path,arcname=os.path.split(input_path)[1])
        except Exception as e:
            exit(1)
        else:
            exit(0)

def get_csv_field_names(full_file_path: str):
    """
    Gets the field names of a csv file
    :param full_file_path: path of a csv file
    :return: csv header in a python dictionary
    """
    with open(full_file_path, 'r') as f:
        return csv.DictReader(f).fieldnames

def days_in_month(year: int, month: int) -> int:
    """
    Calculates the number of days in a provided year and month
    :param year: Year of the date
    :param month: Month of the date
    :return: The number of days in the provided year and month
    """
    return calendar.monthrange(year,month)[1]

def end_of_next_month(year: int,month: int) -> datetime.date:
    """
    Calculates the date that represents the end of the next month after the provided year and month
    :param year: Year of the date (YYYY Type Integer)
    :param month: Month of the date (MM Type Integer)
    :return: Date
    """
    if month == 12:
        month = 1
        year += 1
    else:
        month +=1
    return datetime.date(year,month, days_in_month(year,month))

def end_of_month(year: int,month: int) -> datetime.date:
    """
    Calculates the date that represents the end of the month after the provided year and month
    :param year: Year of the date (YYYY Type Integer)
    :param month: Month of the date (MM Type Integer)
    :return: Date
    """
    return datetime.date(year,month, days_in_month(year,month))

def start_of_next_month(year: int,month: int) -> datetime.date:
    """
    Calculates the date that represents the start of the month after the provided year and month
    :param year: Year of the date (YYYY Type Integer)
    :param month: Month of the date (MM Type Integer)
    :return: Date
    """
    return end_of_month(year,month) + datetime.timedelta(days=1)


