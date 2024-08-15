import os
from datetime import datetime

def get_timestamped_file_path(base_dir, filename):
    """Tạo đường dẫn file mới với tên file chứa timestamp."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(base_dir, new_filename)
    return file_path.replace("\\", "/")

def get_new_exp_dir(base_dir):
    """Tìm thư mục exp mới với tên tăng dần."""
    exp_dirs = [d for d in os.listdir(base_dir) if d.startswith('exp')]
    exp_numbers = [int(d[3:]) for d in exp_dirs if d[3:].isdigit()]
    next_exp_number = max(exp_numbers) + 1 if exp_numbers else 1
    new_exp_dir = os.path.join(base_dir, f'exp{next_exp_number}')
    os.makedirs(new_exp_dir, exist_ok=True)
    return new_exp_dir