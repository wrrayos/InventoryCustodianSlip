import os
import pandas as pd
import numpy as np

class Utility:
    @staticmethod
    def number_only(val):
        if val.isdigit():
            return True
        elif val is "":
            return True
        else:
            return False

    @staticmethod
    def create_directory(directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    @staticmethod
    def transfer_files(old_directory, new_directory):
        try:
            files = []
            # Get all files from old directory
            for (dirpath, dirnames, filenames) in os.walk(old_directory):
                files.extend(filenames)

            # Move files from from old directory to new directory
            for file in files:
                os.rename(old_directory + f"\\{file}", new_directory + f"\\{file}")

            # # Deleting files of the old directory
            for file in files:
                os.remove(old_directory+f"\\{file}")

            # Deleting the old directory itself
            os.rmdir(old_directory)
        except Exception as e:
            print(e)

    @staticmethod
    def date_formatter(date, controller):
        # [0] controller = January 07 2020
        # [1] controller = 2020-01-07
        # [2] controller = Jan 07 2020

        if controller == 0:
            formatted_date = date.strftime("%B %d %Y")
            month, day, year = formatted_date.split(" ")
            return month, day, year
        elif controller == 1:
            formatted_date = date.strftime("%Y-%m-%d")
            return formatted_date
        elif controller == 2:
            formatted_date = date.strftime("%b %d %Y")
            return formatted_date

    @staticmethod
    def month_dictionary(controller,month=""):
        '''
            [0] = Month Initializer/Values
            [1] = Month Word to Number Converter
        :param controller:
        :return:
        '''
        dict_month = {}
        if controller == 0:
            dict_month = {
                'January': 1,
                'February': 2,
                'March': 3,
                'April': 4,
                'May': 5,
                'June': 6,
                'July': 7,
                'August': 8,
                'September': 9,
                'October': 10,
                'November': 11,
                'December': 12
            }
            return dict_month
        elif controller == 1:
            return dict_month[month]

    @staticmethod
    def days_generator():
        return [x for x in range(1,32)]

    @staticmethod
    def years_generator():
        return [x for x in range(2010,2050)]

    @staticmethod
    def generate_printable_report(information):
        data_frame = pd.DataFrame({
            'ICS Number':[x[0] for x in information],
            'IAR Number':[x[1] for x in information],
            'Office':[x[2] for x in information],
            'ICS Date':[Utility.date_formatter(x[3],2) for x in information],
            'Article': [x[4] for x in information],
            'Description': [x[5] for x in information],
            'Quantity': [x[6] for x in information],
            'Unit': [x[7] for x in information],
            'Amount': [x[8] for x in information],
            'Date Acquired': [Utility.date_formatter(x[9],2) for x in information],
            'Estimated Useful Life': [x[10] for x in information],
        })

        writer = pd.ExcelWriter('C:\\Users\\Wilbert\\Desktop\\ICSReport.xlsx',engine='openpyxl')
        data_frame.to_excel(writer,'Sheet1',index=False)
        writer.save()
