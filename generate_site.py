import os, sys, json
from datetime import datetime, date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from generator_data import ITEMS as BASE_ITEMS, CATEGORIES, BASE_URL

DIRS = [SCRIPT_DIR]
for extra in [r"C:\Users\Bappa official\OneDrive\Desktop\HinduGodsGallery", r"C:\Users\Bappa official\HinduGodsGallery", r"c:\Users\Bappa official\.gemini\antigravity\playground\primordial-chromosphere"]:
    if os.path.exists(extra) and extra not in DIRS:
        DIRS.append(extra)

def load_fused_items():
    """Fuses curated items with any newly generated items from images_data.json"""
    import copy
    all_items = copy.deepcopy(BASE_ITEMS)
    existing_ids = {it["id"] for it in all_items}

    json_path = os.path.join(SCRIPT_DIR, "images_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8-sig") as fp:
                data = json.load(fp)
            
            entries = []
            if isinstance(data, dict):
                for d_key, d_list in data.items():
                    if isinstance(d_list, list):
                        entries.extend(d_list)
            elif isinstance(data, list):
                entries.extend(data)

            for entry in entries:
                eid = entry.get("id")
                if eid and eid not in existing_ids:
                    img_raw = entry.get("image") or entry.get("image_url", "")
                    if img_raw.endswith(".jpg") or img_raw.endswith(".webp"):
                        img_base = os.path.splitext(img_raw)[0]
                    else:
                        img_base = img_raw

                    title = entry.get("title") or entry.get("name_en", "Daily Hindu God 4K Wallpaper")
                    titleHi = entry.get("titleHi") or entry.get("name_hi", "दैनिक हिन्दू भगवान 4K फोटो")
                    cat = (entry.get("category") or "cute").split(",")[0].lower()
                    
                    new_item = {
                        "id": eid,
                        "slug": f"photo-{eid}.html",
                        "title": title,
                        "titleHi": titleHi,
                        "category": cat,
                        "categoryName": cat.capitalize() + " Gallery",
                        "categorySlug": f"category-{cat}.html",
                        "god": cat,
                        "img": img_base,
                        "badge": "Daily Divine 4K",
                        "shortDesc": entry.get("description_hi") or f"{titleHi} का मनमोहक और पावन 4K स्वरूप। दैनिक दर्शन एवं वॉलपेपर।",
                        "mantra": "ॐ नमो भगवते वासुदेवाय नमः ।\nसर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः ॥",
                        "mantraMeaning": "सभी सुखी हों, सभी निरोगी रहें, सभी का कल्याण हो।",
                        "article": f"{titleHi} के पावन दर्शन मात्र से जीवन में सुख, शांति और सकारात्मक ऊर्जा का संचार होता है। इस 4K वॉलपेपर को अपने मोबाइल स्क्रीन पर लगाएं या व्हाट्सएप स्टेटस पर शेयर करें।",
                        "tags": entry.get("tags") or [title.lower(), "hindu god 4k", "whatsapp status god photo"]
                    }
                    all_items.append(new_item)
                    existing_ids.add(eid)
        except Exception as e:
            print(f"Notice during images_data.json merge: {e}")

    return all_items

ITEMS = load_fused_items()
print(f"Loaded {len(ITEMS)} total deity items (fused data pipeline active).")

COMMON_HEAD = """
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="apple-touch-icon" href="favicon.png">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#780016">
    <meta name="google-site-verification" content="VN51R5hg-j81ctWmVxSAeWN3DiGhaUM8K-OzI_uXFCY" />
    <meta name="google-site-verification" content="AecstdStcn1JHOXM253jV6q4g3rar75-4VXU9b7Fyjw" />
    <link rel="alternate" type="application/rss+xml" title="Hindu Gods Daily Gallery RSS" href="feed.xml">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Kalam:wght@700&family=Poppins:wght@300;400;500;600;700&family=Rozha+One&display=swap" rel="stylesheet">
"""

