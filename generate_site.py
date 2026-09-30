import os, sys, json
from datetime import datetime, date
import xml.sax.saxutils

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from generator_data import ITEMS as BASE_ITEMS, CATEGORIES, BASE_URL

DIRS = [SCRIPT_DIR]
for extra in [r"C:\Users\Bappa official\OneDrive\Desktop\HinduGodsGallery", r"C:\Users\Bappa official\HinduGodsGallery", r"c:\Users\Bappa official\.gemini\antigravity\playground\primordial-chromosphere"]:
    if os.path.exists(extra) and extra not in DIRS:
        DIRS.append(extra)

def xml_escape(val):
    if not val:
        return ""
    return xml.sax.saxutils.escape(str(val), {'"': "&quot;", "'": "&apos;"})

def resolve_image_assets(img_path):
    """
    Returns (img_jpg, img_webp, img_abs_url, sitemap_loc)
    Safely resolves image paths for both local assets and remote CDN URLs.
    Guarantees:
    - Never appends .jpg/.webp to query params of remote URLs
    - Never prepends BASE_URL to remote URLs
    - Escapes special characters for XML sitemaps
    """
    if not img_path:
        default_img = "images/cute_radha_krishna"
        return f"{default_img}.jpg", f"{default_img}.webp", f"{BASE_URL}{default_img}.jpg", f"{BASE_URL}{default_img}.jpg"
    
    if str(img_path).startswith("http://") or str(img_path).startswith("https://"):
        return img_path, img_path, img_path, xml_escape(img_path)
    
    clean = str(img_path).lstrip("/")
    base = os.path.splitext(clean)[0]
    jpg = f"{base}.jpg"
    webp = f"{base}.webp"
    abs_url = f"{BASE_URL}{base}.jpg"
    return jpg, webp, abs_url, abs_url

# ─────────────────────────────────────────────────────────────────────────────
# DEITY ARTICLE & MANTRA LIBRARY — Rich Content Engine for AdSense Compliance
# ─────────────────────────────────────────────────────────────────────────────

_DEITY_MANTRAS = {
    "shiva": (
        "ॐ नमः शिवाय ।\nमहादेव शम्भो भगवान त्रिपुरान्तक ॥",
        "हे शिव, हे महादेव, हे शम्भु — मैं आपको प्रणाम करता/करती हूँ। यह पंचाक्षरी मंत्र समस्त पापों का नाश करता है और मोक्ष का द्वार खोलता है।"
    ),
    "krishna": (
        "हरे कृष्ण हरे कृष्ण, कृष्ण कृष्ण हरे हरे ।\nहरे राम हरे राम, राम राम हरे हरे ॥",
        "यह महामंत्र कलियुग में सर्वश्रेष्ठ माना जाता है। इसके नित्य जप से मन की शांति, प्रेम और आत्मज्ञान प्राप्त होता है।"
    ),
    "hanuman": (
        "मनोजवं मारुततुल्यवेगं जितेन्द्रियं बुद्धिमतां वरिष्ठम् ।\nवातात्मजं वानरयूथमुख्यं श्रीरामदूतं शरणं प्रपद्ये ॥",
        "मन की गति से चलने वाले, वायु के समान वेगवान, इंद्रियजित, बुद्धिमानों में श्रेष्ठ श्री रामदूत हनुमान जी को मैं शरण लेता हूँ।"
    ),
    "lakshmi": (
        "ॐ श्रीं ह्रीं क्लीं त्रिभुवन महालक्ष्म्यै अस्माकं दारिद्र्यं नाशय प्रचुर धनं देहि देहि ।",
        "हे त्रिभुवन की महालक्ष्मी, हमारी दरिद्रता का नाश करें और प्रचुर धन-वैभव प्रदान करें। यह लक्ष्मी महामंत्र शुक्रवार के व्रत में विशेष फलदायी है।"
    ),
    "durga": (
        "ॐ दुं दुर्गायै नमः ।\nसर्वमंगलमांगल्ये शिवे सर्वार्थसाधिके ।\nशरण्ये त्र्यम्बके गौरि नारायणि नमोस्तुते ॥",
        "हे सर्वमंगलकारी, शिवस्वरूपा, सर्वार्थसाधिका माँ दुर्गा — आपको नमन। नवरात्रि में इस मंत्र का 108 बार जप करने से माँ की विशेष कृपा प्राप्त होती है।"
    ),
    "ganesha": (
        "ॐ गं गणपतये नमः ।\nवक्रतुण्ड महाकाय सूर्यकोटि समप्रभ ।\nनिर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा ॥",
        "हे वक्रतुण्ड, हे सूर्यकोटि के समान तेजस्वी गणपति — मेरे सभी कार्यों में सदा विघ्नों का नाश करें। प्रत्येक शुभ कार्य से पहले गणेश जी का यह मंत्र अनिवार्य माना जाता है।"
    ),
    "saraswati": (
        "ॐ ऐं सरस्वत्यै नमः ।\nया कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता ।\nया वीणावरदण्डमण्डितकरा या श्वेतपद्मासना ॥",
        "हे श्वेत वस्त्रधारिणी, वीणावादिनी, कमलासना माँ सरस्वती — आप विद्या, बुद्धि और कला की देवी हैं। परीक्षाओं से पहले इस मंत्र का जप विद्यार्थियों के लिए अत्यंत लाभकारी है।"
    ),
    "ram": (
        "श्री राम जय राम जय जय राम ।\nरामाय रामभद्राय रामचन्द्राय वेधसे ।\nरघुनाथाय नाथाय सीतायाः पतये नमः ॥",
        "हे राम, हे रामभद्र, हे रघुनाथ, सीता पति को नमन। यह मंत्र मर्यादा, सत्य और धर्म का प्रतीक है। रामनवमी और नित्य पाठ में यह मंत्र विशेष फलदायी है।"
    ),
    "cute": (
        "ॐ नमो भगवते वासुदेवाय नमः ।\nसर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः ।\nसर्वे भद्राणि पश्यन्तु मा कश्चिद् दुःखभाग्भवेत् ॥",
        "सभी प्राणी सुखी हों, सभी निरोगी हों, सभी मंगल देखें, कोई भी दुःख का भागी न हो। यह सर्वकल्याण मंत्र प्रात:काल जपने से दिन की शुभ शुरुआत होती है।"
    ),
    "festival": (
        "ॐ सर्वमंगलमांगल्ये शिवे सर्वार्थसाधिके ।\nशरण्ये त्र्यम्बके गौरि नारायणि नमोस्तुते ॥",
        "हे सर्वमंगलकारी, शिवस्वरूपा, सर्वार्थसाधिका — आपको नमन। त्योहारों के शुभ अवसर पर इस मंत्र का उच्चारण घर में सुख-समृद्धि और शांति लाता है।"
    ),
    "trending": (
        "ॐ नमो भगवते वासुदेवाय नमः ।\nसर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः ॥",
        "सभी सुखी हों, सभी निरोगी रहें, सभी का कल्याण हो। यह सरल किन्तु अत्यंत शक्तिशाली मंत्र जीवन में सकारात्मक ऊर्जा और ईश्वरीय कृपा का संचार करता है।"
    ),
}

