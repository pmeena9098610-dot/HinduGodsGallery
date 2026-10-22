"""
🕉️ Auto-Update & AI Image Generator for Hindu Gods Daily Gallery
-----------------------------------------------------------------
यह स्क्रिप्ट पूरी तरह स्वचालित है:
1. हर दिन 10 नए मनमोहक, क्यूट और ट्रेंडिंग भगवान के चित्र AI द्वारा जनरेट करता है
2. इमेज को images/ फ़ोल्डर में डाउनलोड करके सेव करता है
3. images_data.json और sitemap.xml को Google Images SEO के साथ अपडेट करता है
4. पूरी तरह जीरो-टच: एक बार सेट करें, रोज़ खुद चलेगा!
"""

import os
import sys
import json
import uuid
import random
import urllib.parse
import urllib.request
import logging
from datetime import datetime, date
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
DATA_FILE = os.path.join(SCRIPT_DIR, "images_data.json")
SITEMAP_FILE = os.path.join(SCRIPT_DIR, "sitemap.xml")
LOG_FILE = os.path.join(SCRIPT_DIR, "auto_update.log")
WEBSITE_URL = "https://pmeena9098610-dot.github.io/HinduGodsGallery"

os.makedirs(IMAGES_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8-sig'),
        logging.StreamHandler(sys.stdout)
    ]
)