COMMON_STYLE = """
<style>
    :root {
        --saffron: #FF7700;
        --saffron-light: #FF9933;
        --maroon: #780016;
        --maroon-dark: #4A000E;
        --gold: #FFD700;
        --gold-light: #FFF099;
        --cream: #FFFDF7;
        --text-dark: #2B1810;
        --card-shadow: 0 12px 30px rgba(120, 0, 22, 0.12);
        --card-hover: 0 20px 40px rgba(255, 119, 0, 0.3);
        --whatsapp: #25D366;
        --pinterest: #E60023;
        --facebook: #1877F2;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(180deg, #FFF8F0 0%, var(--cream) 30%, #FFF0E0 100%);
        color: var(--text-dark);
        min-height: 100vh;
        line-height: 1.6;
    }
    /* HEADER */
    .site-header {
        background: linear-gradient(135deg, var(--maroon-dark) 0%, var(--maroon) 40%, var(--saffron) 100%);
        padding: 24px 16px 18px;
        text-align: center;
        color: var(--gold);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        position: relative;
    }
    .site-header h1 {
        font-family: 'Rozha One', serif;
        font-size: clamp(1.4rem, 4vw, 2.4rem);
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    .site-header h1 a { color: var(--gold); text-decoration: none; }
    .site-header p {
        font-family: 'Kalam', cursive;
        color: var(--gold-light);
        font-size: clamp(0.85rem, 2.5vw, 1.15rem);
        margin-top: 4px;
    }
    .header-audio-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 215, 0, 0.2);
        border: 1px solid var(--gold);
        color: var(--gold-light);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        margin-top: 10px;
        transition: all 0.3s;
    }
    .header-audio-btn:hover, .header-audio-btn.playing {
        background: var(--gold);
        color: var(--maroon-dark);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
        transform: scale(1.05);
    }

    /* NAV BAR */
    .top-nav {
        background: white;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        padding: 12px 10px;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-bottom: 2px solid var(--gold);
    }
    .nav-link {
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid var(--saffron);
        color: var(--maroon);
        text-decoration: none;
        font-weight: 600;
        font-size: 0.82rem;
        transition: all 0.25s;
        background: var(--cream);
    }
    .nav-link:hover, .nav-link.active {
        background: linear-gradient(135deg, var(--saffron), var(--maroon));
        color: white;
        border-color: var(--maroon);
        transform: translateY(-2px);
    }
    /* CONTAINER */
    .container {
        max-width: 1280px;
        margin: 0 auto;
        padding: 20px 16px;
    }
    /* BREADCRUMB */
    .breadcrumb {
        font-size: 0.85rem;
        color: #777;
        margin-bottom: 16px;
    }
    .breadcrumb a { color: var(--maroon); text-decoration: none; font-weight: 500; }
    .breadcrumb a:hover { text-decoration: underline; color: var(--saffron); }

    /* CARD GRID */
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 22px;
        margin-top: 18px;
    }
    .card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: var(--card-shadow);
        transition: all 0.35s;
        position: relative;
        display: flex;
        flex-direction: column;
    }
    .card:hover {
        transform: translateY(-6px);
        box-shadow: var(--card-hover);
    }
    .card-img-link {
        display: block;
        position: relative;
        aspect-ratio: 3/4;
        overflow: hidden;
        background: #f5ede4;
    }
    .card-img-link img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s;
    }
    .card:hover .card-img-link img { transform: scale(1.06); }
    .badge {
        position: absolute;
        top: 10px;
        left: 10px;
        background: linear-gradient(135deg, var(--saffron), var(--maroon));
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        z-index: 2;
    }
    .card-body {
        padding: 14px;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .card-body h3 {
        font-family: 'Kalam', cursive;
        font-size: 1.05rem;
        color: var(--maroon);
        margin-bottom: 6px;
    }
    .card-body h3 a { color: var(--maroon); text-decoration: none; }
    .card-body h3 a:hover { color: var(--saffron); }
    .card-body p {
        font-size: 0.8rem;
        color: #666;
        line-height: 1.4;
        margin-bottom: 10px;
        flex-grow: 1;
    }
    .card-actions {
        display: flex;
        gap: 8px;
        margin-top: auto;
    }
    .btn-action {
        flex: 1;
        padding: 8px 10px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        font-size: 0.78rem;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        transition: all 0.2s;
        color: white;
    }
    .btn-view { background: linear-gradient(135deg, var(--saffron), var(--maroon)); }
    .btn-wa { background: var(--whatsapp); }
    .btn-dl { background: #333; }
    .btn-action:hover { opacity: 0.9; transform: scale(1.03); }
    
    /* DETAIL PAGE LAYOUT */
    .detail-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
        background: white;
        border-radius: 20px;
        padding: 28px;
        box-shadow: var(--card-shadow);
        margin-bottom: 30px;
    }
    .detail-img-wrap {
        border-radius: 16px;
        overflow: hidden;
        position: relative;
        background: #fdf5ec;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    .detail-img-wrap img {
        width: 100%;
        height: auto;
        display: block;
    }
    .detail-info h1 {
        font-family: 'Rozha One', serif;
        font-size: clamp(1.5rem, 3.5vw, 2.2rem);
        color: var(--maroon);
        margin-bottom: 6px;
    }
    .detail-info h2 {
        font-family: 'Kalam', cursive;
        color: var(--saffron);
        font-size: 1.25rem;
        margin-bottom: 14px;
    }
    .mantra-box {
        background: linear-gradient(135deg, #FFF9E6, #FFF2CC);
        border: 2px dashed var(--saffron);
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        position: relative;
    }
    .mantra-heading {
        font-weight: 700;
        color: var(--maroon);
        font-size: 0.88rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .mantra-text {
        font-family: 'Rozha One', serif;
        color: var(--maroon-dark);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .mantra-meaning {
        font-size: 0.85rem;
        color: #555;
        margin-top: 8px;
        border-top: 1px dotted #e0c890;
        padding-top: 6px;
    }
    .btn-copy-mantra {
        background: var(--saffron);
        color: white;
        border: none;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        cursor: pointer;
        font-weight: 600;
    }
    .btn-copy-mantra:hover { background: var(--maroon); }
    .button-group {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 20px 0;
    }
    .btn-big {
        padding: 12px 20px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        text-decoration: none;
        color: white;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        border: none;
        transition: all 0.25s;
    }
    .btn-big:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.2); }
    .btn-big-wa { background: var(--whatsapp); }
    .btn-big-dl { background: linear-gradient(135deg, var(--maroon), var(--maroon-dark)); }
    .btn-big-pin { background: var(--pinterest); }
    .article-box {
        margin-top: 20px;
        line-height: 1.7;
        font-size: 0.92rem;
        color: #444;
        border-top: 1px solid #eee;
        padding-top: 16px;
    }
    .tag-cloud {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 12px;
    }
    .tag-item {
        background: #f0ebe4;
        color: #666;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        text-decoration: none;
    }
    .tag-item:hover { background: var(--saffron); color: white; }

    /* PANCHANG & MUHURAT WIDGET */
    .panchang-card {
        background: linear-gradient(135deg, #FFFDF8, #FFF5E6);
        border: 2px solid var(--gold);
        border-radius: 18px;
        padding: 20px 24px;
        margin: 24px auto;
        box-shadow: 0 8px 25px rgba(255,119,0,0.12);
        max-width: 1000px;
    }
    .panchang-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px dashed rgba(255,119,0,0.3);
        padding-bottom: 12px;
        margin-bottom: 14px;
        flex-wrap: wrap;
        gap: 10px;
    }
    .panchang-header h3 {
        font-family: 'Rozha One', serif;
        color: var(--maroon);
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .panchang-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 14px;
    }
    .panchang-item {
        background: white;
        padding: 12px 14px;
        border-radius: 12px;
        border-left: 4px solid var(--saffron);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .panchang-item span.label {
        font-size: 0.76rem;
        color: #777;
        display: block;
        font-weight: 600;
        text-transform: uppercase;
    }
    .panchang-item strong {
        font-size: 0.95rem;
        color: var(--maroon-dark);
        display: block;
        margin-top: 2px;
    }
    .suvichar-box {
        margin-top: 14px;
        background: #FFF9E6;
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 0.88rem;
        color: var(--maroon);
        border: 1px solid var(--gold);
        text-align: center;
    }

    /* DIGITAL 108 JAP MALA */
    .mala-card {
        background: linear-gradient(135deg, #4A000E, #780016);
        border: 2px solid var(--gold);
        border-radius: 20px;
        padding: 24px;
        color: var(--gold-light);
        margin: 28px auto;
        max-width: 900px;
        box-shadow: 0 10px 30px rgba(74, 0, 14, 0.35);
        text-align: center;
    }
    .mala-card h3 {
        font-family: 'Rozha One', serif;
        color: var(--gold);
        font-size: 1.4rem;
        margin-bottom: 6px;
    }
    .mala-mantra-select {
        background: rgba(255,255,255,0.15);
        border: 1px solid var(--gold);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.88rem;
        margin: 10px 0 16px;
        outline: none;
        cursor: pointer;
    }
    .mala-mantra-select option { background: #4A000E; color: white; }
    .mala-bead-btn {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #FFD700 0%, #FF7700 60%, #B71C1C 100%);
        border: 4px solid var(--gold-light);
        color: #4A000E;
        font-family: 'Rozha One', serif;
        font-size: 1.8rem;
        cursor: pointer;
        margin: 10px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(255,215,0,0.5);
        transition: transform 0.15s, box-shadow 0.15s;
        user-select: none;
    }
    .mala-bead-btn:active { transform: scale(0.92); box-shadow: 0 0 40px rgba(255,215,0,0.8); }
    .mala-progress-bar {
        width: 100%;
        height: 12px;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        overflow: hidden;
        margin: 16px 0 8px;
    }
    .mala-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--gold), var(--saffron));
        width: 0%;
        transition: width 0.2s;
    }
    .mala-stats {
        display: flex;
        justify-content: space-around;
        font-size: 0.85rem;
        margin-top: 10px;
    }

    /* SACRED HYMNS FEATURE CARDS */
    .hymns-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin: 20px 0 35px;
    }
    .hymn-card {
        background: white;
        border-radius: 14px;
        padding: 18px 20px;
        border-left: 5px solid var(--saffron);
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        text-decoration: none;
        color: inherit;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.25s;
    }
    .hymn-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(255,119,0,0.25);
        border-left-color: var(--maroon);
    }
    .hymn-icon {
        font-size: 2.2rem;
        background: #FFF3E0;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .hymn-info h4 { font-family: 'Rozha One', serif; color: var(--maroon); font-size: 1.05rem; }
    .hymn-info p { font-size: 0.8rem; color: #666; margin-top: 2px; }

    /* SANATAN FOOTER DIRECTORY */
    .footer-directory {
        max-width: 1200px;
        margin: 28px auto 20px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 24px;
        text-align: left;
        border-top: 1px solid rgba(255,215,0,0.3);
        padding-top: 24px;
    }
    .footer-dir-col h4 {
        color: var(--gold);
        font-family: 'Rozha One', serif;
        font-size: 1.05rem;
        margin-bottom: 12px;
        border-bottom: 1px dashed rgba(255,215,0,0.3);
        padding-bottom: 6px;
    }
    .footer-dir-col ul { list-style: none; }
    .footer-dir-col ul li { margin-bottom: 6px; }
    .footer-dir-col ul li a {
        color: var(--gold-light);
        text-decoration: none;
        font-size: 0.82rem;
        transition: color 0.2s;
        display: inline-block;
    }
    .footer-dir-col ul li a:hover { color: #FFF; text-decoration: underline; }

    /* TOAST */
    #toast {
        position: fixed;
        bottom: 70px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--maroon-dark);
        color: var(--gold);
        padding: 12px 24px;
        border-radius: 30px;
        border: 1px solid var(--gold);
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s;
        z-index: 999999;
        text-align: center;
        max-width: 90%;
    }
    #toast.show { opacity: 1; pointer-events: auto; }

    /* MOBILE BOTTOM NAV */
    .mobile-bottom-nav { display: none; }
    @media (max-width: 768px) {
        .mobile-bottom-nav {
            display: flex;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(74, 0, 14, 0.98);
            border-top: 2px solid var(--gold);
            padding: 8px 12px;
            justify-content: space-around;
            align-items: center;
            z-index: 100000;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.25);
            backdrop-filter: blur(8px);
        }
        .mobile-nav-item {
            color: var(--gold-light);
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.72rem;
            font-weight: 600;
            gap: 2px;
            background: none;
            border: none;
            cursor: pointer;
        }
        .mobile-nav-item span.icon { font-size: 1.25rem; }
        .mobile-nav-item:hover, .mobile-nav-item.active { color: var(--gold); transform: scale(1.08); }
    }

    /* DIGITAL DIYA & AARTI */
    .diya-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 16px 0;
        cursor: pointer;
        user-select: none;
    }
    .diya-flame {
        width: 18px;
        height: 28px;
        background: radial-gradient(ellipse at bottom, #FFD700 0%, #FF5722 65%, transparent 95%);
        border-radius: 50% 50% 20% 20%;
        box-shadow: 0 0 15px #FFD700, 0 0 25px #FF5722;
        animation: flicker 1.2s infinite alternate ease-in-out;
        opacity: 0.3;
        transition: opacity 0.5s;
    }
    .diya-flame.lit {
        opacity: 1;
        box-shadow: 0 0 20px #FFD700, 0 0 35px #FF5722, 0 0 50px rgba(255,215,0,0.6);
    }
    .diya-base {
        width: 54px;
        height: 18px;
        background: linear-gradient(180deg, #D84315 0%, #5D4037 100%);
        border-radius: 0 0 25px 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }
    @keyframes flicker {
        0% { transform: scale(1) rotate(-1deg); }
        50% { transform: scale(1.08, 1.15) rotate(1deg); }
        100% { transform: scale(0.96, 0.98) rotate(-0.5deg); }
    }

    /* FOOTER */
    .site-footer {
        background: linear-gradient(135deg, var(--maroon-dark), var(--maroon));
        color: var(--gold-light);
        text-align: center;
        padding: 36px 16px 80px;
        font-size: 0.85rem;
        margin-top: 50px;
    }
    .site-footer a { color: var(--gold); text-decoration: none; margin: 0 4px; }
    .site-footer a:hover { text-decoration: underline; }

    @media (max-width: 768px) {
        .detail-container { grid-template-columns: 1fr; gap: 20px; padding: 16px; }
        .gallery-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
        .card-body p { display: none; }
        .button-group { flex-direction: column; }
        .btn-big { width: 100%; justify-content: center; }
    }
</style>
"""

