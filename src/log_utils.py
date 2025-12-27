import os
from datetime import datetime


class Logger:
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志配置"""
        home = os.path.expanduser("~")
        log_dir = os.path.join(home, ".dict", "log")
        os.makedirs(log_dir, exist_ok=True)

        self.info_log = os.path.join(log_dir, "info.log")
        self.error_log = os.path.join(log_dir, "error.log")
    
    def log_info(self, message):
        """记录INFO日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}\n"
        
        with open(self.info_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def log_error(self, message):
        """记录ERROR日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}\n"
        
        with open(self.error_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)