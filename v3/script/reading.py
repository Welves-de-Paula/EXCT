import os
import shutil

def store(filepath,subdir):
    # Copia o arquivo para o diretório data/subdir
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    if subdir:
        data_dir = os.path.join(data_dir, subdir)
    os.makedirs(data_dir, exist_ok=True)
    dest_path = os.path.join(data_dir, os.path.basename(filepath))
    shutil.copy2(filepath, dest_path)
      