COMMON_FOOTER = """
<footer class="site-footer">
    <p style="font-size:1.15rem; font-family:'Rozha One', serif; color:var(--gold);">
        ॐ दैनिक हिन्दू भगवान दर्शन | Daily Hindu Gods 4K Wallpaper & WhatsApp Status
    </p>
    <p style="margin: 8px 0; color:var(--gold-light); font-size:0.9rem;">
        समस्त देवी-देवताओं के नित्य पावन 4K स्वरूप, आरती, चालीसा और दैनिक शुभ पंचांग।
    </p>

    <!-- SANATAN DIRECTORY / ALL PAGES INTERNAL LINKING (100% CRAWLABLE BY GOOGLEBOT) -->
    <div class="footer-directory">
        <div class="footer-dir-col">
            <h4>🕉️ देव दर्शन श्रेणियां</h4>
            <ul>
                <li><a href="category-cute.html">🧸 क्यूट बाल स्वरूप दर्शन (Cute 4K)</a></li>
                <li><a href="category-trending.html">🔥 ट्रेंडिंग 4K वॉलपेपर (Trending)</a></li>
                <li><a href="category-festival.html">🎉 त्यौहार व पर्व स्पेशल (Festivals)</a></li>
                <li><a href="category-shiva.html">🔱 महादेव शिव 4K फोटो (Lord Shiva)</a></li>
                <li><a href="category-krishna.html">🦚 श्री कृष्ण व बाल गोपाल (Lord Krishna)</a></li>
                <li><a href="category-ganesha.html">🐘 विघ्नहर्ता श्री गणेश (Lord Ganesha)</a></li>
                <li><a href="category-hanuman.html">🚩 संकटमोचन हनुमान जी (Lord Hanuman)</a></li>
                <li><a href="category-durga.html">🦁 माँ दुर्गा शेरावाली (Maa Durga)</a></li>
                <li><a href="category-lakshmi.html">🪷 माँ लक्ष्मी धनदायिनी (Maa Lakshmi)</a></li>
                <li><a href="category-ram.html">🏹 मर्यादा पुरुषोत्तम श्री राम (Lord Ram)</a></li>
                <li><a href="category-saraswati.html">🪕 माँ सरस्वती विद्यादायिनी (Maa Saraswati)</a></li>
            </ul>
        </div>
        <div class="footer-dir-col">
            <h4>📖 पावन चालीसा व आरतियां</h4>
            <ul>
                <li><a href="hanuman-chalisa.html">🚩 श्री हनुमान चालीसा (सम्पूर्ण पाठ व अर्थ)</a></li>
                <li><a href="shiv-aarti.html">🔱 ॐ जय शिव ओंकारा (महादेव पावन आरती)</a></li>
                <li><a href="ganesh-aarti.html">🐘 जय गणेश जय गणेश देवा (गणपति आरती)</a></li>
            </ul>
            <h4 style="margin-top:16px;">📿 दैनिक भक्ति टूल्स</h4>
            <ul>
                <li><a href="index.html#panchangSection">📅 दैनिक हिन्दू पंचांग व शुभ मुहूर्त</a></li>
                <li><a href="index.html#japMalaSection">📿 डिजिटल 108 जाप माला (Chant Counter)</a></li>
                <li><a href="javascript:void(0)" onclick="playTempleBell()">🔔 मंदिर घंटी बजाएं (Temple Bell)</a></li>
                <li><a href="javascript:void(0)" onclick="playShankh()">🐚 पावन शंख नाद (Conch Shell)</a></li>
                <li><a href="javascript:void(0)" onclick="toggleAmbientMusic()">🎵 ॐ दिव्य संगीत (Ambient Drone)</a></li>
            </ul>
        </div>
        <div class="footer-dir-col">
            <h4>🌸 लोकप्रिय 4K देव दर्शन</h4>
            <ul>
                <li><a href="photo-cute-radha-krishna.html">राधा कृष्ण क्यूट लव 4K फोटो</a></li>
                <li><a href="photo-cute-bal-shiva.html">क्यूट बाल शिव जी डमरू 4K</a></li>
                <li><a href="photo-cute-bal-hanuman.html">क्यूट बाल हनुमान जी संजीवनी</a></li>
                <li><a href="photo-cute-krishna-makhan.html">माखन चोर बाल गोपाल क्यूट फोटो</a></li>
                <li><a href="photo-cute-baby-lakshmi.html">क्यूट बेबी लक्ष्मी कमल पुष्प</a></li>
                <li><a href="photo-cute-baby-saraswati.html">क्यूट बेबी सरस्वती वीणा 4K</a></li>
                <li><a href="photo-cute-ganesha-reading.html">क्यूट बाल गणेश मोदक दर्शन</a></li>
                <li><a href="photo-shiva-kailash.html">महादेव शिव कैलाश पर्वत 4K</a></li>
                <li><a href="photo-ram-ayodhya.html">श्री राम अयोध्या धाम 4K वॉलपेपर</a></li>
                <li><a href="photo-durga-lion.html">माँ दुर्गा शेरावाली सिंह वाहिनी</a></li>
            </ul>
        </div>
    </div>

    <p style="margin-top: 20px;">
        <a href="index.html">Home</a> |
        <a href="category-cute.html">Cute Gallery</a> |
        <a href="category-trending.html">Trending Gods</a> |
        <a href="category-festival.html">Festivals</a> |
        <a href="hanuman-chalisa.html">हनुमान चालीसा</a> |
        <a href="shiv-aarti.html">शिव आरती</a> |
        <a href="ganesh-aarti.html">गणेश आरती</a> |
        <a href="sitemap.xml">Sitemap (XML)</a> |
        <a href="feed.xml">RSS Feed</a> |
        <a href="robots.txt">Robots.txt</a>
    </p>
    <p style="margin-top: 10px; font-size: 0.78rem; opacity: 0.8;">&copy; 2026 Hindu Gods Daily Gallery. Free 4K Download & Devotional WhatsApp Status.</p>
</footer>

<div class="mobile-bottom-nav">
    <a href="index.html" class="mobile-nav-item">
        <span class="icon">🏠</span>
        <span>होम</span>
    </a>
    <a href="category-cute.html" class="mobile-nav-item">
        <span class="icon">🧸</span>
        <span>क्यूट</span>
    </a>
    <a href="category-trending.html" class="mobile-nav-item">
        <span class="icon">🔥</span>
        <span>ट्रेंडिंग</span>
    </a>
    <a href="hanuman-chalisa.html" class="mobile-nav-item">
        <span class="icon">🚩</span>
        <span>चालीसा</span>
    </a>
    <button onclick="playTempleBell()" class="mobile-nav-item">
        <span class="icon">🔔</span>
        <span>घंटी</span>
    </button>
</div>

<div id="toast"></div>

<script>
// Persistent Diya Lighting
function toggleDiya() {
    var flame = document.getElementById('diyaFlame');
    if (flame) {
        var isLit = flame.classList.toggle('lit');
        if (isLit) {
            playTempleBell();
            createFlowerBurst();
            showToast('🪔 दीप प्रज्ज्वलित हुआ! आपका दिन मंगलमय हो 🙏');
            try { localStorage.setItem('diya_lit', '1'); } catch(e){}
        } else {
            showToast('दीप शांत किया गया');
            try { localStorage.removeItem('diya_lit'); } catch(e){}
        }
    }
}
window.addEventListener('DOMContentLoaded', function() {
    try {
        if (localStorage.getItem('diya_lit') === '1') {
            var f = document.getElementById('diyaFlame');
            if (f) f.classList.add('lit');
        }
    } catch(e){}
});

function showToast(msg) {
    var t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(function(){ t.classList.remove('show'); }, 2500);
}

function copyText(text, successMsg) {
    navigator.clipboard.writeText(text).then(function() {
        showToast(successMsg || 'कॉपी हो गया! 🙏');
    }).catch(function() {
        showToast('कॉपी नहीं हो सका');
    });
}

// Web Audio API Synthesizers: Bell, Shankh & Meditation Drone
var audioCtx = null;
function getAudioContext() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
}

function playTempleBell() {
    var ctx = getAudioContext();
    if (ctx.state === 'suspended') ctx.resume();
    var now = ctx.currentTime;
    var freqs = [587.33, 880, 1174.66, 1760];
    freqs.forEach(function(f, i) {
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(f, now);
        var vol = 0.3 / (i + 1);
        gain.gain.setValueAtTime(vol, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 3.5);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 3.5);
    });
    showToast('🔔 ॐ नमः शिवाय! पावन घंटी बजी 🙏');
    createFlowerBurst();
}

function playShankh() {
    var ctx = getAudioContext();
    if (ctx.state === 'suspended') ctx.resume();
    var now = ctx.currentTime;
    var osc = ctx.createOscillator();
    var gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(220, now);
    osc.frequency.linearRampToValueAtTime(246.94, now + 0.5);
    osc.frequency.linearRampToValueAtTime(261.63, now + 1.2);
    osc.frequency.linearRampToValueAtTime(246.94, now + 2.0);
    gain.gain.setValueAtTime(0.01, now);
    gain.gain.linearRampToValueAtTime(0.4, now + 0.4);
    gain.gain.linearRampToValueAtTime(0.3, now + 1.8);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.6);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 2.6);
    showToast('🐚 पावन शंख नाद! जय श्री राम 🙏');
    createFlowerBurst();
}

// Pure Web Audio Meditative Tanpura / Om Drone Synthesizer (100% Offline & Instant)
var ambientNodes = null;
var isAmbientPlaying = false;
function toggleAmbientMusic() {
    var ctx = getAudioContext();
    if (ctx.state === 'suspended') ctx.resume();
    var btn = document.getElementById('ambientMusicBtn');

    if (isAmbientPlaying) {
        if (ambientNodes) {
            ambientNodes.gain.gain.linearRampToValueAtTime(0.0001, ctx.currentTime + 1.0);
            setTimeout(function() {
                if (ambientNodes) {
                    ambientNodes.oscillators.forEach(function(o){ try { o.stop(); }catch(e){} });
                    ambientNodes = null;
                }
            }, 1100);
        }
        isAmbientPlaying = false;
        if (btn) {
            btn.classList.remove('playing');
            btn.innerHTML = '🎵 ॐ दिव्य संगीत चलाएं';
        }
        showToast('संगीत शांत किया गया');
    } else {
        var masterGain = ctx.createGain();
        masterGain.gain.setValueAtTime(0.0001, ctx.currentTime);
        masterGain.gain.linearRampToValueAtTime(0.18, ctx.currentTime + 2.0);
        masterGain.connect(ctx.destination);

        // Indian Tanpura Harmonics (C#3: 138.59Hz, G#3: 207.65Hz, C#4: 277.18Hz)
        var chord = [69.3, 138.59, 207.65, 277.18, 415.30];
        var oscs = [];
        chord.forEach(function(freq, idx) {
            var osc = ctx.createOscillator();
            var oscGain = ctx.createGain();
            osc.type = (idx % 2 === 0) ? 'sine' : 'triangle';
            osc.frequency.setValueAtTime(freq, ctx.currentTime);
            
            // Subtle slow tremolo/shimmer
            var lfo = ctx.createOscillator();
            lfo.frequency.setValueAtTime(0.2 + idx * 0.05, ctx.currentTime);
            var lfoGain = ctx.createGain();
            lfoGain.gain.setValueAtTime(0.04, ctx.currentTime);
            lfo.connect(oscGain.gain);
            lfo.start();

            oscGain.gain.setValueAtTime(0.12 / (idx + 1), ctx.currentTime);
            osc.connect(oscGain);
            oscGain.connect(masterGain);
            osc.start();
            oscs.push(osc);
            oscs.push(lfo);
        });

        ambientNodes = { masterGain: masterGain, gain: masterGain, oscillators: oscs };
        isAmbientPlaying = true;
        if (btn) {
            btn.classList.add('playing');
            btn.innerHTML = '🔊 ॐ संगीत बज रहा है (रोकें)';
        }
        showToast('🎵 ॐ पावन धुन आरंभ हुई! ध्यानमग्न रहें 🙏');
    }
}

function createFlowerBurst() {
    var icons = ['🌸', '🌺', '🌼', '🪷', '✨'];
    for (var i = 0; i < 18; i++) {
        var f = document.createElement('div');
        f.textContent = icons[Math.floor(Math.random() * icons.length)];
        f.style.position = 'fixed';
        f.style.left = (15 + Math.random() * 70) + 'vw';
        f.style.top = (40 + Math.random() * 30) + 'vh';
        f.style.fontSize = (20 + Math.random() * 24) + 'px';
        f.style.pointerEvents = 'none';
        f.style.zIndex = '99999';
        f.style.transition = 'all 1.8s ease-out';
        f.style.transform = 'translateY(0) scale(1)';
        f.style.opacity = '1';
        document.body.appendChild(f);
        (function(el) {
            setTimeout(function() {
                el.style.transform = 'translate(' + ((Math.random() - 0.5) * 220) + 'px, -' + (100 + Math.random() * 160) + 'px) scale(1.4)';
                el.style.opacity = '0';
            }, 50);
            setTimeout(function() { el.remove(); }, 1900);
        })(f);
    }
}

// 108 Jap Mala Counter logic
var malaCount = 0;
var totalMalas = 0;
function countMalaBead() {
    malaCount++;
    if (malaCount > 108) {
        malaCount = 1;
        totalMalas++;
        document.getElementById('malaCompletedCount').textContent = totalMalas;
    }
    document.getElementById('malaBeadText').textContent = malaCount + ' / 108';
    var pct = (malaCount / 108) * 100;
    document.getElementById('malaProgressFill').style.width = pct + '%';

    if (malaCount === 108) {
        playTempleBell();
        createFlowerBurst();
        showToast('🎉 108 जाप पूर्ण! प्रभु की कृपा आप पर सदा रहे 🙏');
    }
}
function resetMala() {
    malaCount = 0;
    document.getElementById('malaBeadText').textContent = '0 / 108';
    document.getElementById('malaProgressFill').style.width = '0%';
    showToast('जाप माला रीसेट की गई');
}

// 1-Click WhatsApp Shubh Prabhat Greeting
function shareCustomWhatsApp(godTitle, url, mantra) {
    var d = new Date();
    var dateStr = d.toLocaleDateString('hi-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    var msg = "🌸 *शुभ प्रभात! आज का पावन दर्शन* 🌸\\n\\n" +
              "🕉️ *" + godTitle + "*\\n" +
              "📅 " + dateStr + "\\n" +
              "✨ *पावन मंत्र:* " + (mantra || 'ॐ नमो भगवते वासुदेवाय नमः') + "\\n\\n" +
              "📲 4K दर्शन और फ्री डाउनलोड करें:\\n" + url + "\\n\\n" +
              "🚩 *आपका दिन मंगलमय और सुखमय हो!* 🙏";
    var waUrl = "https://api.whatsapp.com/send?text=" + encodeURIComponent(msg);
    window.open(waUrl, '_blank');
}
</script>
"""