_DEITY_ARTICLES = {
    "shiva": [
        "भगवान शिव — जिन्हें महादेव, आदियोगी, नीलकंठ और भोलेनाथ भी कहा जाता है — हिंदू त्रिदेवों में सबसे रहस्यमयी और शक्तिशाली देव हैं। शिव को 'देवों के देव' अर्थात् महादेव कहा जाता है। समुद्र मंथन के समय जब विष निकला, तो जगत की रक्षा के लिए महादेव ने वह विष स्वयं पी लिया और नीलकंठ कहलाए। वे सृष्टि के संहारक भी हैं और पालक भी, क्योंकि उनके बिना सृष्टि का चक्र संभव नहीं।",
        "भगवान शिव का स्वरूप अत्यंत भव्य और दिव्य है — माथे पर अर्धचंद्र, जटाओं से बहती गंगा, गले में सर्प, हाथ में त्रिशूल और डमरू, शरीर पर भस्म और बाघ की खाल। उनके नंदी बैल सत्य और धर्म के प्रतीक हैं। कैलाश पर्वत पर माँ पार्वती सहित विराजमान भगवान शिव ध्यान, वैराग्य और मोक्ष के परम प्रतीक हैं। पंचाक्षरी मंत्र 'ॐ नमः शिवाय' को सभी मंत्रों में सर्वश्रेष्ठ माना गया है।",
        "सोमवार का व्रत भगवान शिव को समर्पित है। महाशिवरात्रि वर्ष का सबसे बड़ा शिव पर्व है जब श्रद्धालु रात्रि जागरण कर शिवलिंग पर जल, दूध, बेलपत्र, धतूरा और भांग अर्पित करते हैं। बेलपत्र त्रिदेव — ब्रह्मा, विष्णु और महेश — के तीन रूपों का प्रतीक है। महादेव की आराधना से भय, क्रोध, अहंकार और नकारात्मकता का नाश होता है।",
        "इस 4K दिव्य छवि को अपने मोबाइल का वॉलपेपर, WhatsApp DP, या Good Morning Status बनाकर प्रतिदिन महादेव के दर्शन का लाभ उठाएं। भगवान शिव की इस पावन तस्वीर को परिवार और मित्रों के साथ शेयर करें और सबके जीवन में शिव कृपा का संचार करें।"
    ],
    "krishna": [
        "भगवान श्री कृष्ण — भगवान विष्णु के आठवें अवतार — हिंदू धर्म के सर्वाधिक प्रिय और पूजनीय देव हैं। उनका जन्म द्वापर युग में मथुरा में देवकी और वासुदेव के पुत्र के रूप में हुआ। बाल्यकाल गोकुल और वृंदावन में बीता जहाँ उन्होंने माखन चोरी, कालिया दमन और गोवर्धन उठाने जैसी अनेक लीलाएं कीं। राधा-कृष्ण का प्रेम इस ब्रह्मांड का सबसे पावन और अलौकिक प्रेम माना जाता है।",
        "श्रीमद् भगवद्गीता में भगवान कृष्ण ने अर्जुन को जो ज्ञान दिया वह आज भी करोड़ों लोगों के जीवन का आधार है। 'कर्म करो, फल की चिंता मत करो' — यह गीता का सार है। कृष्ण का मोरपंख मुकुट, पीताम्बर वस्त्र, वंशी की मधुर धुन और शंख (पांचजन्य) उनके दिव्य स्वरूप की पहचान हैं। उनकी आँखों में ब्रह्मांड का सौंदर्य समाया हुआ है।",
        "जन्माष्टमी — श्रीकृष्ण का जन्मदिन — पूरे भारत में अत्यंत धूमधाम से मनाया जाता है। मथुरा-वृंदावन में तो यह पर्व अद्वितीय होता है। दही-हांडी, झाँकियाँ, रासलीला और भजन-कीर्तन से वातावरण कृष्णमय हो जाता है। हरे कृष्ण महामंत्र के नित्य जप से मन की शांति, कर्म की शुद्धि और मोक्ष का मार्ग प्रशस्त होता है।",
        "इस सुंदर 4K कृष्ण छवि को अपने मोबाइल वॉलपेपर, लॉक स्क्रीन, WhatsApp Status या Facebook DP पर लगाकर प्रतिदिन श्रीकृष्ण के दर्शन का अलौकिक आनंद लें। अपने प्रियजनों के साथ यह पावन छवि शेयर करें और सबके जीवन में कृष्ण की बाँसुरी की मधुरता घोलें।"
    ],
    "hanuman": [
        "पवनपुत्र हनुमान — भगवान राम के परमभक्त, असीमित शक्ति के स्वामी और कलियुग के जागृत देव — हिंदू धर्म में सर्वाधिक लोकप्रिय देव हैं। वे भगवान शिव के रुद्रावतार माने जाते हैं। हनुमान जी अमर हैं — वे आज भी इस धरती पर विराजमान हैं। जहाँ भी रामकथा होती है, वहाँ हनुमान जी अदृश्य रूप में उपस्थित रहते हैं।",
        "हनुमान जी ने लंका जाकर माता सीता का पता लगाया, संजीवनी बूटी लाकर लक्ष्मण जी के प्राण बचाए, और समुद्र पर लंका पुल बनाने में अग्रणी भूमिका निभाई। उनकी पूँछ से लंका को जलाने की कथा आज भी बच्चों और बड़ों दोनों के मन में अदम्य साहस का संचार करती है। हनुमान चालीसा के 40 चौपाइयों में उनका पूर्ण यशोगान है जो हर भक्त के कंठ पर है।",
        "मंगलवार और शनिवार हनुमान जी के प्रिय दिन हैं। इन दिनों हनुमान मंदिर में जाकर सिंदूर चढ़ाना, चमेली के तेल का दीप जलाना और हनुमान चालीसा का पाठ करना अत्यंत फलदायी माना जाता है। हनुमान जी की आराधना से भय, भूत-प्रेत बाधा, ग्रह दोष और शत्रु पीड़ा का नाश होता है और शारीरिक-मानसिक शक्ति की प्राप्ति होती है।",
        "इस शक्तिशाली 4K हनुमान छवि को अपने फोन में रखें और प्रतिदिन दर्शन कर जय बजरंगबली का उद्घोष करें। WhatsApp Status पर शेयर करके अपने मित्रों और परिवार के जीवन में भी हनुमान जी का आशीर्वाद पहुँचाएं। बोलो — जय हनुमान! जय श्री राम!"
    ],
    "lakshmi": [
        "माँ लक्ष्मी — धन, वैभव, सौभाग्य और समृद्धि की अधिष्ठात्री देवी — भगवान विष्णु की अर्धांगिनी और सृष्टि की पालक शक्ति हैं। उनका जन्म समुद्र मंथन से हुआ था। वे श्वेत कमल पर विराजमान, चार हाथों में कमल, अभय मुद्रा और स्वर्ण कलश धारण करती हैं। सफेद हाथी उन पर जल की वर्षा करते हैं जो राजसी ऐश्वर्य का प्रतीक है।",
        "माँ लक्ष्मी के आठ रूप हैं — अष्टलक्ष्मी — जिनमें आदिलक्ष्मी, धनलक्ष्मी, धान्यलक्ष्मी, गजलक्ष्मी, संतानलक्ष्मी, वीरलक्ष्मी, विजयलक्ष्मी और विद्यालक्ष्मी शामिल हैं। प्रत्येक रूप जीवन के अलग पहलू को आशीर्वाद देता है। माँ लक्ष्मी स्थायी वास उसी घर में करती हैं जहाँ स्वच्छता, सत्य और परिश्रम हो।",
        "दीपावली माँ लक्ष्मी का सबसे बड़ा पर्व है। इस दिन घर की साफ-सफाई, दीपक जलाना और लक्ष्मी-गणेश पूजा करने से माँ घर में स्थायी रूप से निवास करती हैं। धनतेरस पर सोना, चाँदी या नई वस्तु खरीदना अत्यंत शुभ माना जाता है। शुक्रवार का दिन माँ लक्ष्मी की उपासना के लिए विशेष है — इस दिन श्री सूक्त का पाठ घर में धन-वर्षा करता है।",
        "इस दिव्य 4K लक्ष्मी माँ की छवि को अपने घर में, दुकान में, ऑफिस में या मोबाइल वॉलपेपर में लगाएं और माँ के आशीर्वाद से जीवन में सुख-समृद्धि की बाढ़ आने दें। व्हाट्सएप स्टेटस पर शेयर करके सबके जीवन में माँ लक्ष्मी की कृपा का संचार करें। जय माँ लक्ष्मी!"
    ],
    "durga": [
        "माँ दुर्गा — आद्यशक्ति, महाशक्ति, जगदम्बा — समस्त देवताओं की संयुक्त शक्ति से प्रकट हुई महाशक्ति हैं। जब महिषासुर के अत्याचारों से तीनों लोक त्राहि-त्राहि कर उठे, तब सभी देवताओं ने अपनी-अपनी शक्तियाँ एकत्रित कर माँ दुर्गा का अवतरण किया। सिंह पर सवार, अठारह भुजाओं में विभिन्न अस्त्र-शस्त्र धारण किए माँ दुर्गा असुरों का विनाश करती हैं।",
        "माँ दुर्गा के नौ रूप — नवदुर्गा — नवरात्रि के नौ दिनों में पूजे जाते हैं। शैलपुत्री, ब्रह्मचारिणी, चंद्रघंटा, कूष्माण्डा, स्कन्दमाता, कात्यायनी, कालरात्रि, महागौरी और सिद्धिदात्री — ये नौ रूप क्रमशः शक्ति, तप, संगीत, सृजन, ममता, शौर्य, काल पर विजय, पवित्रता और सिद्धि के प्रतीक हैं। इन नौ रूपों की आराधना जीवन को पूर्णता देती है।",
        "नवरात्रि में माँ दुर्गा की विशेष पूजा, जागरण, डांडिया और दुर्गा सप्तशती का पाठ होता है। दुर्गा सप्तशती में 700 श्लोक हैं जो माँ की महिमा, युद्ध-कथा और वरदान का वर्णन करते हैं। माँ दुर्गा को लाल रंग, लाल फूल और विशेषकर लाल चुनरी प्रिय है। नवरात्रि में व्रत रखकर माँ की उपासना से सभी मनोकामनाएं पूर्ण होती हैं।",
        "इस शक्तिशाली 4K माँ दुर्गा छवि को नवरात्रि और प्रतिदिन के दर्शन के लिए अपने मोबाइल में रखें। दुर्गा माँ की यह भव्य तस्वीर WhatsApp Status, Facebook और Instagram पर शेयर करके सबको माँ के दर्शन का लाभ दें। जय माँ दुर्गा! जय माँ भवानी!"
    ],
    "ganesha": [
        "भगवान गणेश — विघ्नहर्ता, गणपति, लम्बोदर, एकदंत — हिंदू धर्म में सर्वप्रथम पूजनीय देव हैं। कोई भी शुभ कार्य — विवाह, गृह-प्रवेश, व्यापार शुरू करना, यात्रा — गणेश पूजन के बिना अधूरा माना जाता है। हाथी जैसे सिर वाले गणेश जी ज्ञान, बुद्धि और विवेक के देव हैं। उनका मूषक (चूहा) वाहन यह बताता है कि बुद्धि छोटे से छोटे प्राणी में भी रह सकती है।",
        "गणेश जी का जन्म माँ पार्वती ने अपने शरीर के उबटन से किया था। पिता शिव के साथ हुई भ्रांति में उनका मस्तक कट गया, किन्तु हाथी का मस्तक लगाकर उन्हें पुनर्जीवित किया गया। देवता बोले — 'परशु ले लो, यह हाथी-मस्तक ब्रह्मांड की बुद्धि का प्रतीक है।' गणेश जी ने महाभारत को श्री वेद व्यास जी से सुनते हुए स्वयं लिखा — वे विद्या और लेखन के देव भी हैं।",
        "गणेश चतुर्थी भाद्रपद शुक्ल चतुर्थी को मनाई जाती है — महाराष्ट्र में 10 दिनों का यह महापर्व देश का सबसे बड़ा सार्वजनिक उत्सव है। मोदक गणेश जी का प्रिय भोग है। बुधवार का दिन गणेश जी को समर्पित है। 'ॐ गं गणपतये नमः' मंत्र का 108 बार जप विद्यार्थियों की बुद्धि, व्यापारियों के कार्य और साधकों की सिद्धि के लिए उत्तम माना जाता है।",
        "इस सुंदर 4K गणेश जी की छवि को अपने घर, ऑफिस और मोबाइल में स्थापित करें। नई शुरुआत, परीक्षा, साक्षात्कार या किसी भी महत्वपूर्ण कार्य से पहले गणेश जी के इस पावन स्वरूप के दर्शन करें। WhatsApp Status पर शेयर करके सबको गणपति जी का आशीर्वाद पहुँचाएं। गणपति बप्पा मोरया!"
    ],
    "saraswati": [
        "माँ सरस्वती — वागीश्वरी, वीणावादिनी, ब्रह्माणी, शारदा — ज्ञान, विद्या, कला, संगीत और वाणी की देवी हैं। श्वेत वस्त्र धारण किए, श्वेत कमल पर विराजमान, वीणा बजाती माँ सरस्वती की छवि मन को असीम शांति देती है। उनका वाहन हंस विवेक और ज्ञान का प्रतीक है — हंस दूध और पानी को अलग करके सत्य को असत्य से अलग कर सकता है।",
        "माँ सरस्वती की आराधना विशेषकर छात्र, शिक्षक, कवि, संगीतकार, कलाकार और लेखक करते हैं। बसंत पंचमी माँ सरस्वती का जन्मदिन है। इस दिन पीले वस्त्र पहनकर, पीले फूल चढ़ाकर और सरस्वती वंदना गाकर माँ की आराधना की जाती है। स्कूल-कॉलेज में सरस्वती पूजा होती है और किताबें-कलम माँ के चरणों में रखी जाती हैं।",
        "माँ सरस्वती की पूजा से वाणी में मधुरता, बुद्धि में तीक्ष्णता और स्मरण शक्ति में वृद्धि होती है। 'ॐ ऐं सरस्वत्यै नमः' बीज मंत्र का नित्य जप करने से कला, संगीत और शिक्षा के क्षेत्र में सफलता मिलती है। परीक्षा से पूर्व माँ सरस्वती की स्तुति करने से मन एकाग्र होता है और ज्ञान प्रकाशित होता है। माँ सरस्वती सभी विद्यार्थियों की रक्षिका हैं।",
        "इस दिव्य 4K माँ सरस्वती छवि को विद्यार्थी अपनी पढ़ाई की मेज के सामने रखें और परीक्षा में उत्तीर्णता का आशीर्वाद प्राप्त करें। शिक्षक दिवस, बसंत पंचमी और दैनिक पूजा के लिए यह छवि अत्यंत शुभ है। सरस्वती माँ की यह तस्वीर अपने मित्रों, बच्चों और परिवार के साथ शेयर करें। जय माँ सरस्वती!"
    ],
    "ram": [
        "भगवान श्री राम — मर्यादा पुरुषोत्तम, दशरथनंदन, रघुकुल तिलक — भगवान विष्णु के सातवें अवतार हैं। अयोध्या में जन्मे श्री राम का जीवन मर्यादा, सत्य, प्रेम और कर्तव्य का आदर्श उदाहरण है। पिता के वचन की रक्षा के लिए 14 वर्ष का वनवास स्वीकार करना, माता-पिता की सेवा, पत्नी सीता के प्रति एकनिष्ठ प्रेम — ये सब श्री राम को मानव इतिहास का सर्वश्रेष्ठ पुरुष बनाते हैं।",
        "श्री राम का धनुष — शार्ङ्ग — और बाण अजेय थे। रावण के अत्याचारों से पीड़ित माता सीता को लंका से मुक्त कराने के लिए श्री राम ने वानर सेना के साथ मिलकर समुद्र पर सेतु बनाया और लंका पर विजय प्राप्त की। रावण वध के पश्चात् श्री राम का अयोध्या वापसी पर भव्य अभिनंदन हुआ — यही दीपावली का मूल उत्सव है। श्री राम का राज्य 'रामराज्य' आज भी आदर्श शासन का प्रतीक है।",
        "रामनवमी — श्री राम का जन्मदिन — चैत्र शुक्ल नवमी को मनाया जाता है। इस दिन भगवान राम की पूजा, रामचरितमानस का पाठ और भजन-कीर्तन होते हैं। 'जय श्री राम' — यह दो शब्द करोड़ों हिंदुओं के जीवन का मूलमंत्र है। राम नाम का जप करने से आत्मा को शांति, मन को स्थिरता और जीवन को दिशा मिलती है।",
        "इस भव्य 4K श्री राम छवि को अपने घर में, मंदिर में, मोबाइल वॉलपेपर में रखें और प्रतिदिन प्रातः दर्शन करके राम नाम का जप करें। रामनवमी, दीपावली और नित्य सुबह-शाम के लिए यह छवि अत्यंत शुभ है। अपने परिवार और मित्रों के साथ इस पावन छवि को शेयर करें। जय श्री राम!"
    ],
    "cute": [
        "हिंदू देवी-देवताओं के इस मनमोहक बाल रूप (Cute Divine Form) की कल्पना आधुनिक भक्तों के मन में एक नई भावना जगाती है — भक्ति के साथ-साथ वात्सल्य और प्रेम। जब हम भगवान को एक नन्हे, मासूम शिशु के रूप में देखते हैं, तो हृदय में माँ या पिता जैसा भाव उत्पन्न होता है। यही वात्सल्य भक्ति हिंदू अध्यात्म की एक अनूठी परंपरा है।",
        "बाल लीलाएँ — जैसे बाल कृष्ण की माखन चोरी, बाल हनुमान का सूर्य को फल समझकर छलांग लगाना, बाल गणेश का चूहे पर सवार होकर मिठाई खाना — ये सभी कथाएँ बच्चों और बड़ों दोनों के हृदय को छू लेती हैं। इन प्रेमपूर्ण कथाओं में संदेश यह है कि ईश्वर केवल भव्य और गंभीर नहीं, वे बाल सुलभ चंचलता में भी हैं।",
        "इस प्रकार की Cute Divine Art भारत में अत्यंत लोकप्रिय है। WhatsApp Status, Instagram Reels, Facebook Posts — हर जगह इन मनमोहक भगवान की तस्वीरें धड़ल्ले से शेयर होती हैं। जो बच्चे पारंपरिक पूजा-पाठ से दूर थे, वे इन Cute God images के माध्यम से भगवान से जुड़ रहे हैं। यह डिजिटल भक्ति की एक नई और सुंदर परंपरा है।",
        "इस अत्यंत सुंदर 4K Cute God वॉलपेपर को अपने मोबाइल का होम स्क्रीन, लॉक स्क्रीन बनाएं। बच्चों के कमरे में, स्टडी टेबल पर या रसोई में लगाएं — हर जगह यह छवि एक दिव्य उपस्थिति का अनुभव कराएगी। अपने मित्रों और परिवार के साथ शेयर करके उनके दिन को भी दिव्य बनाएं।"
    ],
    "festival": [
        "हिंदू त्योहार — दीपावली, होली, नवरात्रि, जन्माष्टमी, गणेश चतुर्थी, रामनवमी — केवल धार्मिक आयोजन नहीं हैं, ये भारतीय संस्कृति की आत्मा हैं। हर त्योहार एक विशेष संदेश लेकर आता है — दीपावली अंधकार पर प्रकाश की, होली वैर पर प्रेम की, नवरात्रि दुर्बलता पर शक्ति की विजय का उद्घोष है। इन पर्वों में सजावट, पूजा, भोजन और मिलन का एक अनूठा समन्वय होता है।",
        "भारत के विभिन्न राज्यों में एक ही त्योहार अलग-अलग तरीकों से मनाया जाता है — नवरात्रि में गुजरात का गरबा, महाराष्ट्र की गणेश पूजा, बंगाल की दुर्गा पूजा, तमिलनाडु का पोंगल, केरल का ओणम — यह विविधता में एकता हिंदू परंपरा की विशेषता है। हर पर्व से पहले घर की सजावट, पकवान बनाना और नए वस्त्र पहनने की परंपरा है।",
        "त्योहारों का मनोवैज्ञानिक महत्व भी अत्यंत गहरा है। ये एकाकीपन दूर करते हैं, परिवार और समुदाय को जोड़ते हैं, और जीवन में उत्साह, आनंद और सकारात्मकता का संचार करते हैं। वैज्ञानिक शोध भी बताते हैं कि त्योहारों के समय मानवीय संबंध मजबूत होते हैं और मानसिक स्वास्थ्य बेहतर रहता है।",
        "इस विशेष Festival 4K छवि को त्योहार की शुभकामनाओं के साथ WhatsApp Status, Instagram Stories और Facebook पर शेयर करें। अपने परिवार और मित्रों को इस पावन छवि के माध्यम से त्योहार की बधाई दें और उनके घर में उत्सव का उजाला बिखेरें। शुभ पर्व की शुभकामनाएं!"
    ],
    "trending": [
        "हिंदू भगवान की 4K तस्वीरें आज सोशल मीडिया पर सर्वाधिक शेयर होने वाली कंटेंट में से एक हैं। WhatsApp Status, Instagram Reels, Facebook Posts — हर प्लेटफ़ॉर्म पर दैनिक भक्ति सामग्री की माँग लाखों की संख्या में है। यह Trending Hindu God Wallpaper उसी माँग को पूरा करती है — HD से 4K Ultra तक, हर रिज़ॉल्यूशन में उपलब्ध।",
        "आधुनिक भारत में डिजिटल भक्ति एक नई परंपरा बन चुकी है। सुबह उठकर WhatsApp पर भगवान का Good Morning Status भेजना, इंस्टाग्राम पर मंत्र शेयर करना, यूट्यूब पर भजन सुनना — ये सब डिजिटल भारत की नई पूजा पद्धति है। इस परंपरा में 4K Divine Images की भूमिका केंद्रीय है। हर सुबह नई, ताज़ी और सुंदर भगवान की तस्वीर मिलना आत्मा को प्रसन्न करता है।",
        "इस वेबसाइट पर प्रतिदिन नई 4K Hindu God Images अपलोड होती हैं — Shiva, Krishna, Hanuman, Lakshmi, Durga, Ganesha और अन्य सभी देवताओं के Cute, Trending और Festival Special रूपों में। AI-generated लेकिन भारतीय कलाकारों की सुरुचि से क्यूरेट की गई ये तस्वीरें आपके मन, घर और डिजिटल जीवन को पवित्र बनाती हैं।",
        "इस Trending 4K God Wallpaper को अभी Download करें और अपने सभी सोशल मीडिया प्लेटफ़ॉर्म पर शेयर करें। Bookmark करें यह वेबसाइट — क्योंकि यहाँ प्रतिदिन नए दर्शन का लाभ मिलता है। अपने सभी WhatsApp Groups में यह पावन तस्वीर शेयर करके हर किसी के दिन की दिव्य शुरुआत करें।"
    ],
}

