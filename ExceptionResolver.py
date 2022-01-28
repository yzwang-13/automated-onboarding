from typing import overload


import sys
class ExceptionResolver:
    def __init__(self):
        self.message = None
        self.sheetName = None
        self.columnName = None

    def raiseError(self, csvClient, message, sheetName, columnName):
        csvClient.createExceptionLocalExcel(message, sheetName, columnName)
        sys.exit(1)

        