def generate_photo_page(item, all_items):
    related = [x for x in all_items if x["id"] != item["id"] and (x["god"] == item["god"] or x["category"] == item["category"])][:4]
    if len(related) < 4:
        extra = [x for x in all_items if x["id"] != item["id"] and x not in related][:4 - len(related)]
        related.extend(extra)
        
    img_jpg = item["img"] + ".jpg"
    img_webp = item["img"] + ".webp"
    page_url = BASE_URL + item["slug"]
    img_abs_url = BASE_URL + img_jpg

    related_html = ""
    for r in related:
        related_html += f"""
        <div class="card">
            <a class="card-img-link" href="{r['slug']}">
                <span class="badge">{r['badge']}</span>
                <picture>
                    <source srcset="{r['img']}.webp" type="image/webp">
                    <img src="{r['img']}.jpg" alt="{r['title']}" loading="lazy" width="400" height="533">
                </picture>
            </a>
            <div class="card-body">
                <h3><a href="{r['slug']}">{r['titleHi']}</a></h3>
                <p>{r['shortDesc']}</p>
                <div class="card-actions">
                    <a href="{r['slug']}" class="btn-action btn-view">View 4K</a>
                    <button onclick="shareCustomWhatsApp('{r['titleHi']}', '{BASE_URL}{r['slug']}', '{r.get('mantra','')[:50]}...')" class="btn-action btn-wa">WA</button>
                </div>
            </div>
        </div>
        """

    tags_html = "".join([f'<a href="index.html?q={t}" class="tag-item">#{t}</a>' for t in item["tags"]])

    html = f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>{item['titleHi']} | {item['title']} Free Download & WhatsApp Status</title>
    <meta name="description" content="{item['titleHi']} - {item['shortDesc']} Free 4K Ultra HD Wallpaper download & 1-click WhatsApp Status sharing.">
    <meta name="keywords" content="{', '.join(item['tags'])}, {item['title']}, {item['titleHi']}, 4k wallpaper, whatsapp status">
    <link rel="canonical" href="{page_url}">
    
    <!-- Open Graph for Social & WhatsApp Preview -->
    <meta property="og:site_name" content="Hindu Gods Daily Gallery">
    <meta property="og:title" content="{item['titleHi']} - {item['title']}">
    <meta property="og:description" content="{item['shortDesc']}">
    <meta property="og:image" content="{img_abs_url}">
    <meta property="og:image:width" content="1024">
    <meta property="og:image:height" content="1365">
    <meta property="og:url" content="{page_url}">
    <meta property="og:type" content="article">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{item['titleHi']} | 4K Wallpaper">
    <meta name="twitter:description" content="{item['shortDesc']}">
    <meta name="twitter:image" content="{img_abs_url}">
    
    <!-- Google Schema.org ImageObject & BreadcrumbList -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "ImageObject",
          "name": "{item['titleHi']} - {item['title']}",
          "caption": "{item['shortDesc']}",
          "description": "{item['shortDesc']}",
          "contentUrl": "{img_abs_url}",
          "thumbnailUrl": "{img_abs_url}",
          "encodingFormat": "image/jpeg",
          "keywords": {json.dumps(item['tags'], ensure_ascii=False)},
          "author": {{ "@type": "Organization", "name": "Hindu Gods Daily Gallery" }}
        }},
        {{
          "@type": "BreadcrumbList",
          "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE_URL}" }},
            {{ "@type": "ListItem", "position": 2, "name": "{item['categoryName']}", "item": "{BASE_URL}{item['categorySlug']}" }},
            {{ "@type": "ListItem", "position": 3, "name": "{item['titleHi']}", "item": "{page_url}" }}
          ]
        }}
      ]
    }}
    </script>
    {COMMON_STYLE}