def _get_deity_mantra(category):
    """Returns (mantra, mantraMeaning) tuple for a given deity category."""
    cat_key = category.lower().strip()
    for key in _DEITY_MANTRAS:
        if key in cat_key or cat_key in key:
            return _DEITY_MANTRAS[key]
    return _DEITY_MANTRAS["cute"]

def _build_rich_article(titleHi, title_en, category, desc_hi, desc_en, ai_prompt, item_date, style_tag):
    """Builds a 400+ word rich article for a deity item from images_data.json."""
    cat_key = category.lower().strip()
    deity_paras = None
    for key in _DEITY_ARTICLES:
        if key in cat_key or cat_key in key:
            deity_paras = _DEITY_ARTICLES[key]
            break
    if not deity_paras:
        deity_paras = _DEITY_ARTICLES["cute"]

    # Build personalized intro from description
    intro_lines = []
    if desc_hi:
        intro_lines.append(f"<strong>{titleHi}</strong> — {desc_hi}")
    elif desc_en:
        intro_lines.append(f"<strong>{titleHi}</strong> — {desc_en}")
    else:
        intro_lines.append(f"<strong>{titleHi}</strong> का यह अलौकिक 4K स्वरूप दैनिक दर्शन और WhatsApp Status के लिए विशेष रूप से तैयार किया गया है।")

    if style_tag:
        intro_lines.append(f"इस छवि का कलात्मक शैली: <em>{style_tag}</em> — जो इसे विशेष रूप से आकर्षक और साझा करने योग्य बनाती है।")

    if item_date:
        try:
            dt = datetime.strptime(item_date, "%Y-%m-%d")
            intro_lines.append(f"यह {dt.strftime('%d %B %Y')} को हमारी दैनिक दर्शन श्रृंखला में प्रकाशित की गई थी।")
        except Exception:
            pass

    article_parts = ["<p>" + " ".join(intro_lines) + "</p>"]
    for para in deity_paras:
        article_parts.append(f"<p>{para}</p>")

    return "\n".join(article_parts)

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
                    desc_hi = entry.get("description_hi") or ""
                    desc_en = entry.get("description_en") or ""
                    ai_prompt = entry.get("ai_prompt") or ""
                    item_date = entry.get("date", "")
                    style_tag = entry.get("style", "")

                    mantra, mantraMeaning = _get_deity_mantra(cat)
                    article = _build_rich_article(titleHi, title, cat, desc_hi, desc_en, ai_prompt, item_date, style_tag)
                    short_desc = desc_hi or desc_en or f"{titleHi} — भगवान का पावन और अलौकिक 4K स्वरूप। यह दिव्य छवि आपके मन को शांति और भक्ति की अनुभूति कराएगी।"

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
                        "shortDesc": short_desc,
                        "mantra": mantra,
                        "mantraMeaning": mantraMeaning,
                        "article": article,
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
        <a href="about.html">हमारे बारे में</a> |
        <a href="contact.html">संपर्क करें</a> |
        <a href="privacy-policy.html">Privacy Policy</a> |
        <a href="terms.html">नियम व शर्तें</a> |
        <a href="disclaimer.html">अस्वीकरण</a> |
        <a href="sitemap.xml">Sitemap (XML)</a> |
        <a href="feed.xml">RSS Feed</a>
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
        
    img_jpg, img_webp, img_abs_url, sitemap_loc = resolve_image_assets(item["img"])
    page_url = BASE_URL + item["slug"]

    if str(item["img"]).startswith("http"):
        picture_html = f'<img src="{img_jpg}" alt="{item["titleHi"]} - {item["title"]} 4K Free Download" width="1024" height="1365" style="cursor:zoom-in;" onclick="openLightbox(\'{img_jpg}\')">'
    else:
        picture_html = f'''<picture>
                <source srcset="{img_webp}" type="image/webp">
                <img src="{img_jpg}" alt="{item["titleHi"]} - {item["title"]} 4K Free Download" width="1024" height="1365" style="cursor:zoom-in;" onclick="openLightbox(\'{img_jpg}\')">
            </picture>'''

    related_html = ""
    for r in related:
        r_jpg, r_webp, _, _ = resolve_image_assets(r["img"])
        if str(r["img"]).startswith("http"):
            r_pic = f'<img src="{r_jpg}" alt="{r["title"]}" loading="lazy" width="400" height="533">'
        else:
            r_pic = f'<picture><source srcset="{r_webp}" type="image/webp"><img src="{r_jpg}" alt="{r["title"]}" loading="lazy" width="400" height="533"></picture>'
        related_html += f"""
        <div class="card">
            <a class="card-img-link" href="{r['slug']}">
                <span class="badge">{r['badge']}</span>
                {r_pic}
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
        }},
        {{
          "@type": "FAQPage",
          "mainEntity": [
            {{
              "@type": "Question",
              "name": "इस 4K वॉलपेपर को कैसे डाउनलोड करें?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Download 4K Image बटन पर क्लिक करें। छवि तुरंत आपके डिवाइस में मुफ्त सेव हो जाएगी।"
              }}
            }},
            {{
              "@type": "Question",
              "name": "WhatsApp Status पर कैसे लगाएं?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "1-Click WhatsApp Status बटन दबाएं। यह स्वचालित रूप से तस्वीर के साथ पावन मंत्र WhatsApp पर शेयर करेगा।"
              }}
            }},
            {{
              "@type": "Question",
              "name": "यह इमेज किस रिज़ॉल्यूशन में है?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "यह छवि 4K Ultra HD (1024x1365) रिज़ॉल्यूशन में उपलब्ध है — मोबाइल और कंप्यूटर दोनों के लिए अनुकूलित है।"
              }}
            }},
            {{
              "@type": "Question",
              "name": "क्या ये तस्वीरें बिल्कुल मुफ्त हैं?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "हाँ, सभी तस्वीरें 100% मुफ्त हैं — डाउनलोड करें, WhatsApp स्टेटस लगाएं, वॉलपेपर बनाएं।"
              }}
            }}
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
            {picture_html}

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
                <h3 style="color:var(--maroon); margin-bottom:10px; font-family:'Rozha One', serif;">🙏 धार्मिक महत्व एवं आध्यात्मिक विवरण</h3>
                <div class="article-content">
                {item['article']}
                </div>

                <div class="faq-box" style="margin-top:24px; border-top:2px solid var(--saffron); padding-top:16px;">
                    <h3 style="color:var(--maroon); margin-bottom:14px; font-family:'Rozha One', serif;">❓ अक्सर पूछे जाने वाले प्रश्न (FAQ)</h3>
                    <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                        <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">📥 इस 4K वॉलपेपर को कैसे डाउनलोड करें?</summary>
                        <p style="margin-top:8px; color:#555;">ऊपर दिए <strong>📥 Download 4K Image</strong> बटन पर क्लिक करें। छवि तुरंत आपके डिवाइस में सेव हो जाएगी — मोबाइल और कंप्यूटर दोनों पर काम करता है।</p>
                    </details>
                    <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                        <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">📱 WhatsApp Status पर कैसे लगाएं?</summary>
                        <p style="margin-top:8px; color:#555;"><strong>📱 1-Click WhatsApp Status</strong> बटन दबाएं। यह स्वचालित रूप से {item['titleHi']} की तस्वीर के साथ पावन मंत्र WhatsApp पर शेयर करेगा।</p>
                    </details>
                    <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                        <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">🖼️ यह इमेज किस रिज़ॉल्यूशन में है?</summary>
                        <p style="margin-top:8px; color:#555;">यह छवि 4K Ultra HD (1024×1365) रिज़ॉल्यूशन में उपलब्ध है — मोबाइल, टैबलेट और कंप्यूटर सभी पर crystal-clear दिखती है।</p>
                    </details>
                    <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                        <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">🕐 नई तस्वीरें कब अपलोड होती हैं?</summary>
                        <p style="margin-top:8px; color:#555;">इस वेबसाइट पर प्रतिदिन 10 नई 4K Hindu God Images अपलोड होती हैं। बुकमार्क करें और प्रतिदिन ताज़े दर्शन का लाभ उठाएं।</p>
                    </details>
                    <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                        <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">💰 क्या ये तस्वीरें बिल्कुल मुफ्त हैं?</summary>
                        <p style="margin-top:8px; color:#555;">हाँ! सभी तस्वीरें 100% मुफ्त हैं — डाउनलोड करें, WhatsApp पर शेयर करें, वॉलपेपर लगाएं — सब कुछ निःशुल्क।</p>
                    </details>
                </div>

                <h4 style="color:var(--maroon); margin-top:20px; margin-bottom:8px;">🔖 संबंधित सर्च कीवर्ड्स (Tags):</h4>
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
        it_jpg, it_webp, _, _ = resolve_image_assets(it["img"])
        if str(it["img"]).startswith("http"):
            card_pic = f'<img src="{it_jpg}" alt="{it["title"]}" loading="lazy" width="400" height="533">'
        else:
            card_pic = f'<picture><source srcset="{it_webp}" type="image/webp"><img src="{it_jpg}" alt="{it["title"]}" loading="lazy" width="400" height="533"></picture>'
        cards_html += f"""
        <div class="card">
            <a class="card-img-link" href="{it['slug']}">
                <span class="badge">{it['badge']}</span>
                {card_pic}
            </a>
            <div class="card-body">
                <h3><a href="{it['slug']}">{it['titleHi']}</a></h3>
                <p>{it['shortDesc']}</p>
                <div class="card-actions">
                    <a href="{it['slug']}" class="btn-action btn-view">View 4K</a>
                    <button onclick="shareCustomWhatsApp('{it['titleHi']}', '{BASE_URL}{it['slug']}', '{it.get('mantra','')[:50]}...')" class="btn-action btn-wa">WA</button>
                    <a href="{it_jpg}" download class="btn-action btn-dl">Download</a>
                </div>
            </div>
        </div>
        """

    cat_url = BASE_URL + cat["slug"]

    # Retrieve rich deity editorial paragraphs
    cid = cat["id"]
    paras = _DEITY_ARTICLES.get(cid, _DEITY_ARTICLES.get("cute", []))
    editorial_p_html = "".join([f"<p style='font-size:1.02rem; line-height:1.8; color:#333; margin-bottom:14px;'>{p}</p>" for p in paras])

    # Retrieve sacred mantra for category
    mantra, meaning = _get_deity_mantra(cid)

    html = f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>{cat['nameHi']} 4K Wallpaper &amp; Photos | {cat['name']} Free Download</title>
    <meta name="description" content="{cat['desc']} Free 4K Ultra HD Wallpapers, Mantras &amp; WhatsApp Status photos download. {len(cat_items)}+ divine images.">
    <link rel="canonical" href="{cat_url}">
    
    <meta property="og:title" content="{cat['nameHi']} | 4K Hindu Gods Gallery">
    <meta property="og:description" content="{cat['desc']}">
    <meta property="og:url" content="{cat_url}">
    <meta property="og:type" content="website">
    
    <!-- Google Schema.org CollectionPage, BreadcrumbList, and FAQPage -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "CollectionPage",
          "name": "{cat['nameHi']} - {cat['name']}",
          "description": "{cat['desc']}",
          "url": "{cat_url}"
        }},
        {{
          "@type": "BreadcrumbList",
          "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE_URL}" }},
            {{ "@type": "ListItem", "position": 2, "name": "{cat['nameHi']}", "item": "{cat_url}" }}
          ]
        }},
        {{
          "@type": "FAQPage",
          "mainEntity": [
            {{
              "@type": "Question",
              "name": "इस श्रेणी में कुल कितने {cat['nameHi']} 4K वॉलपेपर हैं?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "इस श्रेणी में वर्तमान में {len(cat_items)}+ उच्च रिज़ॉल्यूशन 4K वॉलपेपर उपलब्ध हैं, जो प्रतिदिन नए जोड़े जाते हैं।"
              }}
            }},
            {{
              "@type": "Question",
              "name": "क्या ये वॉलपेपर WhatsApp Status और Instagram Stories के लिए सही हैं?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "हाँ, सभी छवियां 1024x1365 (3:4) लंबवत अनुपात में हैं, जो मोबाइल स्क्रीन, WhatsApp DP, और Status के लिए सटीक हैं।"
              }}
            }},
            {{
              "@type": "Question",
              "name": "क्या {cat['nameHi']} के चित्र बिल्कुल मुफ्त डाउनलोड किए जा सकते हैं?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "हाँ, सभी तस्वीरें 100% मुफ्त हैं। आप बिना किसी शुल्क के डाउनलोड कर सकते हैं।"
              }}
            }}
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
    <p>{cat['nameHi']} — Daily Cute 4K Wallpaper &amp; WhatsApp Status</p>
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
    <a href="category-durga.html" class="nav-link { 'active' if cat['id'] == 'durga' else '' }">🦁 Durga</a>
    <a href="category-lakshmi.html" class="nav-link { 'active' if cat['id'] == 'lakshmi' else '' }">🪷 Lakshmi</a>
    <a href="category-ram.html" class="nav-link { 'active' if cat['id'] == 'ram' else '' }">🏹 Ram</a>
    <a href="category-saraswati.html" class="nav-link { 'active' if cat['id'] == 'saraswati' else '' }">🪕 Saraswati</a>
    <a href="hanuman-chalisa.html" class="nav-link" style="color:var(--saffron);">🚩 चालीसा</a>
</nav>

<div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>{cat['nameHi']}</span>
    </nav>

    <div style="text-align: center; margin: 16px 0 28px;">
        <h1 style="font-family:'Rozha One', serif; color:var(--maroon); font-size:2.3rem; margin-bottom:8px;">{cat['nameHi']}</h1>
        <p style="color:#555; max-width:850px; margin:0 auto 14px; font-size:1.05rem;">{cat['desc']}</p>
        <div style="display:inline-block; background:rgba(255,153,0,0.12); color:var(--maroon); border:1px solid var(--saffron); padding:6px 18px; border-radius:20px; font-weight:700; font-size:0.9rem;">
            🌸 कुल {len(cat_items)} पावन दर्शन उपलब्ध
        </div>
    </div>

    <!-- GALLERY GRID -->
    <div class="gallery-grid">
        {cards_html}
    </div>

    <!-- RICH DEVOTIONAL EDITORIAL SECTION (Pillar Content for Google SEO & AdSense) -->
    <div class="article-box" style="margin-top:40px; background:#fff; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,0.06); border-top:4px solid var(--saffron);">
        <h2 style="color:var(--maroon); font-family:'Rozha One', serif; font-size:1.8rem; margin-bottom:16px;">
            🙏 {cat['nameHi']} — धार्मिक महत्व, महात्म्य एवं दर्शन फल
        </h2>
        {editorial_p_html}

        <!-- SACRED MANTRA BOX -->
        <div class="mantra-box" style="margin:24px 0; background:linear-gradient(135deg, rgba(255,248,240,0.9), rgba(255,243,224,0.9)); border:2px solid var(--gold); border-radius:14px; padding:20px;">
            <div class="mantra-heading" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-family:'Rozha One', serif; color:var(--maroon); font-size:1.15rem;">🌸 पावन मंत्र एवं ध्यान श्लोक</span>
                <button class="btn-copy-mantra" onclick="copyText(`{mantra}`, 'मंत्र कॉपी हो गया! 🙏')" style="background:var(--maroon); color:#fff; border:none; padding:6px 14px; border-radius:15px; cursor:pointer; font-size:0.8rem; font-weight:600;">📋 Copy Mantra</button>
            </div>
            <div class="mantra-text" style="font-family:'Rozha One', serif; font-size:1.2rem; color:var(--maroon); text-align:center; line-height:1.9; white-space:pre-line; margin-bottom:10px;">{mantra}</div>
            <div class="mantra-meaning" style="font-size:0.95rem; color:#4E342E; text-align:center; line-height:1.6;"><strong>अर्थ:</strong> {meaning}</div>
        </div>

        <!-- CATEGORY FAQ ACCORDION -->
        <div class="faq-box" style="margin-top:28px; border-top:2px solid rgba(255,119,0,0.25); padding-top:20px;">
            <h3 style="color:var(--maroon); margin-bottom:14px; font-family:'Rozha One', serif;">❓ अक्सर पूछे जाने वाले प्रश्न ({cat['nameHi']} FAQ)</h3>
            <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">📥 इस श्रेणी की तस्वीरें कैसे डाउनलोड करें?</summary>
                <p style="margin-top:8px; color:#555;">किसी भी तस्वीर के नीचे दिए गए <strong>Download</strong> बटन पर क्लिक करें अथवा फोटो पेज पर जाकर <strong>Download 4K Image</strong> बटन दबाएं।</p>
            </details>
            <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">📱 WhatsApp Status पर शेयर करने का तरीका?</summary>
                <p style="margin-top:8px; color:#555;">हर कार्ड पर <strong>WA</strong> बटन उपलब्ध है। उस पर क्लिक करते ही तस्वीर और मंत्र WhatsApp Status के लिए तैयार हो जाएंगे।</p>
            </details>
            <details style="margin-bottom:10px; background:rgba(255,153,0,0.07); border-radius:8px; padding:10px 14px;">
                <summary style="font-weight:700; color:var(--maroon); cursor:pointer;">🖼️ क्या ये तस्वीरें प्रिंट या फ्रेम करवाने योग्य हैं?</summary>
                <p style="margin-top:8px; color:#555;">हाँ, सभी छवियां 4K Ultra HD (1024x1365) रिज़ॉल्यूशन में हैं। आप इन्हें आसानी से घर के मंदिर अथवा स्टडी टेबल हेतु प्रिंट करा सकते हैं।</p>
            </details>
        </div>
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
            it_jpg, it_webp, _, _ = resolve_image_assets(it["img"])
            if str(it["img"]).startswith("http"):
                card_pic = f'<img src="{it_jpg}" alt="{it["titleHi"]} - {it["title"]}" loading="lazy" width="400" height="533">'
            else:
                card_pic = f'<picture><source srcset="{it_webp}" type="image/webp"><img src="{it_jpg}" alt="{it["titleHi"]} - {it["title"]}" loading="lazy" width="400" height="533"></picture>'
            h += f"""
            <div class="card" data-god="{it.get('god', '')}" data-cat="{it.get('category', '')}" data-search="{it['title'].lower()} {it['titleHi']} {' '.join(it['tags'])}">
                <a class="card-img-link" href="{it['slug']}">
                    <span class="badge">{it['badge']}</span>
                    {card_pic}
                </a>
                <div class="card-body">
                    <h3><a href="{it['slug']}">{it['titleHi']}</a></h3>
                    <p>{it['shortDesc']}</p>
                    <div class="card-actions">
                        <a href="{it['slug']}" class="btn-action btn-view">View 4K</a>
                        <button onclick="shareCustomWhatsApp('{it['titleHi']}', '{BASE_URL}{it['slug']}', '{it.get('mantra','')[:50]}...')" class="btn-action btn-wa">WA</button>
                        <a href="{it_jpg}" download class="btn-action btn-dl">Download</a>
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
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 भगवान खोजें: शिव, कृष्ण, हनुमान, गणेश, दुर्गा, राम, सरस्वती, बाल गोपाल..." onkeyup="filterCards()">
        <div id="searchCountDisplay" style="text-align:center; font-size:0.85rem; color:#780016; font-weight:600; margin-top:8px;">{len(all_items)}+ पावन 4K दर्शन उपलब्ध</div>
    </div>

    <!-- QUICK CATEGORY PILLS (LIVE INSTANT FILTER + DIRECT ACCESS) -->
    <div class="category-pills">
        <button onclick="filterByDeity('all', this)" class="cat-pill active">🌟 सभी दर्शन ({len(all_items)})</button>
        <button onclick="filterByDeity('cute', this)" class="cat-pill">🧸 क्यूट बाल रूप ({len(cute_items)})</button>
        <button onclick="filterByDeity('trending', this)" class="cat-pill">🔥 ट्रेंडिंग 4K ({len(trending_items)})</button>
        <button onclick="filterByDeity('shiva', this)" class="cat-pill">🔱 भगवान शिव</button>
        <button onclick="filterByDeity('krishna', this)" class="cat-pill">🦚 श्री कृष्ण</button>
        <button onclick="filterByDeity('ganesha', this)" class="cat-pill">🐘 गणपति बप्पा</button>
        <button onclick="filterByDeity('hanuman', this)" class="cat-pill">🚩 संकटमोचन हनुमान</button>
        <button onclick="filterByDeity('durga', this)" class="cat-pill">🦁 माँ दुर्गा</button>
        <button onclick="filterByDeity('lakshmi', this)" class="cat-pill">🪷 माँ लक्ष्मी</button>
        <button onclick="filterByDeity('ram', this)" class="cat-pill">🏹 प्रभु श्री राम</button>
        <button onclick="filterByDeity('saraswati', this)" class="cat-pill">🪕 माँ सरस्वती</button>
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
    var visible = 0;
    cards.forEach(function(c) {{
        var s = (c.getAttribute('data-search') || '') + ' ' + (c.getAttribute('data-god') || '') + ' ' + (c.getAttribute('data-cat') || '');
        if (!q || s.toLowerCase().indexOf(q) !== -1) {{
            c.style.display = '';
            visible++;
        }} else {{
            c.style.display = 'none';
        }}
    }});
    var disp = document.getElementById('searchCountDisplay');
    if (disp) {{
        disp.textContent = q ? (visible + ' पावन दर्शन मिले') : '{len(all_items)}+ पावन 4K दर्शन उपलब्ध';
    }}
}}

