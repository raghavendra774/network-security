import sys
from networksecurity.logging import logger 

class NetworkSecurityException(Exception):
    
    def __init__ (self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, exec_tb = error_details.exc_info()

        self.lineno = exec_tb.tb_lineno
        self.filename = exec_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python sctipt file [{self.filename}] line number [{self.lineno}] error message [{self.error_message}]"
    
