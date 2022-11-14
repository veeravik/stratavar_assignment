

#The program class

class BomDisti:
    '''Process bom and disti lists to return a unified list'''

    def __init__(self, bom_list, disti_list):

        '''initialize with bom and disti lists'''

        self.bom_list = bom_list
        self.disti_list = disti_list



    def find_in_disti(self, part_number):

        '''find a part number in dist list and return its quantity'''

        for i in self.disti_list:
            if i["PartNumber"] == part_number:
                return i["Quantity"]
        else:
            return False
  
  


    
    def modify_disti(self, part_number, quantity):

        '''Modify the disti list if its been consumed'''
    
        for i in self.disti_list:

            if i["PartNumber"] == part_number:
                i["Quantity"] -= quantity
            
      
        else:
            return False


    def get_unified_list(self):

        '''compare bom and disti lists to get an unified list'''


        unified_list = []
        for i in self.bom_list:

            d={"BomPN":i["PartNumber"],"BomQTY":i["Quantity"]}
            dist_quant = self.find_in_disti(i["PartNumber"])
            
            if dist_quant: 

                if i["Quantity"] == dist_quant:             
                    d["DistiPN"] = i["PartNumber"]
                    d["DistiQTY"] = dist_quant
                    d["ErrorFlag"] = ""
                    self.modify_disti(i["PartNumber"], dist_quant)

                elif i["Quantity"] > dist_quant:
                    d["DistiPN"] = i["PartNumber"]
                    d["DistiQTY"] = dist_quant
                    d["ErrorFlag"] = "X"
                    self.modify_disti(i["PartNumber"], dist_quant)
                
                else:
                    d["DistiPN"] = i["PartNumber"]
                    d["DistiQTY"] = i["Quantity"]
                    d["ErrorFlag"] = ""
                    self.modify_disti(i["PartNumber"], i["Quantity"])
            else:
                d["DistiPN"] = ""
                d["DistiQTY"] = ""
                d["ErrorFlag"] = "X"
                
                

            
                

            unified_list.append(d)

        for i in disti_list:
            d={"BomPN":"","BomQTY":""}
            if i["Quantity"] > 0:
                d["DistiPN"]=i["PartNumber"]
                d["Quantity"]=i["Quantity"]
                d["ErrorFlag"] = "X"
                unified_list.append(d)

        return unified_list



#The test class
class BomDistiTest:
    '''Class for running the program class and testing'''


    def __init__(self, bom_list, disti_list, unified_list):

        '''initialize with bom and disti lists'''

        self.bom_list = bom_list
        self.disti_list = disti_list
        self.unified_list = unified_list

    def run_test(self):
        '''Test the program'''


        actual_output = BomDisti(self.bom_list, self.disti_list).get_unified_list()
        expected_output = self.unified_list

        if (len(actual_output) == len(expected_output) and all(x in expected_output for x in actual_output)):
            return "Test case has passed"

        else:
            return "Test case has failed"


bom_list = [
  {"PartNumber":"ABC", "Quantity":2},
  {"PartNumber":"XYZ", "Quantity":1},
  {"PartNumber":"IJK", "Quantity":1},
  {"PartNumber":"ABC", "Quantity":1},
  {"PartNumber":"IJK", "Quantity":1},
  {"PartNumber":"XYZ", "Quantity":2},
  {"PartNumber":"DEF", "Quantity":2}
]

disti_list = [
 
  {"PartNumber":"XYZ", "Quantity":2},
  {"PartNumber":"GEF", "Quantity":2},
  {"PartNumber":"ABC", "Quantity":4},
  {"PartNumber":"IJK", "Quantity":2},
  
]

unified_list = [{'BomPN': 'ABC', 'BomQTY': 2, 'DistiPN': 'ABC', 'DistiQTY': 2, 'ErrorFlag': ''}, {'BomPN': 'XYZ', 'BomQTY': 1, 'DistiPN': 'XYZ', 'DistiQTY': 1, 'ErrorFlag': ''}, {'BomPN': 'IJK', 'BomQTY': 1, 'DistiPN': 'IJK', 'DistiQTY': 1, 'ErrorFlag': ''}, {'BomPN': 'ABC', 'BomQTY': 1, 'DistiPN': 'ABC', 'DistiQTY': 1, 'ErrorFlag': ''}, {'BomPN': 'IJK', 'BomQTY': 1, 'DistiPN': 'IJK', 'DistiQTY': 1, 'ErrorFlag': ''}, {'BomPN': 'XYZ', 'BomQTY': 2, 'DistiPN': 'XYZ', 'DistiQTY': 1, 'ErrorFlag': 'X'}, {'BomPN': 'DEF', 'BomQTY': 2, 'DistiPN': '', 'DistiQTY': '', 'ErrorFlag': 'X'}, {'BomPN': '', 'BomQTY': '', 'DistiPN': 'GEF', 'Quantity': 2, 'ErrorFlag': 'X'}, {'BomPN': '', 'BomQTY': '', 'DistiPN': 'ABC', 'Quantity': 1, 'ErrorFlag': 'X'}]
    
bd = BomDistiTest(bom_list, disti_list, unified_list)
print(bd.run_test()) #It will return Test case has passed if expected = actual and fail if not equal