</head>
<body>

<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper & WhatsApp Status</p>
    <button id="ambientMusicBtn" class="header-audio-btn" onclick="toggleAmbientMusic()">🎵 ॐ दिव्य संगीत चलाएं</button>
</header>

<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="category-cute.html" class="nav-link { 'active' if item['category'] == 'cute' else '' }">🧸 Cute Gallery</a>
    <a href="category-trending.html" class="nav-link { 'active' if item['category'] == 'trending' else '' }">🔥 Trending 4K</a>
    <a href="category-festival.html" class="nav-link { 'active' if item['category'] == 'festival' else '' }">🎉 Festival Special</a>
    <a href="category-shiva.html" class="nav-link">🔱 Mahadev</a>
    <a href="category-krishna.html" class="nav-link">🦚 Krishna</a>
    <a href="category-ganesha.html" class="nav-link">🐘 Ganesha</a>
    <a href="category-hanuman.html" class="nav-link">🚩 Hanuman</a>
    <a href="hanuman-chalisa.html" class="nav-link" style="color:var(--saffron);">🚩 हनुमान चालीसा</a>
</nav>

<div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <a href="{item['categorySlug']}">{item['categoryName']}</a> &raquo;
        <span>{item['titleHi']}</span>
    </nav>

    <div class="detail-container">
        <div class="detail-img-wrap">
            <span class="badge" style="top:16px; left:16px; font-size:0.85rem; padding:6px 14px;">{item['badge']}</span>
            <picture>
                <source srcset="{img_webp}" type="image/webp">
                <img src="{img_jpg}" alt="{item['titleHi']} - {item['title']} 4K Free Download" width="1024" height="1365">
            </picture>

            <div class="diya-container" onclick="toggleDiya()" title="क्लिक करके दीप जलाएं">
                <div id="diyaFlame" class="diya-flame"></div>
                <div class="diya-base"></div>
                <span style="font-size:0.75rem; color:#8D6E63; font-weight:700; margin-top:6px;">🪔 दीप प्रज्ज्वलित करें (Tap to Light)</span>
            </div>
        </div>

        <div class="detail-info">
            <h1>{item['titleHi']}</h1>
            <h2>{item['title']}</h2>
            <p style="color:#666; font-size:0.95rem; margin-bottom:12px;">{item['shortDesc']}</p>

            <div class="mantra-box">
                <div class="mantra-heading">
                    <span>🌸 पावन मंत्र एवं श्लोक</span>
                    <button class="btn-copy-mantra" onclick="copyText(`{item['mantra']}`, 'मंत्र कॉपी हो गया! 🙏')">📋 Copy Mantra</button>
                </div>
                <div class="mantra-text">{item['mantra']}</div>
                <div class="mantra-meaning"><strong>अर्थ:</strong> {item['mantraMeaning']}</div>
            </div>

            <div class="button-group">
                <button onclick="shareCustomWhatsApp('{item['titleHi']}', '{page_url}', `{item['mantra']}`)" class="btn-big btn-big-wa">
                    <span>📱 1-Click WhatsApp Status</span>
                </button>
                <a href="{img_jpg}" download="{item['id']}_4k.jpg" class="btn-big btn-big-dl">
                    <span>📥 Download 4K Image</span>
                </a>
                <button onclick="playTempleBell()" class="btn-big" style="background:#FF7700;">
                    <span>🔔 मंदिर घंटी</span>
                </button>
                <button onclick="playShankh()" class="btn-big" style="background:#4A000E;">
                    <span>🐚 शंख नाद</span>
                </button>
                <button onclick="createFlowerBurst(); showToast('🌸 पुष्प अर्पित किए! 🙏');" class="btn-big" style="background:#E91E63;">
                    <span>🌸 पुष्प अर्पित करें</span>
                </button>
                <a href="https://pinterest.com/pin/create/button/?url={page_url}&media={img_abs_url}&description={item['titleHi']}" target="_blank" class="btn-big btn-big-pin">
                    <span>📌 Pinterest</span>
                </a>
            </div>

            <div class="article-box">
                <h3 style="color:var(--maroon); margin-bottom:10px; font-family:'Rozha One', serif;">धार्मिक महत्व एवं वॉलपेपर विवरण</h3>
                <p>{item['article']}</p>
                
                <h4 style="color:var(--maroon); margin-top:16px; margin-bottom:8px;">संबंधित सर्च कीवर्ड्स (Tags):</h4>
                <div class="tag-cloud">
                    {tags_html}
                </div>
            </div>
        </div>
    </div>

    <section style="margin-top: 30px;">
        <h2 style="font-family:'Rozha One', serif; color:var(--maroon); text-align:center; margin-bottom:16px;">
            🌸 और भी मनमोहक दर्शन (Related 4K Wallpapers)
        </h2>
        <div class="gallery-grid">
            {related_html}
        </div>
    </section>
</div>

{COMMON_FOOTER}