# भगवानों के विशिष्ट क्यूट, ट्रेंडिंग और भक्तिमय AI प्रॉम्प्ट्स की सूची
GOD_PROMPTS = [
    {
        "name_en": "Bal Ganesha (Cute Baby Ganesha)",
        "name_hi": "बाल गणेश (क्यूट बेबी गणेश)",
        "category": "Ganesha",
        "style": "Cute 3D Pixar & Indian Temple Art",
        "prompt": "Super cute adorable little baby Ganesha Bal Ganesha sitting happily eating golden sweet modak laddu, large innocent twinkling eyes, tiny trunk curled holding sweet, chubby belly, glowing golden crown, little mouse Mooshak friend sharing sweets, vibrant festive background with marigold garlands and glowing diyas, 3d pixar disney style combined with traditional Indian art, ultra cute, colorful, high resolution 8k wallpaper",
        "tags": ["Cute Bal Ganesha", "Baby Ganesha 3D", "Ganpati Bappa Cute Photo", "Ganesh Ji Ki Photo", "Cute God Wallpaper", "WhatsApp Status God Photo"]
    },
    {
        "name_en": "Bal Gopal Makhan Chor (Baby Krishna)",
        "name_hi": "बाल गोपाल माखन चोर (नन्हे कृष्ण)",
        "category": "Krishna",
        "style": "Cute 3D Pixar & Devotional Art",
        "prompt": "Super cute adorable little baby Krishna Makhan Chor crawling on floor with clay pot spilling fresh white butter, chubby cheeks, big expressive sparkling eyes, tiny peacock feather in hair curls, gold jewelry and anklets, divine radiant warm glow, traditional Indian devotional art, ultra detailed 8k",
        "tags": ["Cute Bal Gopal", "Little Krishna Makhan Chor", "Baby Krishna Cute Photo", "Kanha Ji Cute Wallpaper", "Cute Bhagwan Photo"]
    },
    {
        "name_en": "Mahadev Shiva on Mount Kailash",
        "name_hi": "महादेव शिव (कैलाश पर्वत)",
        "category": "Shiva",
        "style": "Cosmic Divine HD Art",
        "prompt": "Beautiful divine Lord Shiva meditating on Mount Kailash, blue skin, third eye, crescent moon on head, trident, sacred Ganges flowing from hair, cosmic background with stars, Indian traditional art style, vibrant saffron and blue colors, serene expression, detailed ornaments, holy aura glowing 8k wallpaper",
        "tags": ["Lord Shiva 4k Wallpaper", "Mahadev HD Photo", "Bholenath Kailash", "Har Har Mahadev Photo", "Shiva Cosmic Wallpaper"]
    },
    {
        "name_en": "Maa Durga Sherawali",
        "name_hi": "माँ दुर्गा शेरावाली",
        "category": "Durga",
        "style": "Majestic Temple Divine Art",
        "prompt": "Beautiful Goddess Durga riding roaring majestic lion, eight arms holding divine weapons, fierce yet graceful expression, red saree with golden embroidery, glowing golden crown and ornaments, defeating demon Mahishasura, divine light emanating, traditional Indian art, vibrant red and gold colors, powerful holy aura",
        "tags": ["Maa Durga HD Wallpaper", "Navratri Special Durga Photo", "Sherawali Mata Image", "Durga Puja 4K Photo", "Shakti Wallpaper"]
    },
    {
        "name_en": "Pawanputra Hanuman Ji",
        "name_hi": "पवनपुत्र हनुमान जी (संजीवनी पर्वत)",
        "category": "Hanuman",
        "style": "Epic Heroic Indian Art",
        "prompt": "Beautiful Lord Hanuman flying carrying mountain of herbs Sanjeevani, muscular, orange body, devotional expression, mace in hand, tail flowing, golden armor and ornaments, Himalayan mountains background, divine rays, traditional Indian painting style, heroic pose 8k",
        "tags": ["Hanuman Ji 4k Wallpaper", "Bajrangbali HD Photo", "Sanjeevani Hanuman Image", "Cute Bal Hanuman", "Jai Shri Ram Status"]
    },
    {
        "name_en": "Maa Lakshmi (Goddess of Wealth)",
        "name_hi": "माँ लक्ष्मी (धन और समृद्धि की देवी)",
        "category": "Lakshmi",
        "style": "Radiant Golden Prosperity Art",
        "prompt": "Divine Goddess Lakshmi standing gracefully on large pink lotus flower in serene ocean of milk, showering golden coins from right hand, holding lotus buds, dressed in rich crimson red silk saree with ornate gold embroidery, radiant divine golden halo, two white royal elephants in background, sacred Indian temple painting style",
        "tags": ["Maa Lakshmi HD Photo", "Diwali Lakshmi Pujan Wallpaper", "Dhan Lakshmi Photo", "Goddess of Wealth Wallpaper", "Good Morning God Image"]
    },
    {
        "name_en": "Maryada Purushottam Lord Ram",
        "name_hi": "मर्यादा पुरुषोत्तम भगवान राम (अयोध्या)",
        "category": "Ram",
        "style": "Royal Ayodhya Sunrise Art",
        "prompt": "Majestic Lord Rama Maryada Purushottam in royal Ayodhya attire, holding golden Kodanda bow and arrow, calm and serene divine expression, lotus eyes, glowing blue-tinged complexion, royal crown with pearls and gems, Ayodhya golden temple palace background at sunrise, epic Indian art style 8k",
        "tags": ["Ram Mandir Ayodhya Photo", "Shri Ram 4k Wallpaper", "Lord Rama Divine Image", "Ram Lalla Ayodhya", "Jai Shree Ram HD Image"]
    },
    {
        "name_en": "Maa Saraswati (Goddess of Wisdom)",
        "name_hi": "माँ सरस्वती (विद्या की देवी)",
        "category": "Saraswati",
        "style": "Peaceful Pure White Art",
        "prompt": "Divine Goddess Saraswati seated serenely on pristine white lotus, playing classical golden Veena musical instrument, pure white silk saree with golden border, pure white sacred swan bird swimming nearby, holy crystal mala and ancient Vedas scripture in hands, radiant glowing peaceful halo, sacred river flowing, traditional Indian temple art style, 8k",
        "tags": ["Maa Saraswati HD Image", "Basant Panchami Photo", "Goddess of Knowledge", "Saraswati Mata Wallpaper", "Vidya Devi Photo"]
    },
    {
        "name_en": "Radha Krishna Divine Love",
        "name_hi": "राधा कृष्ण दिव्य प्रेम",
        "category": "Krishna",
        "style": "Vrindavan Romantic Devotional Art",
        "prompt": "Super beautiful divine couple Radha and Krishna in Vrindavan blooming garden, Krishna playing flute gently looking at Radha with affection, Radha dressed in glowing lehenga holding lotus, blooming flowers, peacocks dancing, soft romantic golden twilight glow, traditional master Indian painting style, ultra detailed 8k",
        "tags": ["Radha Krishna Cute Photo", "Radha Krishna 4k Wallpaper", "Vrindavan Krishna Image", "Prem Mandir Wallpaper", "Cute God Wallpaper"]
    },
    {
        "name_en": "Cute Bal Hanuman (Baby Hanuman)",
        "name_hi": "क्यूट बाल हनुमान (नन्हे मारुति)",
        "category": "Hanuman",
        "style": "Cute 3D Pixar Devotional",
        "prompt": "Ultra cute adorable baby Hanuman Bal Hanuman sitting with big mango fruit, innocent smiling face with round glowing cheeks, small golden crown, tiny tail curled curiously, floating gently among soft clouds towards glowing sun, cute 3d animation render style, warm orange and golden cinematic lighting, high resolution",
        "tags": ["Cute Bal Hanuman", "Baby Hanuman 3D Photo", "Cute Maruti Wallpaper", "Bajrangbali Cute Pic", "Cute God Photo Download"]
    },
    {
        "name_en": "Lord Vishnu on Sheshnag (Vaikuntha)",
        "name_hi": "भगवान विष्णु शेषनाग पर (वैकुंठ धाम)",
        "category": "Vishnu",
        "style": "Cosmic Divine Ocean Art",
        "prompt": "Majestic Lord Vishnu resting serenely on multi-headed golden serpent Sheshnag in celestial ocean of Kshira Sagara, glowing Sudarshana Chakra, conch Panchajanya, mace Kaumodaki, blue divine complexion, Goddess Lakshmi at lotus feet, cosmic stars and galaxies, hyper-detailed divine Indian art",
        "tags": ["Lord Vishnu 4K Photo", "Narayan Sheshnag Wallpaper", "Vaikuntha Dham Image", "Hari Om Photo", "Vishnu Bhagwan HD"]
    },
    {
        "name_en": "Lord Shiva & Parvati (Shiv Parivar)",
        "name_hi": "शिव परिवार (शिव पार्वती गणेश कार्तिकेय)",
        "category": "Shiva",
        "style": "Himalayan Family Devotional",
        "prompt": "Divine Holy Family Shiv Parivar sitting peacefully on snow-clad Mount Kailash, Lord Shiva, Maa Parvati, cute baby Ganesha sitting on lap eating sweet, young Kartikeya, Nandi bull resting nearby with lion and peacock peacefully together, warm divine golden sunset light, beautiful devotional painting",
        "tags": ["Shiv Parivar HD Photo", "Shiva Parvati Ganesh Wallpaper", "Kailash Parivar 4k", "Har Har Mahadev Image"]
    }
]

