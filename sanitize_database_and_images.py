import os
import shutil
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
DATA_FILE = os.path.join(SCRIPT_DIR, "images_data.json")

# Master clean mapping by category
AUTHENTIC_MAP = {
    'shiva': [
        'images/lord_shiva_1789315505870.jpg',
        'images/lord_shiva_kailash_peace.jpg',
        'images/shiv_parvati_family.jpg',
        'images/cute_bal_shiva.jpg'
    ],
    'ram': [
        'images/shri_ram_darbar.jpg',
        'images/lord_ram_1789315920936.jpg'
    ],
    'hanuman': [
        'images/lord_hanuman_meditation.jpg',
        'images/lord_hanuman_1789315589634.jpg',
        'images/cute_bal_hanuman.jpg'
    ],
    'krishna': [
        'images/lord_krishna_1789315536423.jpg',
        'images/krishna_govardhan.jpg',
        'images/cute_radha_krishna.jpg',
        'images/cute_bal_gopal_1789315873602.jpg',
        'images/cute_krishna_makhan.jpg'
    ],
    'ganesha': [
        'images/lord_ganesha_1789315549643.jpg',
        'images/cute_bal_ganesha_1789316002528.jpg',
        'images/cute_ganesha_reading.jpg'
    ],
    'durga': [
        'images/goddess_durga_1789315573017.jpg',
        'images/navratri_durga_special.jpg',
        'images/navratri_nine_devi.jpg'
    ],
    'lakshmi': [
        'images/goddess_lakshmi_1789315900662.jpg',
        'images/cute_baby_lakshmi.jpg'
    ],
    'saraswati': [
        'images/goddess_saraswati_1789315983989.jpg',
        'images/cute_baby_saraswati.jpg'
    ],
    'vishnu': [
        'images/lord_vishnu_narayan.jpg'
    ],
    'cute': [
        'images/cute_radha_krishna.jpg',
        'images/cute_bal_gopal_1789315873602.jpg',
        'images/cute_bal_ganesha_1789316002528.jpg',
        'images/cute_bal_shiva.jpg',
        'images/cute_bal_hanuman.jpg',
        'images/cute_baby_lakshmi.jpg',
        'images/cute_baby_saraswati.jpg',
        'images/cute_krishna_makhan.jpg',
        'images/cute_ganesha_reading.jpg'
    ]
}

def sanitize_images_data():
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    counters = {k: 0 for k in AUTHENTIC_MAP}

    total_remapped = 0
    for date_key, items in data.items():
        for item in items:
            cat_raw = (item.get("category") or "").lower()
            # Determine canonical category
            matched_cat = "cute"
            for k in AUTHENTIC_MAP:
                if k in cat_raw:
                    matched_cat = k
                    break

            pool = AUTHENTIC_MAP[matched_cat]
            idx = counters[matched_cat] % len(pool)
            counters[matched_cat] += 1
            authentic_img = pool[idx]

            # Remap
            item["image"] = authentic_img
            if "image_url" in item:
                item["image_url"] = authentic_img

            # Sanitize ai_prompt or other metadata to ensure no alien/pollinations mentions
            if "ai_prompt" in item:
                item["ai_prompt"] = item.get("name_hi", "") + " - पावन एवं अलौकिक 4K दर्शन"

            total_remapped += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully remapped {total_remapped} items in {DATA_FILE} to 100% sacred authentic master images!")

def purge_bad_folders():
    purged_count = 0
    for entry in os.listdir(IMAGES_DIR):
        full_path = os.path.join(IMAGES_DIR, entry)
        if os.path.isdir(full_path) and entry.startswith("2026-"):
            shutil.rmtree(full_path, ignore_errors=True)
            purged_count += 1
            print(f"Purged directory: {entry}")
    print(f"Total purged dated subdirectories: {purged_count}")

if __name__ == "__main__":
    sanitize_images_data()
    purge_bad_folders()