</body>
</html>"""
    return html

def generate_category_page(cat, all_items):
    cat_items = []
    if cat["id"] == "cute":
        cat_items = [x for x in all_items if x["category"] == "cute" or "cute" in x["tags"]]
    elif cat["id"] == "trending":
        cat_items = [x for x in all_items if x.get("badge") == "Trending 4K" or "trending" in x["category"] or x.get("trending")]
    elif cat["id"] == "festival":
        cat_items = [x for x in all_items if x["category"] == "festival"]
    else:
        cat_items = [x for x in all_items if x.get("god") == cat["id"] or x.get("category") == cat["id"]]
    
    cards_html = ""
    for it in cat_items:
        cards_html += f"""
        <div class="card">
            <a class="card-img-link" href="{it['slug']}">
                <span class="badge">{it['badge']}</span>
                <picture>
                    <source srcset="{it['img']}.webp" type="image/webp">
                    <img src="{it['img']}.jpg" alt="{it['title']}" loading="lazy" width="400" height="533">
                </picture>
            </a>
            <div class="card-body">
                <h3><a href="{it['slug']}">{it['titleHi']}</a></h3>
                <p>{it['shortDesc']}</p>
                <div class="card-actions">
                    <a href="{it['slug']}" class="btn-action btn-view">View 4K</a>
                    <button onclick="shareCustomWhatsApp('{it['titleHi']}', '{BASE_URL}{it['slug']}', '{it.get('mantra','')[:50]}...')" class="btn-action btn-wa">WA</button>
                    <a href="{it['img']}.jpg" download class="btn-action btn-dl">Download</a>
                </div>
            </div>
        </div>
        """

    cat_url = BASE_URL + cat["slug"]
    html = f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>{cat['nameHi']} 4K Wallpaper & Photos | {cat['name']} Free Download</title>
    <meta name="description" content="{cat['desc']} Free 4K Ultra HD Wallpapers & WhatsApp Status photos download.">
    <link rel="canonical" href="{cat_url}">
    
    <meta property="og:title" content="{cat['nameHi']} | 4K Hindu Gods Gallery">
    <meta property="og:description" content="{cat['desc']}">
    <meta property="og:url" content="{cat_url}">
    <meta property="og:type" content="website">
    
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "{cat['nameHi']} - {cat['name']}",
      "description": "{cat['desc']}",
      "url": "{cat_url}"
    }}
    </script>
    {COMMON_STYLE}
</head>
<body>

<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>{cat['nameHi']} - {cat['name']}</p>
    <button id="ambientMusicBtn" class="header-audio-btn" onclick="toggleAmbientMusic()">🎵 ॐ दिव्य संगीत चलाएं</button>
</header>

<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="category-cute.html" class="nav-link { 'active' if cat['id'] == 'cute' else '' }">🧸 Cute Gallery</a>
    <a href="category-trending.html" class="nav-link { 'active' if cat['id'] == 'trending' else '' }">🔥 Trending 4K</a>
    <a href="category-festival.html" class="nav-link { 'active' if cat['id'] == 'festival' else '' }">🎉 Festival Special</a>
    <a href="category-shiva.html" class="nav-link { 'active' if cat['id'] == 'shiva' else '' }">🔱 Mahadev</a>
    <a href="category-krishna.html" class="nav-link { 'active' if cat['id'] == 'krishna' else '' }">🦚 Krishna</a>
    <a href="category-ganesha.html" class="nav-link { 'active' if cat['id'] == 'ganesha' else '' }">🐘 Ganesha</a>
    <a href="category-hanuman.html" class="nav-link { 'active' if cat['id'] == 'hanuman' else '' }">🚩 Hanuman</a>
    <a href="hanuman-chalisa.html" class="nav-link" style="color:var(--saffron);">🚩 चालीसा</a>
</nav>

<div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>{cat['nameHi']}</span>
    </nav>

    <div style="text-align: center; margin: 10px 0 24px;">
        <h1 style="font-family:'Rozha One', serif; color:var(--maroon); font-size:2rem;">{cat['nameHi']}</h1>
        <p style="color:#666; max-width:800px; margin:8px auto; font-size:0.95rem;">{cat['desc']}</p>
    </div>

    <div class="gallery-grid">
        {cards_html}
    </div>
</div>

{COMMON_FOOTER}

</body>
</html>"""
    return html

