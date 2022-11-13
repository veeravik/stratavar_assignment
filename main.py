import datetime,xlrd
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







filename = "./python_skill_test.xlsx"
ps = ProcessSheet(filename)
print(ps.process_file())


            



