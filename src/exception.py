import sys

from src.logger import logging

def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    error_msg = f"Error occurred\nFile: {file_name}\nLine: {line_no}\nMessage: {str(error)}"
    return error_msg

class CustomException(Exception):
    def __init__(self, error_msg, error_detail):
        super().__init__(error_msg)
        self.error_msg = error_message_detail(error_msg, error_detail)

    def __str__(self):
        return self.error_msg
    
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Invalid operations")
        raise CustomException(e,sys)

        