def generate_index_page(all_items):
    cute_items = [x for x in all_items if x["category"] == "cute"]
    trending_items = [x for x in all_items if x.get("badge") == "Trending 4K" or x.get("trending")]
    festival_items = [x for x in all_items if x["category"] == "festival"]

    def build_grid(items_list):
        h = ""
        for it in items_list:
            h += f"""
            <div class="card" data-search="{it['title'].lower()} {it['titleHi']} {' '.join(it['tags'])}">
                <a class="card-img-link" href="{it['slug']}">
                    <span class="badge">{it['badge']}</span>
                    <picture>
                        <source srcset="{it['img']}.webp" type="image/webp">
                        <img src="{it['img']}.jpg" alt="{it['titleHi']} - {it['title']}" loading="lazy" width="400" height="533">
                    </picture>
                </a>
                <div class="card-body">
                    <h3><a href="{it['slug']}">{it['titleHi']}</a></h3>
                    <p>{it['shortDesc']}</p>
                    <div class="card-actions">
                        <a href="{it['slug']}" class="btn-action btn-view">View 4K</a>
                        <button onclick="shareCustomWhatsApp('{it['titleHi']}', '{BASE_URL}{it['slug']}', '{it.get('mantra','')[:50]}...')" class="btn-action btn-wa">WA</button>
                        <a href="{it['img']}.jpg" download class="btn-action btn-dl">Download</a>
                    </div>
                </div>
            </div>
            """
        return h

    # Daily Hindu Panchang & Vaar calculations
    today = date.today()
    weekdays_hi = ["सोमवार (Monday)", "मंगलवार (Tuesday)", "बुधवार (Wednesday)", "गुरुवार (Thursday)", "शुक्रवार (Friday)", "शनिवार (Saturday)", "रविवार (Sunday)"]
    weekday_idx = today.weekday()
    day_name_hi = weekdays_hi[weekday_idx]
    
    deity_by_day = [
        {"god": "महादेव शिव (Lord Shiva)", "mantra": "ॐ नमः शिवाय", "link": "category-shiva.html"},
        {"god": "श्री हनुमान जी (Bajrangbali)", "mantra": "ॐ हनुमते नमः", "link": "category-hanuman.html"},
        {"god": "विघ्नहर्ता श्री गणेश (Ganesha)", "mantra": "ॐ गं गणपतये नमः", "link": "category-ganesha.html"},
        {"god": "भगवान विष्णु व श्री कृष्ण", "mantra": "ॐ नमो भगवते वासुदेवाय", "link": "category-krishna.html"},
        {"god": "माँ लक्ष्मी व माँ दुर्गा", "mantra": "ॐ श्रीं ह्रीं क्लीं नमः", "link": "category-lakshmi.html"},
        {"god": "शनि देव व हनुमान जी", "mantra": "ॐ शं शनैश्चराय नमः", "link": "category-hanuman.html"},
        {"god": "सूर्य देव व प्रभु श्री राम", "mantra": "ॐ सूर्याय नमः / जय श्री राम", "link": "category-ram.html"}
    ]
    today_deity = deity_by_day[weekday_idx]

    html = f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>ॐ दैनिक हिन्दू भगवान दर्शन | Daily Cute Hindu Gods 4K Wallpaper & WhatsApp Status</title>
    <meta name="description" content="दैनिक 21+ नए मनमोहक, क्यूट और 4K हिन्दू भगवानों के AI फोटो। बाल गोपाल, बाल गणेश, महादेव शिव, राम लला, हनुमान जी, माँ लक्ष्मी और माँ दुर्गा के सर्वश्रेष्ठ व्हाट्सएप स्टेटस और वॉलपेपर फ्री डाउनलोड।">
    <meta name="keywords" content="cute bhagwan photo, hindu gods photos, good morning god images today, hindu god images for whatsapp status, cute bal gopal photo, baby krishna makhan chor wallpaper 4k, mahadev 4k wallpaper download, lord shiva kailash 3d wallpaper, bholenath photo hd, ram lalla ayodhya photo 4k, ram mandir wallpaper, cute bal ganesh 3d, ganpati bappa cute photo, hanuman ji 4k wallpaper full screen, bajrangbali hd photo, maa durga 4k wallpaper navratri, sherawali mata image, maa lakshmi photo download, diwali lakshmi pujan wallpaper, radha krishna cute love photo, all hindu gods 4k wallpaper, shubh prabhat bhagwan photo, daily god images 2026, 3d ai hindu god images, cute god wallpaper for mobile, god images with quotes in hindi, bhagwan ke photo download, lord shiva hd 1080p, shri ram 4k wallpaper ayodhya">
    <link rel="canonical" href="{BASE_URL}">
    
    <meta property="og:site_name" content="Hindu Gods Daily Gallery">
    <meta property="og:title" content="ॐ दैनिक हिन्दू भगवान दर्शन | Daily Cute Hindu Gods 4K Photos">
    <meta property="og:description" content="21+ क्यूट बाल गोपाल, बाल गणेश, महादेव शिव एवं सभी देवी-देवताओं के 4K वॉलपेपर व व्हाट्सएप स्टेटस फ्री डाउनलोड।">
    <meta property="og:image" content="{BASE_URL}images/cute_radha_krishna.jpg">
    <meta property="og:image:width" content="1024">
    <meta property="og:image:height" content="1365">
    <meta property="og:url" content="{BASE_URL}">
    <meta property="og:type" content="website">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="ॐ Daily Cute Hindu Gods 4K Photos & Festival Special">
    <meta name="twitter:description" content="Daily 21+ cute divine Hindu god images in Ultra HD 4K with WhatsApp Status sharing.">
    <meta name="twitter:image" content="{BASE_URL}images/cute_radha_krishna.jpg">

    <script type="application/ld+json">
    [
      {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Hindu Gods Daily Gallery",
        "url": "{BASE_URL}",
        "potentialAction": {{
          "@type": "SearchAction",
          "target": "{BASE_URL}?q={{search_term_string}}",
          "query-input": "required name=search_term_string"
        }}
      }},
      {{
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "name": "Daily Hindu Gods 4K Photo Gallery",
        "description": "Daily automated cute and divine high-resolution 4K AI images of Hindu deities.",
        "url": "{BASE_URL}"
      }}
    ]
    </script>
    {COMMON_STYLE}
    <style>
        .search-container {{
            max-width: 650px;
            margin: 20px auto;
            position: relative;
        }}
        .search-input {{
            width: 100%;
            padding: 14px 24px;
            border-radius: 30px;
            border: 2px solid var(--saffron);
            font-size: 1rem;
            outline: none;
            box-shadow: 0 4px 15px rgba(255,119,0,0.15);
            transition: all 0.3s;
        }}
        .search-input:focus {{
            border-color: var(--maroon);
            box-shadow: 0 4px 20px rgba(255,119,0,0.3);
        }}
        .category-pills {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin: 16px 0 24px;
        }}
        .cat-pill {{
            padding: 8px 18px;
            border-radius: 25px;
            background: white;
            border: 1.5px solid var(--saffron);
            color: var(--maroon);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.25s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        .cat-pill:hover {{
            background: linear-gradient(135deg, var(--saffron), var(--maroon));
            color: white;
            transform: translateY(-2px);
        }}
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 36px 0 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid rgba(255,119,0,0.25);
        }}
        .section-header h2 {{
            font-family: 'Rozha One', serif;
            color: var(--maroon);
            font-size: clamp(1.3rem, 3vw, 1.8rem);
        }}
        .section-header a {{
            color: var(--saffron);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .section-header a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>

<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper & WhatsApp Status</p>
    <button id="ambientMusicBtn" class="header-audio-btn" onclick="toggleAmbientMusic()">🎵 ॐ दिव्य संगीत चलाएं</button>
</header>

<nav class="top-nav">
    <a href="index.html" class="nav-link active">Home (होम)</a>
    <a href="category-cute.html" class="nav-link">🧸 Cute Gallery</a>
    <a href="category-trending.html" class="nav-link">🔥 Trending 4K</a>
    <a href="category-festival.html" class="nav-link">🎉 Festival Special</a>
    <a href="category-shiva.html" class="nav-link">🔱 Mahadev</a>
    <a href="category-krishna.html" class="nav-link">🦚 Krishna</a>
    <a href="category-ganesha.html" class="nav-link">🐘 Ganesha</a>
    <a href="category-hanuman.html" class="nav-link">🚩 Hanuman</a>
    <a href="category-durga.html" class="nav-link">🦁 Durga</a>
    <a href="category-lakshmi.html" class="nav-link">🪷 Lakshmi</a>
    <a href="category-ram.html" class="nav-link">🏹 Ram</a>
    <a href="category-saraswati.html" class="nav-link">🪕 Saraswati</a>
    <a href="hanuman-chalisa.html" class="nav-link" style="color:var(--saffron);">🚩 चालीसा</a>
</nav>

<div class="container">

    <!-- SEARCH BAR -->
    <div class="search-container">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 भगवान खोजें: Cute Bal Gopal, Mahadev 4K, Navratri, Hanuman..." onkeyup="filterCards()">
    </div>

    <!-- QUICK CATEGORY PILLS -->
    <div class="category-pills">
        <a href="category-cute.html" class="cat-pill">🧸 Cute Gallery ({len(cute_items)})</a>
        <a href="category-trending.html" class="cat-pill">🔥 Trending 4K ({len(trending_items)})</a>
        <a href="category-festival.html" class="cat-pill">🎉 Festival Special ({len(festival_items)})</a>
        <a href="category-shiva.html" class="cat-pill">🔱 भगवान शिव</a>
        <a href="category-krishna.html" class="cat-pill">🦚 श्री कृष्ण</a>
        <a href="category-ganesha.html" class="cat-pill">🐘 गणपति बप्पा</a>
        <a href="category-hanuman.html" class="cat-pill">🚩 संकटमोचन हनुमान</a>
        <a href="category-durga.html" class="cat-pill">🦁 मां दुर्गा</a>
        <a href="category-lakshmi.html" class="cat-pill">🪷 मां लक्ष्मी</a>
        <a href="category-ram.html" class="cat-pill">🏹 प्रभु श्री राम</a>
        <a href="category-saraswati.html" class="cat-pill">🪕 मां सरस्वती</a>
    </div>

    <!-- DAILY PANCHANG & SHUBH MUHURAT WIDGET -->
    <div class="panchang-card" id="panchangSection">
        <div class="panchang-header">
            <h3>📅 दैनिक हिन्दू पंचांग एवं शुभ मुहूर्त</h3>
            <button onclick="shareCustomWhatsApp('आज का दैनिक पंचांग दर्शन', '{BASE_URL}', 'आज के आराध्य: {today_deity['god']}')" class="btn-action btn-wa" style="padding:6px 14px; border-radius:20px;">
                📲 पंचांग व्हाट्सएप पर भेजें
            </button>
        </div>
        <div class="panchang-grid">
            <div class="panchang-item">
                <span class="label">आज का दिन (Day)</span>
                <strong>{day_name_hi}</strong>
            </div>
            <div class="panchang-item">
                <span class="label">आज के आराध्य देव</span>
                <strong><a href="{today_deity['link']}" style="color:var(--maroon); text-decoration:none;">{today_deity['god']}</a></strong>
            </div>
            <div class="panchang-item">
                <span class="label">आज का पावन मंत्र</span>
                <strong>{today_deity['mantra']}</strong>
            </div>
            <div class="panchang-item">
                <span class="label">अभिजित मुहूर्त (शुभ समय)</span>
                <strong style="color:#2E7D32;">11:48 AM - 12:38 PM (अत्यंत शुभ)</strong>
            </div>
        </div>
        <div class="suvichar-box">
            🌸 <strong>आज का सुविचार:</strong> "ईश्वर पर अटूट विश्वास और शुद्ध कर्म ही मनुष्य के समस्त संकटों को दूर करते हैं। प्रभु स्मरण से मन को परम शांति प्राप्त होती है।"
        </div>
    </div>

    <!-- DIGITAL 108 JAP MALA COUNTER -->
    <div class="mala-card" id="japMalaSection">
        <h3>📿 डिजिटल 108 जाप माला (Chant Counter)</h3>
        <p style="font-size:0.88rem; opacity:0.9;">आराध्य देव का नाम जपें और दैनिक 108 मणियों की माला पूर्ण करें</p>
        <select class="mala-mantra-select" id="malaMantraSelect">
            <option>ॐ नमः शिवाय (Lord Shiva)</option>
            <option>हरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे</option>
            <option>ॐ गं गणपतये नमः (Lord Ganesha)</option>
            <option>जय श्री राम (Lord Ram)</option>
            <option>ॐ हनुमते नमः (Lord Hanuman)</option>
            <option>ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं (गायत्री मंत्र)</option>
        </select>
        <div>
            <button class="mala-bead-btn" onclick="countMalaBead()">
                <span style="font-size:0.85rem; opacity:0.8;">जाप</span>
                <span id="malaBeadText">0 / 108</span>
            </button>
        </div>
        <div class="mala-progress-bar">
            <div id="malaProgressFill" class="mala-progress-fill"></div>
        </div>
        <div class="mala-stats">
            <span>माला पूर्ण: <strong id="malaCompletedCount">0</strong></span>
            <button onclick="resetMala()" style="background:none; border:1px solid var(--gold); color:var(--gold); padding:2px 10px; border-radius:12px; cursor:pointer; font-size:0.75rem;">रीसेट करें</button>
        </div>
    </div>

    <!-- SACRED HYMNS & AARTIS -->
    <div class="section-header">
        <h2>📖 संपूर्ण पाठ, चालीसा एवं पावन आरतियां</h2>
    </div>
    <div class="hymns-grid">
        <a href="hanuman-chalisa.html" class="hymn-card">
            <div class="hymn-icon">🚩</div>
            <div class="hymn-info">
                <h4>श्री हनुमान चालीसा</h4>
                <p>दोहा, चौपाई, अर्थ सहित संपूर्ण पाठ पढ़ें</p>
            </div>
        </a>
        <a href="shiv-aarti.html" class="hymn-card">
            <div class="hymn-icon">🔱</div>
            <div class="hymn-info">
                <h4>ॐ जय शिव ओंकारा</h4>
                <p>महादेव की संपूर्ण आरती एवं नित्य पाठ</p>
            </div>
        </a>
        <a href="ganesh-aarti.html" class="hymn-card">
            <div class="hymn-icon">🐘</div>
            <div class="hymn-info">
                <h4>जय गणेश जय गणेश देवा</h4>
                <p>विघ्नहर्ता गणपति बप्पा की मंगलकारी आरती</p>
            </div>
        </a>
    </div>

    <!-- FESTIVAL SPECIAL SECTION -->
    <section>
        <div class="section-header">
            <h2>🎉 Festival Special | त्यौहार स्पेशल 4K</h2>
            <a href="category-festival.html">View All &raquo;</a>
        </div>
        <div class="gallery-grid" id="festivalGrid">
            {build_grid(festival_items)}
        </div>
    </section>

    <!-- CUTE GALLERY SECTION -->
    <section>
        <div class="section-header">
            <h2>🧸 Cute Gallery | मनमोहक बाल स्वरूप 4K</h2>
            <a href="category-cute.html">View All &raquo;</a>
        </div>
        <div class="gallery-grid" id="cuteGrid">
            {build_grid(cute_items)}
        </div>
    </section>

    <!-- TRENDING SECTION -->
    <section>
        <div class="section-header">
            <h2>🔥 Trending Gods | सर्वाधिक लोकप्रिय 4K वॉलपेपर</h2>
            <a href="category-trending.html">View All &raquo;</a>
        </div>
        <div class="gallery-grid" id="trendingGrid">
            {build_grid(trending_items)}
        </div>
    </section>
</div>

{COMMON_FOOTER}

<script>
function filterCards() {{
    var q = document.getElementById('searchInput').value.toLowerCase().trim();
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(c) {{
        var s = c.getAttribute('data-search') || '';
        if (!q || s.indexOf(q) !== -1) {{
            c.style.display = '';
        }} else {{
            c.style.display = 'none';
        }}
    }});
}}

// PWA Service worker registration
if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('sw.js').catch(function(){{}});
}}
</script>

