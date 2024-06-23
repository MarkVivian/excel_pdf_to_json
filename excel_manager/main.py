import excel_manipulation as ex
import refurbish_info
import sql_script

if __name__ == "__main__":
    # Define the path to the Excel file
    file_path = './info/ALL STAFF DATA BASE-MEDICAL COMPREHENSIVE April, 2024 rm hr.xlsx'

    # Create an instance of the Excel class with the given file path
    excel_processor = ex.Excel(file_path)

    # Process the Excel file and retrieve the data
    data = excel_processor.process_excel()
    # Check for redundancy

    rf = refurbish_info.Refurbish()

    rf.write_to_json("./json_files/info.json", data)

    rf.check_redundancy()

    sql_script.Scripter()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
