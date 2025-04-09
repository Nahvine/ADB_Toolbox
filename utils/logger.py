#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module ghi log cho ứng dụng ADB Toolbox
"""

import os
import logging
from datetime import datetime

def setup_logger():
    """
    Thiết lập logger cho ứng dụng
    
    Returns:
        logging.Logger: Logger đã được cấu hình
    """
    # Tạo thư mục logs nếu chưa có
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    log_file = os.path.join(logs_dir, "adb_toolbox.log")
    
    # Cấu hình logger
    logger = logging.getLogger("adb_toolbox")
    logger.setLevel(logging.INFO)
    
    # Tạo file handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Tạo formatter
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    
    # Thêm handler vào logger
    logger.addHandler(file_handler)
    
    return logger

def log_command(command, result=None):
    """
    Ghi log lệnh ADB đã chạy
    
    Args:
        command (str): Lệnh ADB đã chạy
        result (str): Kết quả của lệnh (nếu có)
    """
    logger = setup_logger()
    
    log_message = f"Đã chạy lệnh: {command}"
    if result:
        log_message += f" - Kết quả: {result}"
        
    logger.info(log_message)
    
def log_error(error_message):
    """
    Ghi log lỗi
    
    Args:
        error_message (str): Thông báo lỗi
    """
    logger = setup_logger()
    logger.error(error_message)
    
def get_logs(limit=20):
    """
    Lấy lịch sử log gần đây
    
    Args:
        limit (int): Số lượng dòng log muốn lấy
        
    Returns:
        list: Danh sách các dòng log
    """
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    log_file = os.path.join(logs_dir, "adb_toolbox.log")
    
    if not os.path.exists(log_file):
        return []
        
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    return lines[-limit:] if len(lines) > limit else lines 