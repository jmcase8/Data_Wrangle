"""This module is a data wrangling and basic completeness/consistency checker.
Only '.zip' is supported for compressed files. 
The following are supported file types:'.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods','.odt', '.txt', '.data', '.csv', '.dat', '.tsv'
"""
import pandas as pd
import sys
import requests
import pathlib
import zipfile
import argparse
import validators

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("data", help="Url or Path to data")
#parser.add_argument("-c", "--columns", nargs="*", help="List of headers for data") #writing out the column names is tedious
#headers could be included witha true or false flag
args = parser.parse_args()
if validators.url(args.data):
    location = "external"
else:
    location = "local"

def main():
    """Main function called when running script.

    """
    try:
        if location == "local":
            df = get_data(path=args.data)
            comp_check(df)
            consis_check(df)
        elif location == "external":
            df = get_data(url=args.data)
            comp_check(df)
            consis_check(df)
    except FileNotFoundError:
        sys.exit("Ensure you have the right link or file location")


def get_data(url=None, path=None):
    """
    Takes either a https(or http) url or a local path to a zip file or file with data. If the file is a zip it will take the zip 
    and decompres it. If it is a file, it will do a completeness and consistency check of the data and write it to a "filename_result.txt".

    """
    try:
        #executes for local files
        if path != None:
            if pathlib.PurePath(path).suffix.lower() == ".zip": # unpack to directory of same name
                with zipfile.ZipFile(pathlib.PurePath(path).name, "r") as zip_ref:
                    zip_ref.extractall(pathlib.Path(path).with_suffix("").name)
                    sys.exit("Data successfully downloaded. Use local path to look at data.")
            elif pathlib.PurePath(path).suffix.lower() in ['.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods','.odt']:
                data = pd.read_excel(path) #depends on openpyxl
                return data
            elif pathlib.PurePath(path).suffix.lower() in [".txt", ".data", ".csv", ".dat"]:
                data = pd.read_csv(path, header=None)
                return data
            else:
                sys.exit('Please enter a supported file type.')
        #executes for HTTP requests
        elif url != None:
            if pathlib.Path(pathlib.Path(url).name).exists():
                sys.exit("File exists use local path.")
            else:
                r = requests.get(url, timeout=300)
                if pathlib.PurePath(url).suffix.lower() == ".zip": # if the url leads to a zip
                    # download zip
                    with open(pathlib.PurePath(url).name, "wb") as fd:
                        for chunk in r.iter_content(chunk_size=128):
                            fd.write(chunk)
                    # unpack to directory of same name
                    with zipfile.ZipFile(pathlib.PurePath(url).name, "r") as zip_ref:
                        zip_ref.extractall(pathlib.Path(url).with_suffix("").name)
                    sys.exit("Data successfully downloaded. Use local path to look at data.")

                # downloading files from a link
                elif pathlib.PurePath(url).suffix.lower() in [".txt", ".data", ".csv", ".dat", '.tsv']:
                    with open(pathlib.PurePath(url).name, "ab+") as fd:
                        for chunk in r.iter_content(chunk_size=128):
                            fd.write(chunk)
                    data = pd.read_csv(pathlib.PurePath(url).name, header=None, index_col=False)
                    return data
                elif pathlib.PurePath(path).suffix.lower() in ['.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods','.odt']:
                    data = pd.read_excel(path) #depends on openpyxl
                    return data
                    
                    return data
        elif path != None and url != None:
            sys.exit("Enter either a path or url")
        else:
            sys.exit("No path or url provided")

    except FileNotFoundError:
        sys.exit("Ensure you have the right link or file location")
    
    


def comp_check(df: pd.DataFrame) -> None:
    """
    Checks for completeness of data. This is checking to see if there is any values in the columns or in
    the rows that are missing. Columns/Rows with missing data are written to a separate file. 
    """
    #creates empty file if it does not exist
    try:
        with open(pathlib.PurePath(args.data).with_suffix("").name + ("_results.txt"), 'x'):
            pass
    except FileExistsError:
        pass

    for i, col in zip(df.isnull().sum(), df.columns):
        # checking each column for null
        if i != 0:
            with open(pathlib.PurePath(args.data).with_suffix("").name + ("_results.txt"), "a+") as f:
                f.write(f"Column {col} has {i} null\n")
        else:
            pass
    for idx, i in enumerate(df.isnull().sum(axis=1)):
        # checking each row for null
        if i != 0:
            with open(
                pathlib.PurePath(args.data).with_suffix("").name + ("_results.txt"), "a+") as f:
                f.write(f"Row {idx} has {i} null\n")
        else:
            pass


def consis_check(df: pd.DataFrame) -> None:
    """
    Checks for consistency of data. Inconsistent data is valid and accurate, but represented in multiple ways.
    Checks each column for their type. If type is "O" it is an object in pandas which means it can possibly be
    a mixutre of data types. 
    """
    #creates empty file if it does not exist
    try:
        with open(pathlib.PurePath(args.data).with_suffix("").name + ("_results.txt"), 'x'):
            pass
    except FileExistsError:
        pass
    for col in df.columns:
        if df[col].dtypes == "O":
            with open(pathlib.PurePath(args.data).with_suffix("").name + ("_results.txt"), "a+") as f:
                f.write(f"Column {col} has object type\n")
        else:
            pass


if __name__ == "__main__":
    main()