import os
import requests
from tqdm import tqdm

# Base URL for CHB-MIT dataset on PhysioNet
BASE_URL = "https://physionet.org/files/chbmit/1.0.0/"

# List of all 23 patients
PATIENTS = [f"chb{i:02d}" for i in range(1, 24)]

# Save path (current folder)
SAVE_DIR = os.getcwd()

# Approximate number of files per patient (CHB-MIT has 23-24 files per patient)
FILES_PER_PATIENT = {
    "chb01": 24, "chb02": 24, "chb03": 24, "chb04": 24,
    "chb05": 24, "chb06": 24, "chb07": 24, "chb08": 24,
    "chb09": 24, "chb10": 24, "chb11": 24, "chb12": 24,
    "chb13": 24, "chb14": 24, "chb15": 24, "chb16": 24,
    "chb17": 24, "chb18": 24, "chb19": 24, "chb20": 24,
    "chb21": 24, "chb22": 24, "chb23": 24,
}

def download_file(url, save_path):
    """Download file in small chunks to avoid memory issues"""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(save_path, 'wb') as f, tqdm(
            total=total, unit='B', unit_scale=True, desc=os.path.basename(save_path)
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

for patient in PATIENTS:
    patient_dir = os.path.join(SAVE_DIR, patient)
    os.makedirs(patient_dir, exist_ok=True)
    
    num_files = FILES_PER_PATIENT[patient]
    for i in range(1, num_files + 1):
        edf_file = f"{patient}_{i:02d}.edf"
        url = f"{BASE_URL}{patient}/{edf_file}?download"
        save_path = os.path.join(patient_dir, edf_file)
        if os.path.exists(save_path):
            print(f"{edf_file} already exists, skipping...")
            continue
        print(f"Downloading {edf_file}...")
        try:
            download_file(url, save_path)
        except Exception as e:
            print(f"Error downloading {edf_file}: {e}")
            continue

print("All CHB-MIT EDF files downloaded successfully!")