function filterByDeity(tag, btn) {{
    document.querySelectorAll('.cat-pill').forEach(function(b){{ b.classList.remove('active'); }});
    if (btn) btn.classList.add('active');
    var input = document.getElementById('searchInput');
    if (tag === 'all') {{
        input.value = '';
    }} else {{
        input.value = tag;
    }}
    filterCards();
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
        _, _, it_abs, _ = resolve_image_assets(it["img"])
        xml.append('    <item>')
        xml.append(f'      <title><![CDATA[{it["titleHi"]} | {it["title"]}]]></title>')
        xml.append(f'      <link>{BASE_URL}{it["slug"]}</link>')
        xml.append(f'      <guid isPermaLink="true">{BASE_URL}{it["slug"]}</guid>')
        xml.append(f'      <description><![CDATA[{it["shortDesc"]}]]></description>')
        xml.append(f'      <enclosure url="{xml_escape(it_abs)}" length="250000" type="image/jpeg" />')
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

    # Add top 30 images right to the homepage URL so Googlebot Image indexes them on first crawl!
    for it in all_items[:30]:
        _, _, _, s_loc = resolve_image_assets(it["img"])
        s_title = xml_escape(f"{it['titleHi']} - {it['title']}")
        s_cap = xml_escape(it.get('shortDesc', ''))
        xml_lines.append('    <image:image>')
        xml_lines.append(f'      <image:loc>{s_loc}</image:loc>')
        xml_lines.append(f'      <image:title>{s_title}</image:title>')
        xml_lines.append(f'      <image:caption>{s_cap}</image:caption>')
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
            _, _, _, s_loc = resolve_image_assets(it["img"])
            s_title = xml_escape(f"{it['titleHi']} - {it['title']}")
            s_cap = xml_escape(it.get('shortDesc', ''))
            xml_lines.append('    <image:image>')
            xml_lines.append(f'      <image:loc>{s_loc}</image:loc>')
            xml_lines.append(f'      <image:title>{s_title}</image:title>')
            xml_lines.append(f'      <image:caption>{s_cap}</image:caption>')
            xml_lines.append('    </image:image>')
        xml_lines.append('  </url>')

    # Individual photo pages with Google Image extensions
    xml_lines.append('  <!-- Dedicated Photo Pages -->')
    for it in all_items:
        _, _, _, s_loc = resolve_image_assets(it["img"])
        s_title = xml_escape(f"{it['titleHi']} - {it['title']}")
        s_cap = xml_escape(it.get('shortDesc', ''))
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{BASE_URL}{it["slug"]}</loc>')
        xml_lines.append(f'    <lastmod>{today_iso}</lastmod>')
        xml_lines.append('    <changefreq>daily</changefreq>')
        xml_lines.append('    <priority>0.8</priority>')
        xml_lines.append('    <image:image>')
        xml_lines.append(f'      <image:loc>{s_loc}</image:loc>')
        xml_lines.append(f'      <image:title>{s_title}</image:title>')
        xml_lines.append(f'      <image:caption>{s_cap}</image:caption>')
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

    # Static Policy Pages
    xml_lines.append('  <!-- Static Policy & Trust Pages (AdSense Compliance) -->')
    for sp in ['about.html', 'contact.html', 'privacy-policy.html', 'terms.html', 'disclaimer.html']:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{BASE_URL}{sp}</loc>')
        xml_lines.append(f'    <lastmod>{today_iso}</lastmod>')
        xml_lines.append('    <changefreq>monthly</changefreq>')
        xml_lines.append('    <priority>0.7</priority>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    return "\n".join(xml_lines)

def generate_about_page():
    """About Us page — required for AdSense approval and E-E-A-T."""
    today_iso = date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>हमारे बारे में | Hindu Gods Daily Gallery — About Us</title>
    <meta name="description" content="Hindu Gods Daily Gallery के बारे में जानें — भारत की #1 दैनिक हिन्दू देव-देवी 4K वॉलपेपर वेबसाइट। हमारा मिशन, विजन और संपादकीय मूल्य।">
    <link rel="canonical" href="{BASE_URL}about.html">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "AboutPage",
      "name": "हमारे बारे में — Hindu Gods Daily Gallery",
      "description": "Daily 4K Hindu God Wallpaper, Mantras, Chalisa and WhatsApp Status — Free for all devotees.",
      "url": "{BASE_URL}about.html",
      "publisher": {{
        "@type": "Organization",
        "name": "Hindu Gods Daily Gallery",
        "url": "{BASE_URL}",
        "logo": "{BASE_URL}favicon.png"
      }}
    }}
    </script>
    {COMMON_STYLE}
</head>
<body>
<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper &amp; WhatsApp Status</p>
</header>
<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="category-cute.html" class="nav-link">🧸 Cute Gallery</a>
    <a href="category-trending.html" class="nav-link">🔥 Trending 4K</a>
    <a href="category-shiva.html" class="nav-link">🔱 Mahadev</a>
    <a href="category-krishna.html" class="nav-link">🦚 Krishna</a>
    <a href="hanuman-chalisa.html" class="nav-link" style="color:var(--saffron);">🚩 हनुमान चालीसा</a>
</nav>
<div class="container" style="max-width:960px; margin:24px auto; padding:20px;">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>हमारे बारे में</span>
    </nav>
    <main>
        <div class="article-box" style="background:#fff; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,0.06); border-top:4px solid var(--saffron);">
            <h1 style="color:var(--maroon); font-family:'Rozha One',serif; font-size:2.2rem; margin-bottom:16px; text-align:center;">🙏 हमारे बारे में (About Us)</h1>
            <p style="font-size:1.15rem; color:#555; text-align:center; max-width:750px; margin:0 auto 24px;">
                सनातन धर्म की पावन ऊर्जा, दिव्यता और सौम्यता को डिजिटल युग के हर श्रद्धालु तक पहुँचाने का एक विनम्र प्रयास।
            </p>

            <h2 style="color:var(--maroon); margin-top:28px; margin-bottom:12px; font-family:'Rozha One',serif;">🌺 हमारा परिचय</h2>
            <p style="font-size:1.05rem; line-height:1.8; color:#333;">
                <strong>Hindu Gods Daily Gallery</strong> भारत की एक प्रमुख और समर्पित भक्ति डिजिटल गैलरी है। यहाँ प्रतिदिन हिन्दू देवी-देवताओं के
                4K Ultra HD वॉलपेपर, वैदिक मंत्र, सम्पूर्ण चालीसा, दैनिक आरतियां और प्रामाणिक पंचांग प्रकाशित किए जाते हैं।
                हमारा उद्देश्य है कि प्रत्येक श्रद्धालु अपने दिन का प्रारंभ पावन ईश्वरीय दर्शन और सकारात्मक विचारों के साथ कर सके।
            </p>
            <p style="font-size:1.05rem; line-height:1.8; color:#333;">
                हमारे संग्रह में <strong>महादेव शिव, भगवान श्री कृष्ण, पवनपुत्र हनुमान, माता दुर्गा, धनलक्ष्मी, विद्यादायिनी सरस्वती,
                विघ्नहर्ता गणेश और मर्यादा पुरुषोत्तम श्री राम</strong> के दिव्य और बाल स्वरूप (Cute God Wallpapers) विशेष रूप से सुसज्जित हैं।
            </p>

            <h2 style="color:var(--maroon); margin-top:28px; margin-bottom:12px; font-family:'Rozha One',serif;">🎯 हमारा ध्येय एवं विजन (Our Mission)</h2>
            <p style="font-size:1.05rem; line-height:1.8; color:#333;">
                हमारा मुख्य विजन है — <em>"हर मोबाइल स्क्रीन पर पावन दर्शन, हर घर में सुख-शांति और ईश्वरीय कृपा।"</em>
            </p>
            <ul style="list-style:none; padding:0; margin:16px 0;">
                <li style="padding:10px 16px; margin-bottom:8px; background:rgba(255,153,0,0.08); border-left:4px solid var(--saffron); border-radius:6px; font-size:1rem;">
                    ✨ <strong>नित्य नवीन 4K दर्शन:</strong> प्रतिदिन 10 नवीन, उच्च रिज़ॉल्यूशन (1024×1365) देव प्रतिमाएं।
                </li>
                <li style="padding:10px 16px; margin-bottom:8px; background:rgba(255,153,0,0.08); border-left:4px solid var(--saffron); border-radius:6px; font-size:1rem;">
                    📲 <strong>1-Click WhatsApp Status:</strong> एक क्लिक में परिवार और मित्रों के साथ मंत्र सहित फोटो शेयर करने की सुविधा।
                </li>
                <li style="padding:10px 16px; margin-bottom:8px; background:rgba(255,153,0,0.08); border-left:4px solid var(--saffron); border-radius:6px; font-size:1rem;">
                    📖 <strong>प्रामाणिक वैदिक सामग्री:</strong> प्रत्येक छवि के साथ प्रामाणिक श्लोक, मंत्र, उनका सरल हिंदी अर्थ और पौराणिक संदर्भ।
                </li>
                <li style="padding:10px 16px; margin-bottom:8px; background:rgba(255,153,0,0.08); border-left:4px solid var(--saffron); border-radius:6px; font-size:1rem;">
                    📿 <strong>डिजिटल साधना टूल्स:</strong> दैनिक पंचांग, 108 जाप माला, वर्चुअल मंदिर घंटी और शंख नाद।
                </li>
            </ul>

            <h2 style="color:var(--maroon); margin-top:28px; margin-bottom:12px; font-family:'Rozha One',serif;">🛡️ संपादकीय एवं गुणवत्ता मानक (Quality Standards)</h2>
            <p style="font-size:1.05rem; line-height:1.8; color:#333;">
                हमारी टीम यह सुनिश्चित करती है कि सभी प्रस्तुत छवियां अत्यंत आदर, धार्मिक मर्यादा और भक्ति भाव से तैयार की गई हों।
                हम आधुनिक रचनात्मक तकनीक के साथ-साथ पारंपरिक शास्त्रों के सौंदर्य का पूर्ण सम्मान करते हैं।
                यह वेबसाइट सभी भक्तों के लिए 100% निःशुल्क और सुरक्षित है।
            </p>

            <div style="text-align:center; margin-top:36px; padding-top:24px; border-top:1px solid #eee;">
                <p style="font-family:'Rozha One',serif; color:var(--maroon); font-size:1.25rem;">
                    ॥ सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः ॥<br>
                    जय श्री राम | हर हर महादेव | गणपति बप्पा मोरया 🙏
                </p>
            </div>
        </div>
    </main>
</div>
{COMMON_FOOTER}
</body>
</html>"""


def generate_contact_page():
    """Contact Us page — required for AdSense approval and transparent communication."""
    return f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>संपर्क करें | Hindu Gods Daily Gallery — Contact Us</title>
    <meta name="description" content="Hindu Gods Daily Gallery से संपर्क करें — सुझाव, प्रतिक्रिया, तकनीकी सहायता, अथवा नवीन देव प्रतिमा अनुरोध।">
    <link rel="canonical" href="{BASE_URL}contact.html">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ContactPage",
      "name": "संपर्क करें — Hindu Gods Daily Gallery",
      "url": "{BASE_URL}contact.html"
    }}
    </script>
    {COMMON_STYLE}
</head>
<body>
<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper &amp; WhatsApp Status</p>
</header>
<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="about.html" class="nav-link">हमारे बारे में</a>
    <a href="category-cute.html" class="nav-link">🧸 Cute Gallery</a>
    <a href="category-trending.html" class="nav-link">🔥 Trending 4K</a>
    <a href="hanuman-chalisa.html" class="nav-link" style="color:var(--saffron);">🚩 हनुमान चालीसा</a>
</nav>
<div class="container" style="max-width:960px; margin:24px auto; padding:20px;">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>संपर्क करें</span>
    </nav>
    <main>
        <div class="article-box" style="background:#fff; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,0.06); border-top:4px solid var(--saffron);">
            <h1 style="color:var(--maroon); font-family:'Rozha One',serif; font-size:2.2rem; margin-bottom:16px; text-align:center;">📬 संपर्क करें (Contact Us)</h1>
            <p style="font-size:1.15rem; color:#555; text-align:center; max-width:750px; margin:0 auto 28px;">
                श्रद्धालुओं और पाठकों के विचार, सुझाव और प्रश्न हमारे लिए अत्यंत बहुमूल्य हैं।
            </p>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:20px; margin-bottom:28px;">
                <div style="background:rgba(255,153,0,0.06); border:1.5px solid rgba(255,119,0,0.3); border-radius:12px; padding:20px; text-align:center;">
                    <div style="font-size:2.5rem; margin-bottom:8px;">💬</div>
                    <h3 style="color:var(--maroon); margin-bottom:8px; font-family:'Rozha One',serif;">सामान्य पूछताछ व सुझाव</h3>
                    <p style="font-size:0.95rem; color:#666; margin-bottom:14px;">वेबसाइट सुधार, नई श्रेणियों अथवा देव प्रतिमाओं के सुझाव हेतु।</p>
                    <a href="https://github.com/pmeena9098610-dot/HinduGodsGallery/issues" target="_blank" rel="noopener" style="display:inline-block; background:var(--maroon); color:#fff; padding:8px 18px; border-radius:20px; text-decoration:none; font-weight:600; font-size:0.9rem;">
                        GitHub Community Issues
                    </a>
                </div>
                <div style="background:rgba(255,153,0,0.06); border:1.5px solid rgba(255,119,0,0.3); border-radius:12px; padding:20px; text-align:center;">
                    <div style="font-size:2.5rem; margin-bottom:8px;">⚖️</div>
                    <h3 style="color:var(--maroon); margin-bottom:8px; font-family:'Rozha One',serif;">कॉपीराइट एवं नीतिगत विषय</h3>
                    <p style="font-size:0.95rem; color:#666; margin-bottom:14px;">सामग्री, बौद्धिक संपदा अथवा गोपनीयता नीति संबंधी प्रश्नों हेतु।</p>
                    <a href="privacy-policy.html" style="display:inline-block; background:var(--saffron); color:#fff; padding:8px 18px; border-radius:20px; text-decoration:none; font-weight:600; font-size:0.9rem;">
                        Privacy Policy देखें
                    </a>
                </div>
            </div>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">📋 संपर्क के प्रमुख विषय</h2>
            <ul style="list-style:disc; margin-left:24px; color:#444; line-height:1.8;">
                <li><strong>विशेष देव प्रतिमा का अनुरोध:</strong> यदि आप किसी विशेष मंदिर, स्वरूप अथवा त्यौहार के 4K वॉलपेपर चाहते हैं।</li>
                <li><strong>तकनीकी त्रुटि (Bug Report):</strong> यदि कोई छवि लोड न हो रही हो, डाउनलोड में समस्या हो, अथवा लिंक टूटा हो।</li>
                <li><strong>मंत्र अथवा पाठ संशोधन:</strong> यदि किसी श्लोक या मंत्र के उच्चारण में सुधार अपेक्षित हो।</li>
            </ul>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">⏱️ प्रतिक्रिया समय</h2>
            <p style="font-size:1.05rem; line-height:1.8; color:#333;">
                हमारी तकनीकी व संपादकीय टीम प्राप्त सुझावों का मूल्यांकन कर <strong>24 से 48 घंटों</strong> के भीतर समाधान करने का पूर्ण प्रयास करती है।
            </p>

            <div style="text-align:center; margin-top:32px; padding-top:20px; border-top:1px solid #eee;">
                <p style="font-family:'Rozha One',serif; color:var(--maroon); font-size:1.15rem;">
                    भगवान आपके जीवन में सुख, शांति और समृद्धि प्रदान करें। जय श्री राम 🙏
                </p>
            </div>
        </div>
    </main>
</div>
{COMMON_FOOTER}
</body>
</html>"""


def generate_privacy_page():
    """Privacy Policy page — comprehensive compliance for AdSense, GDPR, CCPA, Cookies."""
    today_iso = date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>Privacy Policy (गोपनीयता नीति) | Hindu Gods Daily Gallery</title>
    <meta name="description" content="Hindu Gods Daily Gallery की गोपनीयता नीति — हम आपके डेटा की सुरक्षा का पूर्ण सम्मान करते हैं। Google AdSense, Cookies और पारदर्शिता विवरण।">
    <link rel="canonical" href="{BASE_URL}privacy-policy.html">
    {COMMON_STYLE}
</head>
<body>
<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper &amp; WhatsApp Status</p>
</header>
<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="about.html" class="nav-link">हमारे बारे में</a>
    <a href="contact.html" class="nav-link">संपर्क</a>
    <a href="terms.html" class="nav-link">नियम एवं शर्तें</a>
</nav>
<div class="container" style="max-width:960px; margin:24px auto; padding:20px;">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>Privacy Policy</span>
    </nav>
    <main>
        <div class="article-box" style="background:#fff; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,0.06); border-top:4px solid var(--saffron);">
            <h1 style="color:var(--maroon); font-family:'Rozha One',serif; font-size:2.2rem; margin-bottom:8px; text-align:center;">🔒 गोपनीयता नीति (Privacy Policy)</h1>
            <p style="color:#888; font-size:0.9rem; text-align:center; margin-bottom:24px;">अंतिम अद्यतन (Last Updated): {today_iso}</p>

            <p style="font-size:1.05rem; line-height:1.8; color:#333;">
                <strong>Hindu Gods Daily Gallery</strong> (वेबसाइट URL: <a href="{BASE_URL}" style="color:var(--maroon);">{BASE_URL}</a>) पर हम अपने आगंतुकों की गोपनीयता का सर्वोच्च सम्मान करते हैं।
                यह गोपनीयता नीति दस्तावेज स्पष्ट करता है कि हमारी वेबसाइट द्वारा किस प्रकार की जानकारी एकत्र व दर्ज की जाती है और हम उसका किस प्रकार उपयोग करते हैं।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">1. व्यक्तिगत डेटा संग्रह (Personal Data Collection)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                हम एक निःशुल्क, सार्वजनिक भक्ति पोर्टल हैं। हमारी वेबसाइट पर विज़िट करने, 4K वॉलपेपर डाउनलोड करने, मंत्र पढ़ने अथवा पंचांग देखने के लिए किसी भी प्रकार के 
                <strong>पंजीकरण (Registration), लॉगिन (Login) अथवा व्यक्तिगत पहचान जानकारी (जैसे नाम, ईमेल, फोन नंबर)</strong> की आवश्यकता नहीं होती। हम प्रत्यक्ष रूप से आपकी कोई भी व्यक्तिगत जानकारी संग्रहीत नहीं करते।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">2. लॉग फाइल्स (Log Files)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                मानक वेब सर्वर प्रक्रियाओं के अनुसार (GitHub Pages होस्टिंग प्लेटफॉर्म द्वारा), सर्वर विज़िट के दौरान अज्ञात तकनीकी लॉग एकत्र हो सकते हैं, जिनमें इंटरनेट प्रोटोकॉल (IP) पते, ब्राउज़र प्रकार, इंटरनेट सेवा प्रदाता (ISP), दिनांक/समय स्टैम्प, रेफरिंग पृष्ठ और क्लिक्स की संख्या शामिल हो सकती है। यह जानकारी किसी भी व्यक्तिगत पहचान से संबद्ध नहीं होती और केवल साइट के तकनीकी प्रबंधन तथा रुझानों के विश्लेषण हेतु प्रयुक्त होती है।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">3. कुकीज़ एवं स्थानीय संग्रहण (Cookies &amp; Local Storage)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                हमारी वेबसाइट उपयोगकर्ता अनुभव को समृद्ध बनाने के लिए स्थानीय ब्राउज़र संग्रहण (Local Storage / Session Storage) का उपयोग करती है। उदाहरणार्थ — आपकी 108 जाप माला की प्रगति, वर्चुअल दीपक प्रज्ज्वलन स्थिति अथवा डार्क मोड प्राथमिकताएं। ये कुकीज़ किसी भी बाहरी सर्वर को प्रेषित नहीं की जातीं और पूर्णतः आपके स्थानीय डिवाइस में सुरक्षित रहती हैं।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">4. गूगल ऐडसेंस एवं थर्ड-पार्टी विज्ञापन (Google AdSense)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                Google हमारी साइट पर एक तृतीय-पक्ष विक्रेता के रूप में विज्ञापन प्रदर्शित करने के लिए कुकीज़ (जैसे DoubleClick DART कुकी) का उपयोग कर सकता है। DART कुकी का उपयोग Google को हमारे उपयोगकर्ताओं को इस साइट और इंटरनेट पर अन्य साइटों पर उनकी विज़िट के आधार पर विज्ञापन प्रस्तुत करने में सक्षम बनाता है।
                उपयोगकर्ता Google विज्ञापन और सामग्री नेटवर्क गोपनीयता नीति पर जाकर DART कुकी के उपयोग को ऑप्ट-आउट कर सकते हैं:
                <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener" style="color:var(--maroon); font-weight:600;">Google Ads Privacy Policy</a>.
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">5. बच्चों की गोपनीयता (Children's Privacy Protection)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                हमारी भक्ति सामग्री सभी आयु वर्गों के लिए पूर्णतः सुरक्षित और सकारात्मक है। हम 13 वर्ष से कम आयु के बच्चों से जानबूझकर कोई भी व्यक्तिगत पहचान योग्य जानकारी एकत्र नहीं करते। यदि आपको विश्वास है कि किसी बच्चे ने हमारी साइट पर जानकारी प्रदान की है, तो कृपया तत्काल हमसे संपर्क करें।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">6. सहमति (Consent)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                हमारी वेबसाइट का उपयोग करके, आप एतद्द्वारा हमारी गोपनीयता नीति से सहमति व्यक्त करते हैं और इसके सभी नियमों व शर्तों को स्वीकार करते हैं।
            </p>

            <div style="text-align:center; margin-top:32px; padding-top:20px; border-top:1px solid #eee;">
                <p style="font-size:0.95rem; color:#777;">
                    गोपनीयता नीति संबंधी किसी भी प्रश्न के लिए कृपया <a href="contact.html" style="color:var(--maroon);">संपर्क पृष्ठ</a> पर संपर्क करें।
                </p>
            </div>
        </div>
    </main>
</div>
{COMMON_FOOTER}
</body>
</html>"""


def generate_terms_page():
    """Terms of Service page — formal legal clarity for Google compliance."""
    today_iso = date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>नियम एवं शर्तें | Hindu Gods Daily Gallery — Terms of Service</title>
    <meta name="description" content="Hindu Gods Daily Gallery की सेवा शर्तें एवं उपयोग नियम — निःशुल्क धार्मिक वॉलपेपर, डाउनलोडिंग और स्टेटस शेयरिंग संबंधी दिशा-निर्देश।">
    <link rel="canonical" href="{BASE_URL}terms.html">
    {COMMON_STYLE}
</head>
<body>
<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper &amp; WhatsApp Status</p>
</header>
<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="about.html" class="nav-link">हमारे बारे में</a>
    <a href="privacy-policy.html" class="nav-link">Privacy Policy</a>
    <a href="contact.html" class="nav-link">संपर्क</a>
</nav>
<div class="container" style="max-width:960px; margin:24px auto; padding:20px;">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>Terms of Service</span>
    </nav>
    <main>
        <div class="article-box" style="background:#fff; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,0.06); border-top:4px solid var(--saffron);">
            <h1 style="color:var(--maroon); font-family:'Rozha One',serif; font-size:2.2rem; margin-bottom:8px; text-align:center;">📜 उपयोग की शर्तें (Terms of Service)</h1>
            <p style="color:#888; font-size:0.9rem; text-align:center; margin-bottom:24px;">अंतिम अद्यतन: {today_iso}</p>

            <h2 style="color:var(--maroon); margin-top:20px; margin-bottom:12px; font-family:'Rozha One',serif;">1. स्वीकृति (Acceptance of Terms)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                Hindu Gods Daily Gallery में आपका स्वागत है। इस वेबसाइट का उपयोग करके, आप इन सेवा शर्तों, हमारी गोपनीयता नीति तथा लागू सभी स्थानीय व अंतरराष्ट्रीय कानूनों का पालन करने के लिए अपनी बाध्यकारी सहमति प्रदान करते हैं।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">2. सामग्री का अनुमत उपयोग (Permitted Use)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                इस वेबसाइट पर उपलब्ध समस्त 4K देव प्रतिमाएं, मंत्र, आरतियां एवं चालीसा पाठ श्रद्धालुओं के <strong>व्यक्तिगत, गैर-व्यावसायिक एवं भक्ति उपयोग</strong> हेतु 100% निःशुल्क प्रदान की गई हैं।
                आप इन छवियों को अपने मोबाइल/कंप्यूटर वॉलपेपर, WhatsApp स्टेटस, पारिवारिक साझाकरण तथा व्यक्तिगत पूजा-साधना में निर्बाध रूप से उपयोग कर सकते हैं।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">3. बौद्धिक संपदा एवं प्रतिबंध (Intellectual Property &amp; Restrictions)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                उपयोगकर्ताओं को निम्नलिखित गतिविधियों की अनुमति नहीं है:
            </p>
            <ul style="list-style:disc; margin-left:24px; color:#444; line-height:1.8;">
                <li>वेबसाइट की सामग्री को किसी भी व्यावसायिक लाभ अथवा पुनर्विक्रय (Resale/Merchandise) हेतु बिना पूर्व लिखित अनुमति के उपयोग करना।</li>
                <li>वेबसाइट के किसी भी अंश का दुर्भावनापूर्ण अथवा सनातन धर्म की मर्यादा के विपरीत अनैतिक प्रयोग।</li>
                <li>स्वचालित बॉट्स द्वारा साइट के सर्वर पर अनुचित भार डालना।</li>
            </ul>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">4. दायित्व की सीमा (Limitation of Liability)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                यह वेबसाइट "जैसी है" (AS IS) आधार पर भक्ति सेवा भाव से संचालित है। हम साइट के निरंतर, त्रुटिरहित अथवा किसी भी समय अनुपलब्ध होने के उत्तरदायी नहीं होंगे, यद्यपि हम 99.9% निर्बाध सेवा बनाए रखने हेतु सतत प्रयासरत रहते हैं।
            </p>
        </div>
    </main>
</div>
{COMMON_FOOTER}
</body>
</html>"""


def generate_disclaimer_page():
    """Disclaimer page — spiritual, mythological, and AI generation transparency."""
    today_iso = date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="hi" prefix="og: https://ogp.me/ns#">
<head>
    {COMMON_HEAD}
    <title>अस्वीकरण | Hindu Gods Daily Gallery — Disclaimer</title>
    <meta name="description" content="Hindu Gods Daily Gallery का अस्वीकरण (Disclaimer) — धार्मिक निष्ठा, कलात्मक चित्रण और सनातन मर्यादा संबंधी स्पष्टीकरण।">
    <link rel="canonical" href="{BASE_URL}disclaimer.html">
    {COMMON_STYLE}
</head>
<body>
<header class="site-header">
    <h1><a href="index.html">ॐ दैनिक हिन्दू भगवान दर्शन</a></h1>
    <p>Daily Cute Hindu Gods 4K Wallpaper &amp; WhatsApp Status</p>
</header>
<nav class="top-nav">
    <a href="index.html" class="nav-link">Home (होम)</a>
    <a href="about.html" class="nav-link">हमारे बारे में</a>
    <a href="privacy-policy.html" class="nav-link">Privacy Policy</a>
    <a href="contact.html" class="nav-link">संपर्क</a>
</nav>
<div class="container" style="max-width:960px; margin:24px auto; padding:20px;">
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> &raquo;
        <span>Disclaimer</span>
    </nav>
    <main>
        <div class="article-box" style="background:#fff; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,0.06); border-top:4px solid var(--saffron);">
            <h1 style="color:var(--maroon); font-family:'Rozha One',serif; font-size:2.2rem; margin-bottom:8px; text-align:center;">⚠️ अस्वीकरण (Disclaimer)</h1>
            <p style="color:#888; font-size:0.9rem; text-align:center; margin-bottom:24px;">अंतिम अद्यतन: {today_iso}</p>

            <h2 style="color:var(--maroon); margin-top:20px; margin-bottom:12px; font-family:'Rozha One',serif;">1. धार्मिक एवं आध्यात्मिक निष्ठा (Faith &amp; Devotion)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                Hindu Gods Daily Gallery पर प्रकाशित समस्त कलाकृतियां, आरतियां, चालीसा, मंत्र एवं पंचांग केवल और केवल सनातन धर्म की निष्ठा, भक्ति प्रचार तथा श्रद्धालुओं के आध्यात्मिक कल्याण के उद्देश्य से प्रस्तुत किए जाते हैं। हमारा उद्देश्य किसी भी संप्रदाय, जाति, पंथ अथवा आस्था की भावना को ठेस पहुँचाना नहीं है।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">2. कलात्मक एवं रचनात्मक स्वरूप (Artistic Representation)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                गैलरी में प्रस्तुत अनेक छवियां — विशेष रूप से 'क्यूट बाल स्वरूप' (Cute Bal Roop) — आधुनिक डिजिटल कलात्मक तकनीकों एवं पारंपरिक पुराणों में वर्णित वात्सल्य भाव की सुंदर प्रेरणा से सृजित की गई हैं। यह विशुद्ध रूप से ईश्वर के प्रति प्रेम और वात्सल्य भक्ति को समर्पित एक कलात्मक अभिव्यक्ति है।
            </p>

            <h2 style="color:var(--maroon); margin-top:24px; margin-bottom:12px; font-family:'Rozha One',serif;">3. पंचांग एवं मुहूर्त सूचना (Panchang Information)</h2>
            <p style="font-size:1.02rem; line-height:1.8; color:#444;">
                प्रदर्शित दैनिक पंचांग, तिथि, नक्षत्र व शुभ मुहूर्त सामान्य धार्मिक जानकारी हेतु प्रदान किए जाते हैं। किसी भी विशेष व्रत, यज्ञानुष्ठान अथवा मांगलिक कार्य के लिए श्रद्धालु अपने स्थानीय पुरोहित अथवा विद्वान ज्योतिषाचार्य से अवश्य परामर्श लें, क्योंकि स्थानीय सूर्योदय-सूर्यास्त के अनुसार समय में सूक्ष्म अंतर हो सकता है।
            </p>

            <div style="text-align:center; margin-top:32px; padding-top:20px; border-top:1px solid #eee;">
                <p style="font-family:'Rozha One',serif; color:var(--maroon); font-size:1.15rem;">
                    ॥ ॐ शांतिः शांतिः शांतिः ॥<br>
                    समस्त विश्व का कल्याण हो 🙏
                </p>
            </div>
        </div>
    </main>
</div>
{COMMON_FOOTER}
</body>
</html>"""

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

# 5. Generate Essential Policy & Trust Pages (About, Contact, Privacy, Terms, Disclaimer)
generated_files["about.html"] = generate_about_page()
generated_files["contact.html"] = generate_contact_page()
generated_files["privacy-policy.html"] = generate_privacy_page()
generated_files["terms.html"] = generate_terms_page()
generated_files["disclaimer.html"] = generate_disclaimer_page()
print("Generated 5 Essential Policy & Trust Pages for Google AdSense Approval!")
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
