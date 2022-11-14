import datetime, xlrd
import os



class ProcessSheet:
    '''Process an excel file by giving the filename'''


    def __init__(self,filename):
        '''Declare an initialize some variables'''
        self.filename = filename
        self.workbook, self.sheet_1 = self.open_file()
        self.row_count, self.col_count = self.get_row_column_count()
    

    def open_file(self):
        '''Open the file with xlrd and initialize workbook and sheet variables'''

        self.workbook = xlrd.open_workbook(self.filename)
        return self.workbook,self.workbook.sheet_by_index(0)

    def get_row_column_count(self):
        '''return the row and column count'''

        return self.sheet_1.nrows, self.sheet_1.ncols


    def process_file(self):

        '''process file and return the output list'''
        result_dict = {}
        line_number_row = None
        line_number_column = None
        for cur_row in range(0, self.row_count):
            for cur_col in range(0, self.col_count):
                cell = self.sheet_1.cell(cur_row, cur_col)
                if cell.value == "Quote Number":
                    result_dict["Quote Number"] = self.sheet_1.cell(cur_row, cur_col+1).value
                elif cell.value == "Date":
                    a1_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(self.sheet_1.cell(cur_row, cur_col+1).value, self.workbook.datemode)).strftime("%Y-%m-%d")

                    result_dict["Date"] = a1_as_datetime
                elif cell.value == "Ship To":
                    result_dict["Ship To"] = self.sheet_1.cell(cur_row, cur_col+1).value
                elif cell.value == "Ship From":
                    result_dict["Ship From"] = self.sheet_1.cell(cur_row, cur_col+1).value
                elif "Name" in str(cell.value):
                    result_dict["Name"] = cell.value.split(":")[1]
                elif cell.value == "LineNumber":
                    line_number_row = cur_row
                    line_number_column = cur_col
        result_list = []
        for cur_row in range(line_number_row, self.row_count):
            value_dict = {}

            for cur_col in range(0, self.col_count):
                
                cell = self.sheet_1.cell(cur_row, cur_col)
                if cur_row > line_number_row:
                    
                    if not (cell.value == None  or cell.value == "") and self.sheet_1.cell(line_number_row, cur_col).value in ["LineNumber","PartNumber","Price","Description"] :
                        value_dict[self.sheet_1.cell(line_number_row, cur_col).value]=cell.value

            if len(value_dict) > 0:            
                result_list.append(value_dict)
            


        result_dict["Items"] = result_list 
        return result_dict  





class ProcessSheetTest:
    '''Class for running the program class and testing'''

    def __init__(self, filename, expected_output):
        '''initialize the test class'''

        self.filename = filename
        self.expected_output = expected_output

    def test_run(self):
        '''Test the program'''

        ps = ProcessSheet(self.filename)
        actual_output = ps.process_file()

        if (len(actual_output) == len(self.expected_output) and all(x in self.expected_output for x in actual_output)):
            return "Test case has passed"

        else:
            return "Test case has failed"




    


filename = "./files/python_skill_test.xlsx"
expected_output = {'Quote Number': 98765.0, 'Date': '2019-01-01', 'Ship To': 'USA', 'Name': 'Rapahel Epstein', 'Items': [{'LineNumber': 1.0, 'PartNumber': 'ABC', 'Description': 'Very Good', 'Price': 200.2}, {'LineNumber': 2.0, 'PartNumber': 'DEF', 'Description': 'Not so good', 'Price': 100.1}]}



ps = ProcessSheetTest(filename, expected_output)

print(ps.test_run()) #It will return Test case has passed if expected = actual and fail if not equal