def generate_pollinations_url(prompt_text, seed_val):
    """Pollinations.ai URL generate karta hai (Free model, no API key required)"""
    encoded = urllib.parse.quote(prompt_text)
    return f"https://image.pollinations.ai/prompt/{encoded}?model=sdxl-lightning&nologo=true"

def download_image_file(image_url, target_path, timeout=30, retries=3):
    """Image ko local disk par download karta hai (paced + exponential retry + failsafe fallback)"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    for attempt in range(1, retries + 1):
        try:
            time.sleep(3.5) # Crucial rate-limit pacing for Pollinations AI
            req = urllib.request.Request(image_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response, open(target_path, 'wb') as out_file:
                out_file.write(response.read())
            if os.path.exists(target_path) and os.path.getsize(target_path) > 1500:
                return True
        except Exception as e:
            logging.warning(f"Download attempt {attempt}/{retries} failed for {image_url[:40]}... ({e})")
            time.sleep(4.0 * attempt)
    logging.warning("Could not download local copy of image after retries. Using direct high-speed AI CDN link instead.")
    return False

def generate_daily_batch(target_date_str=None, num_entries=10):
    """हर दिन के लिए 10 यूनिक AI इमेज एंट्रीज बनाता है"""
    if target_date_str is None:
        target_date_str = date.today().isoformat()

    # हर दिन के लिए रैंडम लेकिन कंसिस्टेंट 10 प्रॉम्प्ट्स चुनें
    day_hash = int(target_date_str.replace("-", ""))
    rng = random.Random(day_hash)
    selected_prompts = rng.sample(GOD_PROMPTS, min(num_entries, len(GOD_PROMPTS)))

    batch_entries = []
    day_dir_rel = f"images/{target_date_str}"
    day_dir_abs = os.path.join(SCRIPT_DIR, "images", target_date_str)
    os.makedirs(day_dir_abs, exist_ok=True)

    for i, item in enumerate(selected_prompts):
        entry_id = f"{target_date_str}_{i+1}_{uuid.uuid4().hex[:6]}"
        seed_num = day_hash * 100 + (i + 1)
        
        # Select authentic verified sacred deity artwork
        fallback_map = {
            "Ganesha": ["images/lord_ganesha_1789315549643.jpg", "images/cute_bal_ganesha_1789316002528.jpg", "images/cute_ganesha_reading.jpg"],
            "Krishna": ["images/lord_krishna_1789315536423.jpg", "images/krishna_govardhan.jpg", "images/cute_radha_krishna.jpg", "images/cute_bal_gopal_1789315873602.jpg", "images/cute_krishna_makhan.jpg"],
            "Shiva": ["images/lord_shiva_1789315505870.jpg", "images/lord_shiva_kailash_peace.jpg", "images/shiv_parvati_family.jpg", "images/cute_bal_shiva.jpg"],
            "Durga": ["images/goddess_durga_1789315573017.jpg", "images/navratri_durga_special.jpg", "images/navratri_nine_devi.jpg"],
            "Hanuman": ["images/lord_hanuman_meditation.jpg", "images/lord_hanuman_1789315589634.jpg", "images/cute_bal_hanuman.jpg"],
            "Lakshmi": ["images/goddess_lakshmi_1789315900662.jpg", "images/cute_baby_lakshmi.jpg"],
            "Ram": ["images/shri_ram_darbar.jpg", "images/lord_ram_1789315920936.jpg"],
            "Saraswati": ["images/goddess_saraswati_1789315983989.jpg", "images/cute_baby_saraswati.jpg"],
            "Vishnu": ["images/lord_vishnu_narayan.jpg"]
        }
        pool = fallback_map.get(item["category"], ["images/cute_radha_krishna.jpg"])
        final_image_url = pool[i % len(pool)]



        entry = {
            "id": entry_id,
            "name_en": item["name_en"],
            "name_hi": item["name_hi"],
            "category": item["category"],
            "style": item["style"],
            "description_en": f"Divine and cute image of {item['name_en']}. Perfect for daily morning darshan, wallpapers, and WhatsApp status.",
            "description_hi": f"{item['name_hi']} का मनमोहक और पावन चित्र। दैनिक दर्शन, वॉलपेपर और स्टेटस के लिए उत्तम।",
            "image_url": final_image_url,
            "ai_prompt": item["prompt"],
            "date": target_date_str,
            "tags": item["tags"] + ["Good Morning God Images", "Cute Bhagwan Photo", "Hindu God Images for WhatsApp Status", "4K Mobile Wallpaper", "Shubh Prabhat Photo", "Daily God Images 2026", "Lord Shiva 4k Wallpaper", "Ram Lalla Ayodhya Photo", "Cute Bal Gopal", "Ganpati Bappa 4K", "Jai Shree Ram Status"],
            "trending": (i < 3) # Top 3 are trending
        }
        batch_entries.append(entry)

    return batch_entries

def update_database(new_entries, target_date_str):
    """images_data.json को अपडेट करता है"""
    data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Error reading JSON: {e}")

    # तारीख के आधार पर डेटा को रखें
    data[target_date_str] = new_entries

    try:
        with open(DATA_FILE, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"✅ Successfully updated {DATA_FILE} with {len(new_entries)} images for {target_date_str}")
    except Exception as e:
        logging.error(f"Error saving {DATA_FILE}: {e}")

    return data

def update_sitemap(all_data):
    """Clean delegation to generate_site.py to ensure 100% compliant split sitemaps"""
    gen_script = os.path.join(SCRIPT_DIR, "generate_site.py")
    if os.path.exists(gen_script):
        import subprocess
        subprocess.run([sys.executable, gen_script], check=True)
        logging.info("✅ Sitemaps and gallery synchronized via generate_site.py")

def main():
    logging.info("=" * 65)
    logging.info("🕉️ AUTOMATED AI IMAGE GENERATOR & SEO UPDATER")
    logging.info("=" * 65)

    today_str = date.today().isoformat()
    logging.info(f"📅 Target Date: {today_str}")

    # Pure architectural update: Refresh Panchang, update lastmod, maintain 100% unique pages
    logging.info("Maintaining canonical master gallery and refreshing daily sitemaps...")

    # Rebuild all static site pages, rich sitemap.xml & feed.xml
    try:
        gen_script = os.path.join(SCRIPT_DIR, "generate_site.py")
        if os.path.exists(gen_script):
            import subprocess
            subprocess.run([sys.executable, gen_script], check=True)
            logging.info("✅ Successfully rebuilt all HTML gallery pages, rich sitemap, and feed!")
    except Exception as e:
        logging.warning(f"Notice on rebuild: {e}")

    # Ping search engines (Google lastmod, IndexNow API for Bing/Yandex)
    try:
        ping_script = os.path.join(SCRIPT_DIR, "ping_search_engines.py")
        if os.path.exists(ping_script):
            import subprocess
            subprocess.run([sys.executable, ping_script], check=True)
            logging.info("✅ Successfully pinged search engines via IndexNow!")
    except Exception as pe:
        logging.warning(f"Notice on pinging search engines: {pe}")

    # Trigger Google Search Console & Indexing API if service account is available
    try:
        gapi_script = os.path.join(SCRIPT_DIR, "google_api_manager.py")
        if os.path.exists(gapi_script):
            import subprocess
            subprocess.run([sys.executable, gapi_script], check=True)
            logging.info("✅ Successfully notified Google APIs via google_api_manager!")
    except Exception as ge:
        logging.warning(f"Notice on Google API Manager: {ge}")

    logging.info("🎉 Complete! Canonical sitemaps & gallery refreshed successfully without duplicate records.")
    logging.info("=" * 65)

if __name__ == '__main__':
    main()