</body>
</html>"""
    return html

def generate_rss_feed(all_items):
    from datetime import timezone
    now_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        '    <title>ॐ दैनिक हिन्दू भगवान दर्शन | Daily Hindu Gods 4K Wallpaper</title>',
        f'    <link>{BASE_URL}</link>',
        '    <description>Daily automated cute and divine 4K AI images of Hindu deities, Mantras and WhatsApp Status.</description>',
        '    <language>hi</language>',
        f'    <lastBuildDate>{now_str}</lastBuildDate>',
        f'    <atom:link href="{BASE_URL}feed.xml" rel="self" type="application/rss+xml" />'
    ]
    for it in all_items:
        xml.append('    <item>')
        xml.append(f'      <title><![CDATA[{it["titleHi"]} | {it["title"]}]]></title>')
        xml.append(f'      <link>{BASE_URL}{it["slug"]}</link>')
        xml.append(f'      <guid isPermaLink="true">{BASE_URL}{it["slug"]}</guid>')
        xml.append(f'      <description><![CDATA[{it["shortDesc"]}]]></description>')
        xml.append(f'      <enclosure url="{BASE_URL}{it["img"]}.jpg" length="250000" type="image/jpeg" />')
        xml.append(f'      <pubDate>{now_str}</pubDate>')
        xml.append('    </item>')
    xml.append('  </channel>')
    xml.append('</rss>')
    return '\n'.join(xml)

def generate_sitemap(all_items, all_cats):
    today_iso = date.today().isoformat()
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        '  <!-- Homepage with Top Image Extensions for Instant Google Discovery -->',
        '  <url>',
        f'    <loc>{BASE_URL}</loc>',
        f'    <lastmod>{today_iso}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>'
    ]

    # Add top 25 images right to the homepage URL so Googlebot Image indexes them on first crawl!
    for it in all_items[:25]:
        xml_lines.append('    <image:image>')
        xml_lines.append(f'      <image:loc>{BASE_URL}{it["img"]}.jpg</image:loc>')
        xml_lines.append(f'      <image:title>{it["titleHi"]} - {it["title"]}</image:title>')
        xml_lines.append(f'      <image:caption>{it["shortDesc"]}</image:caption>')
        xml_lines.append('    </image:image>')
    xml_lines.append('  </url>')

    # Category pages with their respective images
    xml_lines.append('  <!-- Category Pages -->')
    for cat in all_cats:
        c_items = [x for x in all_items if x.get("god") == cat["id"] or x.get("category") == cat["id"]]
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{BASE_URL}{cat["slug"]}</loc>')
        xml_lines.append(f'    <lastmod>{today_iso}</lastmod>')
        xml_lines.append('    <changefreq>daily</changefreq>')
        xml_lines.append('    <priority>0.9</priority>')
        for it in c_items[:10]:
            xml_lines.append('    <image:image>')
            xml_lines.append(f'      <image:loc>{BASE_URL}{it["img"]}.jpg</image:loc>')
            xml_lines.append(f'      <image:title>{it["titleHi"]} - {it["title"]}</image:title>')
            xml_lines.append(f'      <image:caption>{it["shortDesc"]}</image:caption>')
            xml_lines.append('    </image:image>')
        xml_lines.append('  </url>')

    # Individual photo pages with Google Image extensions
    xml_lines.append('  <!-- Dedicated Photo Pages -->')
    for it in all_items:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{BASE_URL}{it["slug"]}</loc>')
        xml_lines.append(f'    <lastmod>{today_iso}</lastmod>')
        xml_lines.append('    <changefreq>daily</changefreq>')
        xml_lines.append('    <priority>0.8</priority>')
        xml_lines.append('    <image:image>')
        xml_lines.append(f'      <image:loc>{BASE_URL}{it["img"]}.jpg</image:loc>')
        xml_lines.append(f'      <image:title>{it["titleHi"]} - {it["title"]}</image:title>')
        xml_lines.append(f'      <image:caption>{it["shortDesc"]}</image:caption>')
        xml_lines.append('    </image:image>')
        xml_lines.append('  </url>')

    # Spiritual Text Pages
    xml_lines.append('  <!-- Spiritual Text Pages (Chalisa & Aartis) -->')
    for sp in ['hanuman-chalisa.html', 'shiv-aarti.html', 'ganesh-aarti.html']:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{BASE_URL}{sp}</loc>')
        xml_lines.append(f'    <lastmod>{today_iso}</lastmod>')
        xml_lines.append('    <changefreq>weekly</changefreq>')
        xml_lines.append('    <priority>0.9</priority>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    return "\n".join(xml_lines)

# Main Generation Runner
print("Starting Ultra Site Generation...")

# 1. Generate Photo Pages
generated_files = {}
for it in ITEMS:
    content = generate_photo_page(it, ITEMS)
    generated_files[it["slug"]] = content
    print(f"Generated photo page: {it['slug']}")

# 2. Generate Category Pages
for cat in CATEGORIES:
    content = generate_category_page(cat, ITEMS)
    generated_files[cat["slug"]] = content
    print(f"Generated category page: {cat['slug']}")

# 3. Generate Index Page
generated_files["index.html"] = generate_index_page(ITEMS)
print("Generated index.html with Panchang & 108 Jap Mala widgets!")

# 4. Generate Sitemap & RSS
sitemap_content = generate_sitemap(ITEMS, CATEGORIES)
generated_files["sitemap.xml"] = sitemap_content
generated_files["feed.xml"] = generate_rss_feed(ITEMS)
print("Generated feed.xml for Google Discover!")
print(f"Generated sitemap.xml with dynamic lastmod & enriched image tags!")

# 5. Write all files to all target directories
for d in DIRS:
    os.makedirs(d, exist_ok=True)
    for fname, data in generated_files.items():
        fpath = os.path.join(d, fname)
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(data)
    print(f"Saved {len(generated_files)} files to {d}")

print("Ultra Site Generation COMPLETE!")
