"""
TASK 1.3: CUAD Legal Dataset Acquisition
Downloads CUAD_v1.zip from Zenodo, extracts CUAD_v1.json in-memory,
and saves 8 unique contract texts to /data/contracts/.
"""
import os
import json
import zipfile
import io
import urllib.request

TARGET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/contracts"))
CUAD_ZIP_URL = "https://zenodo.org/records/4595826/files/CUAD_v1.zip?download=1"
NUM_CONTRACTS = 8


def download_zip(url: str) -> bytes:
    import subprocess
    print(f"Downloading CUAD_v1.zip from Zenodo (~106 MB, please wait)...")
    zip_path = "CUAD_v1.zip"
    subprocess.run(["curl.exe", "-L", "-o", zip_path, url], check=True)
    with open(zip_path, "rb") as f:
        data = f.read()
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print(f"  Downloaded {len(data) / 1_000_000:.1f} MB")
    return data


def extract_contracts(zip_bytes: bytes) -> dict[str, str]:
    unique: dict[str, str] = {}
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        json_names = [n for n in zf.namelist() if n.endswith("CUAD_v1.json")]
        if not json_names:
            raise FileNotFoundError("CUAD_v1.json not found in zip archive.")
        print(f"  Found JSON: {json_names[0]}")
        with zf.open(json_names[0]) as f:
            data = json.load(f)
    for entry in data.get("data", []):
        title = entry.get("title", "unknown")
        safe = "".join(c if c.isalnum() or c in " _-" else "" for c in title).strip().replace(" ", "_")
        if not safe:
            safe = f"contract_{len(unique)}"
        paragraphs = entry.get("paragraphs", [])
        full_text = "\n\n".join(p.get("context", "") for p in paragraphs if p.get("context"))
        if safe not in unique and full_text:
            unique[safe] = full_text
    return unique


def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    try:
        zip_bytes = download_zip(CUAD_ZIP_URL)
    except Exception as e:
        print(f"Error downloading CUAD zip: {e}")
        return

    try:
        contracts = extract_contracts(zip_bytes)
    except Exception as e:
        print(f"Error extracting contracts: {e}")
        return

    print(f"Found {len(contracts)} unique contracts.")
    count = 0
    for title, text in contracts.items():
        if count >= NUM_CONTRACTS:
            break
        path = os.path.join(TARGET_DIR, f"{title}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  Saved: {title}.txt  ({len(text)//1024} KB)")
        count += 1
    print(f"\nDone. {count} contracts saved to: {TARGET_DIR}")


if __name__ == "__main__":
    main()
