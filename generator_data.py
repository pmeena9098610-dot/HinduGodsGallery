import os, json

# Base URL on GitHub Pages
BASE_URL = "https://pmeena9098610-dot.github.io/HinduGodsGallery/"

# Master item database with rich devotional content & mantras
ITEMS = [
    {
        "id": "cute-radha-krishna",
        "slug": "photo-cute-radha-krishna.html",
        "title": "Cute Radha Krishna Love 4K Wallpaper",
        "titleHi": "राधा कृष्ण क्यूट लव 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "krishna",
        "img": "images/cute_radha_krishna",
        "badge": "Cute Special",
        "shortDesc": "Adorable baby Radha and baby Krishna holding hands smiling in magical Vrindavan garden with blooming flowers, butterflies, and divine golden light.",
        "mantra": "हरे कृष्ण हरे कृष्ण, कृष्ण कृष्ण हरे हरे ।\nहरे राम हरे राम, राम राम हरे हरे ॥",
        "mantraMeaning": "हे भगवान कृष्ण, हे भगवान राम, मुझे अपनी प्रेमाभक्ति में लीन कीजिए। यह महामंत्र जीवन में सुख, शांति और प्रेम का संचार करता है।",
        "article": """राधा और कृष्ण का प्रेम ब्रह्मांड का सबसे पावन और अलौकिक प्रेम माना जाता है। इस 4K वॉलपेपर में बाल रूप में श्री राधा और कृष्ण को वृंदावन के मनमोहक बगीचे में एक-दूसरे का हाथ थामे दिखाया गया है। उनके मुख पर मधुर मुस्कान, मोरपंख से सजे घुंघराले बाल और चारों ओर खिले सुगंधित पुष्प मन को असीम शांति प्रदान करते हैं। 

यह क्यूट राधा कृष्ण फोटो मोबाइल वॉलपेपर, व्हाट्सएप डीपी (WhatsApp DP), और दैनिक गुड मॉर्निंग स्टेटस (Good Morning Status) के लिए अत्यंत लोकप्रिय है। इस छवि को अपने फोन स्क्रीन पर लगाने से दिनभर सकारात्मक ऊर्जा और भक्ति का अनुभव होता है।""",
        "tags": ["cute radha krishna love photo", "radha krishna wallpaper 4k", "radha krishna whatsapp status", "baby radha krishna image", "vrindavan love photo", "cute bal radha krishna hd"]
    },
    {
        "id": "cute-bal-shiva",
        "slug": "photo-cute-bal-shiva.html",
        "title": "Cute Baby Shiva with Damru 4K Wallpaper",
        "titleHi": "क्यूट बाल शिव जी डमरू 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "shiva",
        "img": "images/cute_bal_shiva",
        "badge": "Cute Special",
        "shortDesc": "Ultra cute baby Lord Shiva playing golden damru on tiger skin with tiny Nandi calf, set against snowy Himalayan peaks in divine golden aura.",
        "mantra": "कर्पूरगौरं करुणावतारं संसारसारम् भुजगेन्द्रहारम् ।\nसदावसन्तं हृदयारविन्दे भवं भवानीसहितं नमामि ॥",
        "mantraMeaning": "कपूर के समान उज्ज्वल, करुणा के अवतार, संसार के सार और भुजंगों का हार पहनने वाले भगवान शिव को माता भवानी सहित मैं नमन करता हूँ।",
        "article": """भगवान शिव का बाल रूप भक्तों को सम्मोहित कर देने वाला है। इस विशेष 4K कलाकृति में बाल शिव बाघ की खाल पर विराजमान होकर नन्हे हाथों से डमरू बजा रहे हैं। उनके माथे पर छोटा सा बाल चंद्रमा, त्रिशूल और पास में प्रेमपूर्वक बैठा नंदी बछड़ा इस दृश्य को अलौकिक सुंदरता प्रदान करता है।

सोमवार के व्रत, महाशिवरात्रि एवं दैनिक शिव पूजा के लिए यह फोटो अत्यंत शुभ मानी जाती है। अपने मोबाइल में बाल भोलेनाथ का यह स्वरूप रखने से भय, चिंता और नकारात्मक ऊर्जा का नाश होता है।""",
        "tags": ["cute baby shiva photo", "bal shiv ji wallpaper", "cute mahadev baby image", "baby shiva damru photo", "cute bholenath wallpaper", "bal shiv 3d wallpaper"]
    },
    {
        "id": "cute-bal-hanuman",
        "slug": "photo-cute-bal-hanuman.html",
        "title": "Cute Baby Hanuman Flying 4K Wallpaper",
        "titleHi": "क्यूट बाल हनुमान जी उड़ते हुए 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "hanuman",
        "img": "images/cute_bal_hanuman",
        "badge": "Cute Special",
        "shortDesc": "Super cute baby Hanuman flying through sunset sky with flowing red cape and golden gada, surrounded by heart-shaped glowing clouds.",
        "mantra": "मनोजवं मारुततुल्यवेगं जितेन्द्रियं बुद्धिमतां वरिष्ठम् ।\nवातात्मजं वानरयूथमुख्यं श्रीरामदूतं शरणं प्रपद्ये ॥",
        "mantraMeaning": "मन के समान वेग वाले, वायु के समान पराक्रमी, इंद्रियों को जीतने वाले और बुद्धिमानों में श्रेष्ठ श्री रामदूत हनुमान जी की मैं शरण लेता हूँ।",
        "article": """पवनपुत्र बाल हनुमान का यह स्वरूप अदम्य साहस, मासूमियत और भक्ति का अद्भुत संगम है। जब बाल हनुमान ने सूर्य देव को फल समझकर आकाश में छलांग लगाई थी, उसी बाल लीला को इस 3D कला में मनमोहक ढंग से प्रस्तुत किया गया है। 

मंगलवार और शनिवार को हनुमान चालीसा के पाठ के साथ यह फोटो स्टेटस में लगाने से हर प्रकार के संकट और भय दूर होते हैं। बच्चों और युवाओं के बीच बाल बजरंगबली का यह स्वरूप अत्यधिक लोकप्रिय है।""",
        "tags": ["cute baby hanuman photo", "bal hanuman flying wallpaper", "cute hanuman ji image", "baby bajrangbali photo", "cute hanuman 3d wallpaper", "bal hanuman gada photo"]
    },
    {
        "id": "cute-krishna-makhan",
        "slug": "photo-cute-krishna-makhan.html",
        "title": "Cute Krishna Stealing Butter 4K Wallpaper",
        "titleHi": "माखन चोर बाल गोपाल क्यूट 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "krishna",
        "img": "images/cute_krishna_makhan",
        "badge": "Cute Special",
        "shortDesc": "Adorable baby Krishna Bal Gopal stealing freshly churned makhan from hanging clay pot with his gopa friends in Vrindavan kitchen.",
        "mantra": "श्री कृष्ण गोविन्द हरे मुरारी, हे नाथ नारायण वासुदेवाय ॥",
        "mantraMeaning": "हे भगवान कृष्ण, हे गोविंद, हे मुरारी, हे नाथ नारायण, आप ही समस्त ब्रह्मांड के पालनकर्ता और मेरे सर्वस्व हैं।",
        "article": """गोकुल और वृंदावन की सबसे प्रिय बाल लीला 'माखन चोरी' है। इस चित्र में नन्हे कान्हा अपने बाल सखाओं के कंधों पर चढ़कर छींके पर टंगी मटकी से ताजा माखन चुरा रहे हैं। मुख पर लगा माखन, नटखट आंखें और मोरपंख मुकुट कन्हैया की अनुपम छवि को जीवंत कर देते हैं।

जन्माष्टमी पर्व और दैनिक सुप्रभात संदेशों के लिए यह फोटो हर हिंदू परिवार की पहली पसंद है। इसे घर में रखने से सुख-शांति और संतान सुख की प्राप्ति मानी जाती है।""",
        "tags": ["makhan chor bal gopal photo", "baby krishna stealing butter", "cute krishna makhan wallpaper", "bal gopal 3d image", "cute kanhaiya photo", "krishna butter thief 4k"]
    },
    {
        "id": "cute-baby-lakshmi",
        "slug": "photo-cute-baby-lakshmi.html",
        "title": "Cute Baby Goddess Lakshmi 4K Wallpaper",
        "titleHi": "क्यूट बेबी लक्ष्मी जी कमल पर 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "lakshmi",
        "img": "images/cute_baby_lakshmi",
        "badge": "Cute Special",
        "shortDesc": "Adorable baby Goddess Lakshmi sitting on blooming pink lotus flower showering gold coins and gems, accompanied by cute owl.",
        "mantra": "ॐ श्रीं ह्रीं क्लीं श्री सिद्ध लक्ष्म्यै नमः ॥",
        "mantraMeaning": "समस्त सुख-समृद्धि, धन-वैभव और सौभाग्य प्रदान करने वाली परम पूज्य मां लक्ष्मी को बारंबार नमन।",
        "article": """धन, वैभव और सौभाग्य की अधिष्ठात्री देवी मां लक्ष्मी का यह बाल रूप अत्यंत दुर्लभ और मनमोहक है। गुलाबी कमल दल पर बैठी नन्ही लक्ष्मी जी अपने नन्हे हाथों से स्वर्णिम सिक्कों की वर्षा कर रही हैं। 

दीपावली, धनतेरस, शुक्रवार की लक्ष्मी पूजा और व्यापार में बरकत के लिए यह फोटो अत्यंत शुभ मानी जाती है। इसे मोबाइल स्क्रीन पर रखने से घर में लक्ष्मी जी का स्थाई वास होता है।""",
        "tags": ["cute baby lakshmi photo", "baby lakshmi devi wallpaper", "cute lakshmi lotus image", "baby goddess lakshmi 3d", "cute maa lakshmi photo", "lakshmi gold coins wallpaper"]
    },
    {
        "id": "cute-ganesha-reading",
        "slug": "photo-cute-ganesha-reading.html",
        "title": "Cute Bal Ganesha Reading Book 4K Wallpaper",
        "titleHi": "क्यूट बाल गणेश जी पढ़ाई करते हुए 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "ganesha",
        "img": "images/cute_ganesha_reading",
        "badge": "Cute Special",
        "shortDesc": "Baby Ganesha wearing spectacles reading glowing divine scripture with modak in hand and his little mouse reading alongside.",
        "mantra": "वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ ।\nनिर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा ॥",
        "mantraMeaning": "घुमावदार सूंड वाले, विशाल शरीर वाले और करोड़ों सूर्यों के समान तेजस्वी हे गणेश देव, मेरे सभी कार्यों को सदा बाधा रहित पूर्ण करें।",
        "article": """बुद्धि, विवेक और विद्या के दाता भगवान गणेश का यह बाल रूप विद्यार्थियों और युवाओं के लिए प्रेरणादायक है। नन्हे गणपति चश्मा लगाकर वेदों का अध्ययन कर रहे हैं और उनके साथ उनका प्रिय मूषक भी नन्ही किताब पढ़ रहा है। 

गणेश चतुर्थी, बुधवार के दिन और किसी भी नए कार्य, परीक्षा या व्यापार की शुरुआत में यह वॉलपेपर लगाना अत्यंत शुभ और सिद्धिदायक माना जाता है।""",
        "tags": ["cute ganesha reading photo", "baby ganesh padhai wallpaper", "cute ganpati bappa image", "bal ganesh 3d cute", "ganesha with book image", "cute ganesh modak wallpaper"]
    },
    {
        "id": "cute-baby-saraswati",
        "slug": "photo-cute-baby-saraswati.html",
        "title": "Cute Baby Saraswati with Veena 4K Wallpaper",
        "titleHi": "क्यूट बेबी सरस्वती जी वीणा वादिनी 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "saraswati",
        "img": "images/cute_baby_saraswati",
        "badge": "Cute Special",
        "shortDesc": "Adorable baby Goddess Saraswati seated on white swan playing golden veena beside glowing lotus pond with floating sacred books.",
        "mantra": "सरस्वति नमस्तुभ्यं वरदे कामरूपिणि ।\nविद्यारम्भं करिष्यामि सिद्धिर्भवतु मे सदा ॥",
        "mantraMeaning": "हे वरदायिनी और सबकी मनोकामनाएं पूर्ण करने वाली मां सरस्वती, मैं विद्या अध्ययन शुरू कर रहा हूँ, मुझे सदा सफलता प्रदान करें।",
        "article": """ज्ञान, कला, वाणी और संगीत की देवी मां सरस्वती का यह बाल स्वरूप मन को एकाग्र और शांत करने वाला है। धवल वस्त्रों में सुसज्जित नन्ही सरस्वती जी हंस पर विराजमान होकर वीणा की दिव्य तान छेड़ रही हैं। 

वसंत पंचमी, सरस्वती पूजा और विद्यार्थियों के अध्ययन कक्ष के लिए यह चित्र सर्वोत्तम है। इसे प्रतिदिन दर्शन करने से स्मरण शक्ति और बुद्धि का तीव्र विकास होता है।""",
        "tags": ["cute baby saraswati photo", "baby saraswati veena wallpaper", "cute saraswati devi image", "baby goddess saraswati 3d", "cute maa saraswati swan", "saraswati vidya photo"]
    },
    {
        "id": "shiva-kailash",
        "slug": "photo-shiva-kailash.html",
        "title": "Lord Shiva Kailash Meditation 4K Ultra HD Wallpaper",
        "titleHi": "भगवान शिव कैलाश ध्यान 4K महाकाल वॉलपेपर",
        "category": "shiva",
        "categoryName": "Shiva Gallery",
        "categorySlug": "category-shiva.html",
        "god": "shiva",
        "img": "images/lord_shiva_1789315505870",
        "badge": "Trending 4K",
        "shortDesc": "Majestic Lord Shiva Mahadev in deep meditation on snow-covered Mount Kailash with holy Ganga flowing from matted hair, trishul, and damru.",
        "mantra": "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम् ।\nउर्वारुकमिव बन्धनान्मृत्योर्मुक्षीय माऽमृतात् ॥",
        "mantraMeaning": "हम त्रिनेत्रधारी भगवान शिव की आराधना करते हैं जो जीवन में सुगंध और पुष्टि प्रदान करते हैं। वे हमें मृत्यु के बंधनों से मुक्त कर मोक्ष प्रदान करें।",
        "article": """देवों के देव महादेव की समाधि अवस्था का यह दृश्य अत्यंत प्रभावशाली और आध्यात्मिक तेज से परिपूर्ण है। कैलाश पर्वत की बर्फीली चोटियों के मध्य भगवान शिव शांत मुद्रा में ध्यानमग्न हैं। उनकी जटाओं से मां गंगा की अविरल धारा बह रही है और उनके समीप त्रिशूल व डमरू सुशोभित हैं। 

महादेव के 4K वॉलपेपर गूगल पर सबसे अधिक खोजे जाने वाले वॉलपेपर हैं। सावन मास, महाशिवरात्रि और सोमवार के दिन भक्त इसे अपने व्हाट्सएप स्टेटस और फुल स्क्रीन मोबाइल स्क्रीन पर लगाते हैं।""",
        "tags": ["mahadev 4k wallpaper download", "lord shiva kailash meditation", "bholenath hd photo", "shiva trishul damru image", "shiv ji 4k wallpaper", "har har mahadev photo"]
    },
    {
        "id": "krishna-flute",
        "slug": "photo-krishna-flute.html",
        "title": "Lord Krishna Playing Flute in Vrindavan 4K Wallpaper",
        "titleHi": "भगवान श्री कृष्ण बांसुरी वृंदावन 4K वॉलपेपर",
        "category": "krishna",
        "categoryName": "Krishna Gallery",
        "categorySlug": "category-krishna.html",
        "god": "krishna",
        "img": "images/lord_krishna_1789315536423",
        "badge": "Trending 4K",
        "shortDesc": "Divine Lord Krishna playing enchanting bansuri flute in sacred Vrindavan forest alongside dancing peacocks and serene Yamuna river.",
        "mantra": "कस्तूरीतिलकं ललाटपटले वक्षःस्थले कौस्तुभं\nनासाग्रे वरमौक्तिकं करतले वेणुं करे कङ्कणम् ॥",
        "mantraMeaning": "जिनके मस्तक पर कस्तूरी का तिलक, वक्षस्थल पर कौस्तुभ मणि, हाथों में बांसुरी और कंगन सुशोभित हैं, उन भुवन सुंदर भगवान कृष्ण को नमन।",
        "article": """श्यामल वर्ण भगवान श्री कृष्ण की त्रिभंग मुद्रा में बांसुरी वादन की छवि समस्त चराचर जगत को सम्मोहित कर लेती है। वृंदावन के कदम्ब वृक्षों के नीचे, मयूरों के नृत्य और यमुना जी की पावन लहरों के बीच मुरलीधर की यह 4K फोटो भक्ति रस से परिपूर्ण है। 

हर सुबह श्री कृष्ण के दर्शन और इस मधुर वॉलपेपर को देखने से दिनभर मन शांत, प्रसन्न और तनावमुक्त रहता है।""",
        "tags": ["lord krishna flute photo 4k", "krishna bansuri wallpaper", "vrindavan krishna image", "shri krishna hd photo", "krishna peacock feather image", "krishna yamuna photo"]
    },
    {
        "id": "ganesha-throne",
        "slug": "photo-ganesha-throne.html",
        "title": "Lord Ganesha Golden Throne 4K Wallpaper",
        "titleHi": "गणपति बप्पा स्वर्ण सिंहासन 4K वॉलपेपर",
        "category": "ganesha",
        "categoryName": "Ganesha Gallery",
        "categorySlug": "category-ganesha.html",
        "god": "ganesha",
        "img": "images/lord_ganesha_1789315549643",
        "badge": "Trending 4K",
        "shortDesc": "Magnificent Lord Ganesha sitting on golden lotus throne with divine cosmic aura, holding sweet modak with faithful mouse at feet.",
        "mantra": "ॐ गं गणपतये नमः ।\nएकदन्ताय विद्महे वक्रतुण्डाय धीमहि तन्नो दन्तिः प्रचोदयात् ॥",
        "mantraMeaning": "भगवान गणेश को बारंबार नमस्कार। एकदंत और वक्रतुंड स्वरूप वाले श्री गणेश हमारी बुद्धि को सन्मार्ग पर प्रेरित करें।",
        "article": """विघ्नहर्ता और मंगलमूर्ति भगवान गणेश के स्वर्ण सिंहासन पर विराजमान स्वरूप का यह 4K वॉलपेपर ऐश्वर्य और शुभता का प्रतीक है। भगवान के दिव्य वरद हस्त से भक्तों को अभय और सौभाग्य का आशीर्वाद मिल रहा है। 

गणेशोत्सव, संकष्टी चतुर्थी और किसी भी नए व्यापार या गृह प्रवेश के अवसर पर गणपति बप्पा की यह फोटो लगाना मंगलकारी सिद्ध होता है।""",
        "tags": ["ganpati bappa 4k wallpaper", "lord ganesha golden photo", "ganesh ji hd image", "ganesha throne wallpaper", "ganpati bappa morya photo", "vinayak 4k image"]
    },
    {
        "id": "durga-lion",
        "slug": "photo-durga-lion.html",
        "title": "Goddess Durga Riding Lion 4K Wallpaper",
        "titleHi": "मां दुर्गा शेरावाली सिंह वाहिनी 4K फोटो",
        "category": "durga",
        "categoryName": "Durga Gallery",
        "categorySlug": "category-durga.html",
        "god": "durga",
        "img": "images/goddess_durga_1789315573017",
        "badge": "Trending 4K",
        "shortDesc": "Fierce yet motherly Goddess Durga riding mighty golden lion, holding eight cosmic weapons with glowing divine power and red silk saree.",
        "mantra": "सर्वमङ्गलमाङ्गल्ये शिवे सर्वार्थसाधिके ।\nशरण्ये त्र्यम्बके गौरि नारायणि नमोऽस्तु ते ॥",
        "mantraMeaning": "हे नारायणी, आप सब मंगलों में मंगल, कल्याणकारी, समस्त कामनाओं को पूर्ण करने वाली और तीनों लोकों की आश्रयदात्री हैं। आपको नमस्कार है।",
        "article": """अधर्म पर धर्म की विजय की प्रतीक मां दुर्गा का सिंह वाहिनी रूप भक्तों को निर्भयता और शक्ति प्रदान करता है। अष्टभुजाओं में त्रिशूल, चक्र, धनुष-बाण आदि दिव्य अस्त्र धारण किए मां शेरावाली का यह 4K रूप अत्यंत तेजस्वी है। 

नवरात्रि के नौ दिनों और दुर्गा पूजा महोत्सव में यह वॉलपेपर लाखों श्रद्धालुओं द्वारा डाउनलोड और शेयर किया जाता है।""",
        "tags": ["maa durga 4k wallpaper", "durga sherawali image", "goddess durga lion photo", "maa durga hd download", "durga mata photo", "navratri durga image"]
    },
    {
        "id": "hanuman-sanjeevani",
        "slug": "photo-hanuman-sanjeevani.html",
        "title": "Lord Hanuman Sanjeevani Mountain 4K Wallpaper",
        "titleHi": "हनुमान जी संजीवनी पर्वत 4K वॉलपेपर",
        "category": "hanuman",
        "categoryName": "Hanuman Gallery",
        "categorySlug": "category-hanuman.html",
        "god": "hanuman",
        "img": "images/lord_hanuman_1789315589634",
        "badge": "Trending 4K",
        "shortDesc": "Mighty Lord Hanuman Bajrangbali carrying the whole Sanjeevani mountain flying through dramatic skies with divine golden strength.",
        "mantra": "अतुलितबलधामं हेमशैलाभदेहं दनुजवनकृशानुं ज्ञानिनामग्रगण्यम् ।\nसकलगुणनिधानं वानराणामधीशं रघुपतिप्रियभक्तं वातजातं नमामि ॥",
        "mantraMeaning": "अतुलनीय बल के धाम, स्वर्ण पर्वत के समान कांति वाले, ज्ञानियों में अग्रगण्य और श्री राम के प्रिय भक्त हनुमान जी को मैं शीश नवाता हूँ।",
        "article": """लक्ष्मण जी के प्राणों की रक्षा के लिए जब हनुमान जी द्रोणागिरी पर्वत को एक ही हाथ पर उठाकर आकाश मार्ग से उड़े, उस असीम पराक्रम के क्षण को इस 4K वॉलपेपर में साकार किया गया है। 

यह चित्र आत्मविश्वास, संकट से मुक्ति और आत्मबल का सबसे बड़ा प्रतीक है। संकटमोचन हनुमान जी की इस प्रतिमा को फोन में रखने से सभी विपत्तियां दूर होती हैं।""",
        "tags": ["hanuman ji 4k wallpaper", "hanuman sanjeevani photo", "bajrangbali hd image", "hanuman flying photo", "jai hanuman wallpaper", "hanuman ji full screen"]
    },
    {
        "id": "bal-gopal-original",
        "slug": "photo-bal-gopal-original.html",
        "title": "3D Cute Bal Gopal Makhan Chor 4K Wallpaper",
        "titleHi": "3D बाल गोपाल माखन चोर 4K मोबाइल वॉलपेपर",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "krishna",
        "img": "images/cute_bal_gopal_1789315873602",
        "badge": "Trending 4K",
        "shortDesc": "Super cute 3D baby Krishna Bal Gopal with butter pot and mischievous smile, peacock feather crown, and warm divine glow.",
        "mantra": "अधरं मधुरं वदनं मधुरं नयनं मधुरं हसितं मधुरम् ।\nहृदयं मधुरं गमनं मधुरं मधुराधिपतेरखिलं मधुरम् ॥",
        "mantraMeaning": "जिनके होंठ मधुर हैं, मुख मधुर है, नेत्र मधुर हैं, मुस्कान मधुर है और जिनका संपूर्ण अस्तित्व ही मधुरता का सागर है, उन मधुसूदन को प्रणाम।",
        "article": """नंदलाला बाल गोपाल का यह 3D स्वरूप इतना मनभावन है कि एक बार देखते ही हृदय आनंद से भर जाता है। मटकी से ताजा माखन खाते हुए, चेहरे पर भोली मुस्कान और आभूषणों से सजे कान्हा जी का यह चित्र हर भक्त का मन मोह लेता है।""",
        "tags": ["bal gopal 3d photo", "baby krishna makhan chor", "cute kanhaiya wallpaper", "bal gopal cute image", "krishna butter thief 3d", "nand gopal photo"]
    },
    {
        "id": "lakshmi-gold",
        "slug": "photo-lakshmi-gold.html",
        "title": "Goddess Lakshmi Gold Shower 4K Wallpaper",
        "titleHi": "मां लक्ष्मी धन वर्षा 4K वॉलपेपर",
        "category": "lakshmi",
        "categoryName": "Lakshmi Gallery",
        "categorySlug": "category-lakshmi.html",
        "god": "lakshmi",
        "img": "images/goddess_lakshmi_1789315900662",
        "badge": "Trending 4K",
        "shortDesc": "Divine Goddess Lakshmi showering gold coins from sacred pink lotus flower, with white divine elephants performing sacred abhishek.",
        "mantra": "ॐ महालक्ष्म्यै च विद्महे विष्णुपत्न्यै च धीमहि तन्नो लक्ष्मीः प्रचोदयात् ॥",
        "mantraMeaning": "भगवान विष्णु की अर्धांगिनी और समस्त ब्रह्मांड की समृद्धि की दात्री मां महालक्ष्मी हमारी बुद्धि और जीवन को आलोकित करें।",
        "article": """कमलवासिनी मां लक्ष्मी का यह स्वरूप धन, यश, सौभाग्य और पारिवारिक सुख-समृद्धि का प्रत्यक्ष आशीर्वाद है। दोनों ओर खड़े दिव्य श्वेत गज मां का जलाभिषेक कर रहे हैं और मां के करकमलों से स्वर्ण मुद्राओं की निरंतर वर्षा हो रही है। 

दीपावली, शुक्रवार व्रत और व्यापार स्थल पर यह फोटो स्थापित करना अत्यंत फलदायी माना गया है।""",
        "tags": ["maa lakshmi 4k photo", "lakshmi devi gold image", "lakshmi ji hd wallpaper", "diwali lakshmi photo", "goddess lakshmi download", "lakshmi dhan photo"]
    },
    {
        "id": "ram-ayodhya",
        "slug": "photo-ram-ayodhya.html",
        "title": "Lord Ram Ayodhya Ram Mandir 4K Wallpaper",
        "titleHi": "प्रभु श्री राम लला अयोध्या मंदिर 4K फोटो",
        "category": "ram",
        "categoryName": "Ram Gallery",
        "categorySlug": "category-ram.html",
        "god": "ram",
        "img": "images/lord_ram_1789315920936",
        "badge": "Trending 4K",
        "shortDesc": "Majestic Maryada Purushottam Lord Ram standing with divine bow in Ayodhya dham with grand Ram Mandir bathed in golden sunset light.",
        "mantra": "श्री राम राम रमेति रमे रामे मनोरमे ।\nसहस्रनाम तत्तुल्यं रामनाम वरानने ॥",
        "mantraMeaning": "श्री राम का एक बार नाम लेना भगवान विष्णु के सहस्त्र (हजार) नामों के जप के समान पुण्य फलदायी होता है।",
        "article": """अयोध्या में भव्य राम मंदिर के पृष्ठभूमि में मर्यादा पुरुषोत्तम प्रभु श्री राम का यह तेजस्वी स्वरूप करोड़ों रामभक्तों की आस्था का केंद्र है। उनके हाथ में कोदंड धनुष, मुख पर मंद मुस्कान और सूर्यवंश का दिव्य तेज इस वॉलपेपर को ऐतिहासिक और पावन बना देता है। 

रामनवमी, दीपोत्सव और प्रतिदिन 'जय श्री राम' के उद्घोष के साथ यह फोटो स्टेटस में लगाई जाती है।""",
        "tags": ["ram lalla ayodhya 4k photo", "shri ram wallpaper", "lord ram bow arrow image", "ram mandir wallpaper", "jai shri ram photo", "ayodhya ram mandir image"]
    },
    {
        "id": "saraswati-veena",
        "slug": "photo-saraswati-veena.html",
        "title": "Goddess Saraswati Veena Vadini 4K Wallpaper",
        "titleHi": "मां सरस्वती वीणा वादिनी 4K वॉलपेपर",
        "category": "saraswati",
        "categoryName": "Saraswati Gallery",
        "categorySlug": "category-saraswati.html",
        "god": "saraswati",
        "img": "images/goddess_saraswati_1789315983989",
        "badge": "Trending 4K",
        "shortDesc": "Divine Goddess Saraswati playing sacred golden veena on pure white lotus with graceful swan, peacock, and floating scriptures.",
        "mantra": "या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता ।\nया वीणावरदण्डमण्डितकरा या श्वेतपद्मासना ॥",
        "mantraMeaning": "जो कुंद के फूल, चंद्रमा और बर्फ के हार जैसी श्वेत हैं, शुभ्र वस्त्र धारण करती हैं और जिनके हाथों में वीणा सुशोभित है, वे मां भगवती मेरी रक्षा करें।",
        "article": """सा विद्या या विमुक्तये - ज्ञान की अधिष्ठात्री मां सरस्वती का यह रूप निर्मलता, सत्य और विद्या का प्रतीक है। उनके हाथ में वीणा सुर और संगीत का, वेद ज्ञान का और अक्षमाला ध्यान का प्रतीक है। विद्यार्थियों और शिक्षकों के लिए यह चित्र अत्यंत प्रेरणादायक है।""",
        "tags": ["maa saraswati 4k wallpaper", "saraswati veena photo", "goddess saraswati hd image", "saraswati puja wallpaper", "vidya devi photo", "saraswati swan lotus"]
    },
    {
        "id": "bal-ganesha-original",
        "slug": "photo-bal-ganesha-original.html",
        "title": "3D Cute Bal Ganesha with Modak 4K Wallpaper",
        "titleHi": "3D क्यूट बाल गणेश मोदक 4K फोटो",
        "category": "cute",
        "categoryName": "Cute Gallery",
        "categorySlug": "category-cute.html",
        "god": "ganesha",
        "img": "images/cute_bal_ganesha_1789316002528",
        "badge": "Trending 4K",
        "shortDesc": "Adorable 3D baby Ganesha with cute curled trunk holding sweet modak laddu, tiny golden crown, and affectionate mouse companion.",
        "mantra": "प्रणम्य शिरसा देवं गौरीपुत्रं विनायकम् ।\nभक्तावासं स्मरेन्नित्यमायुष्कामार्थसिद्धये ॥",
        "mantraMeaning": "माता पार्वती के पुत्र, विघ्नहर्ता भगवान विनायक को सिर झुकाकर प्रणाम करता हूँ। उनके स्मरण से आयु, कामना और धन की सिद्धि होती है।",
        "article": """गौरी नंदन बाल गणेश का यह 3D स्वरूप अपने हाथ में लड्डू पकड़े, चुलबुली आंखों से मुस्कुराते हुए सबका मन हर लेता है। यह वॉलपेपर घर में सुख, शांति और नन्हें बच्चों की सुरक्षा व बुद्धि के लिए अत्यंत शुभ माना जाता है।""",
        "tags": ["cute bal ganesh 3d photo", "baby ganesha wallpaper", "bal ganesh modak image", "cute ganpati 3d wallpaper", "baby elephant god photo", "ganesh chaturthi cute"]
    },
    {
        "id": "navratri-durga-special",
        "slug": "photo-navratri-durga-special.html",
        "title": "Navratri Special Maa Durga Pandal 4K Wallpaper",
        "titleHi": "नवरात्रि स्पेशल मां दुर्गा पंडाल 4K फोटो",
        "category": "festival",
        "categoryName": "Festival Special",
        "categorySlug": "category-festival.html",
        "god": "durga",
        "img": "images/navratri_durga_special",
        "badge": "Festival Special",
        "shortDesc": "Spectacular Navratri Durga Maa riding golden lion with eight glowing weapons, set in grand Durga Puja festive pandal with sacred yajna fire.",
        "mantra": "या देवी सर्वभूतेषु शक्ति-रूपेण संस्थिता ।\nनमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः ॥",
        "mantraMeaning": "जो देवी समस्त प्राणियों में शक्ति रूप में स्थित हैं, उन जगदंबा को मेरा बारंबार प्रणाम, बारंबार प्रणाम है।",
        "article": """शारदीय एवं चैत्र नवरात्रि के पावन दिनों में मां भगवती दुर्गा के इस भव्य पंडाल स्वरूप का दर्शन करोड़ों भक्तों की मनोकामनाएं पूर्ण करता है। सुनहरे सिंह पर आरूढ़ मां जगदंबा की आंखों में ममता और पापियों के संहार का तेज एक साथ दृष्टिगोचर होता है। 

नवरात्रि के 9 दिनों में प्रतिदिन इस वॉलपेपर को शेयर करने से घर-परिवार में सुख-समृद्धि और आरोग्य का वास होता है।""",
        "tags": ["navratri special maa durga image", "navratri 2026 images", "durga puja pandal photo", "maa durga navratri wallpaper", "sherawali mata navratri", "navratri day images"]
    },
    {
        "id": "navratri-nine-devi",
        "slug": "photo-navratri-nine-devi.html",
        "title": "Navdurga 9 Forms Mandala 4K Wallpaper",
        "titleHi": "नवदुर्गा 9 रूप पवित्र मंडल 4K फोटो",
        "category": "festival",
        "categoryName": "Festival Special",
        "categorySlug": "category-festival.html",
        "god": "durga",
        "img": "images/navratri_nine_devi",
        "badge": "Festival Special",
        "shortDesc": "All nine divine manifestations of Goddess Durga from Day 1 Shailputri to Day 9 Siddhidatri arranged in sacred mandala with Navratri holy colors.",
        "mantra": "प्रथमं शैलपुत्री च द्वितीयं ब्रह्मचारिणी ।\nतृतीयं चन्द्रघण्टेति कूष्माण्डेति चतुर्थकम् ॥\nपञ्चमं स्कन्दमातेति षष्ठं कात्यायनीति च ।\nसप्तमं कालरात्रीति महागौरीति चाष्टमम् ॥\nनवमं सिद्धिदात्री च नवदुर्गाः प्रकीर्तिताः ॥",
        "mantraMeaning": "शैलपुत्री, ब्रह्मचारिणी, चंद्रघंटा, कूष्मांडा, स्कंदमाता, कात्यायनी, कालरात्रि, महागौरी और सिद्धिदात्री — ये मां दुर्गा के नौ परम पावन स्वरूप हैं।",
        "article": """नवरात्रि का महापर्व मां शक्ति के नौ पावन रूपों की उपासना का पर्व है। इस अलौकिक वॉलपेपर में नवदुर्गा के सभी नौ रूपों — शैलपुत्री, ब्रह्मचारिणी, चंद्रघंटा, कूष्मांडा, स्कंदमाता, कात्यायनी, कालरात्रि, महागौरी और सिद्धिदात्री को उनके वाहनों और नौ पावन रंगों सहित एक ही चक्र में प्रदर्शित किया गया है। 

नवरात्रि के नौ दिनों में दिन-वार स्टेटस लगाने के लिए यह सबसे उपयोगी और संपूर्ण आध्यात्मिक छवि है।""",
        "tags": ["navdurga nine forms photo", "navratri 9 devi images", "navratri day 1 to 9 goddess", "nine forms durga wallpaper", "navdurga mandala image", "navratri colors today"]
    },
    {
        "id": "shiv-parivar",
        "slug": "photo-shiv-parivar.html",
        "title": "Divine Shiv Parivar Family Portrait 4K Wallpaper",
        "titleHi": "पावन शिव परिवार कैलाश दर्शन 4K वॉलपेपर",
        "category": "shiva",
        "categoryName": "Shiva Gallery",
        "categorySlug": "category-shiva.html",
        "god": "shiva",
        "img": "images/shiv_parvati_family",
        "badge": "Festival Special",
        "shortDesc": "Beautiful divine Shiv Parivar portrait on Mount Kailash - Lord Shiva, Maa Parvati, baby Ganesha eating modak, Kartikeya, and faithful Nandi bull.",
        "mantra": "नगेन्द्रहाराय त्रिलोचनाय भस्माङ्गरागाय महेश्वराय ।\nनित्याय शुद्धाय दिगम्बराय तस्मै नकाराय नमः शिवाय ॥",
        "mantraMeaning": "नागों का हार पहनने वाले, तीन नेत्रों वाले, भस्म रमाने वाले और नित्य शुद्ध महेश्वर भगवान शिव को मेरा बारंबार नमस्कार।",
        "article": """शिव परिवार संपूर्ण सृष्टि में पारिवारिक प्रेम, सामंजस्य और आध्यात्मिक पूर्णता का सर्वोच्च आदर्श है। विरोधी स्वभाव के जीव भी शिव परिवार की छत्रछाया में परम शांति से निवास करते हैं। भगवान शिव, माता पार्वती, बाल गणेश, कार्तिकेय और नंदी जी का यह चित्र घर के मुख्य द्वार या पूजा कक्ष में लगाने से गृह क्लेश समाप्त होते हैं और परिवार में अटूट प्रेम बना रहता है।""",
        "tags": ["shiv parivar photo 4k", "shiva parvati family wallpaper", "shiv parivar kailash image", "mahadev parivar photo", "shiva ganesha kartikeya", "shiv family hd image"]
    },
    {
        "id": "krishna-govardhan",
        "slug": "photo-krishna-govardhan.html",
        "title": "Lord Krishna Lifting Govardhan Hill 4K Wallpaper",
        "titleHi": "श्री कृष्ण गोवर्धन पर्वत लीला 4K फोटो",
        "category": "krishna",
        "categoryName": "Krishna Gallery",
        "categorySlug": "category-krishna.html",
        "god": "krishna",
        "img": "images/krishna_govardhan",
        "badge": "Festival Special",
        "shortDesc": "Majestic Lord Krishna lifting massive Govardhan mountain on his little pinky finger to shelter Brajwasis and cows from Indra's storm.",
        "mantra": "हे कृष्ण द्वारकावासिन् क्वासि यादवनन्दन ।\nआत्मानं मां च संत्राय गोवर्द्धनधरो भव ॥",
        "mantraMeaning": "हे द्वारकावासी, हे यदुनंदन श्री कृष्ण, गोवर्धन पर्वत को धारण कर संपूर्ण ब्रजमंडल और हम सभी शरणागतों की रक्षा करने वाले गिरधारी भगवान को नमन।",
        "article": """इंद्र के अभिमान को चूर कर ब्रज के ग्वाल-बालों और गौमाताओं की रक्षा हेतु जब सात वर्षीय कन्हैया ने विशाल गोवर्धन पर्वत को अपनी कनिष्ठिका (छोटी उंगली) पर छत्र की भांति उठा लिया था, उस अलौकिक लीला का यह 4K दृश्य है। 

गोवर्धन पूजा, अन्नकूट महोत्सव और दिवाली के अगले दिन यह फोटो करोड़ों श्रद्धालुओं द्वारा विशेष रूप से शेयर की जाती है। यह भगवान के शरणागत वत्सल स्वभाव का प्रमाण है।""",
        "tags": ["krishna govardhan photo 4k", "govardhan parvat image", "krishna lifting mountain wallpaper", "govardhan pooja image", "krishna vrindavan photo", "shri krishna leela"]
    }
]

# Categories definition
CATEGORIES = [
    {"slug": "category-cute.html", "id": "cute", "name": "Cute Gallery", "nameHi": "🧸 क्यूट गैलरी", "desc": "Adorable baby Hindu God photos - Bal Gopal, Bal Ganesh, Baby Shiva & Hanuman for WhatsApp status."},
    {"slug": "category-trending.html", "id": "trending", "name": "Trending Gods", "nameHi": "🔥 ट्रेंडिंग वॉलपेपर", "desc": "Top searched and trending 4K Ultra HD wallpapers of Hindu deities."},
    {"slug": "category-festival.html", "id": "festival", "name": "Festival Special", "nameHi": "🎉 त्यौहार स्पेशल", "desc": "Navratri, Diwali, Shivaratri & Ganesh Chaturthi divine special photos."},
    {"slug": "category-shiva.html", "id": "shiva", "name": "Mahadev Shiva", "nameHi": "🔱 भगवान शिव", "desc": "Lord Shiva Kailash meditation, Trishul, Shiv Parivar and Bholenath 4K wallpapers."},
    {"slug": "category-krishna.html", "id": "krishna", "name": "Shri Krishna", "nameHi": "🦚 श्री कृष्ण", "desc": "Lord Krishna flute in Vrindavan, Makhan Chor Bal Gopal and Govardhan Leela photos."},
    {"slug": "category-ganesha.html", "id": "ganesha", "name": "Ganpati Bappa", "nameHi": "🐘 गणपति बप्पा", "desc": "Lord Ganesha throne, cute Bal Ganesh reading book and modak 4K wallpapers."},
    {"slug": "category-hanuman.html", "id": "hanuman", "name": "Lord Hanuman", "nameHi": "🚩 संकटमोचन हनुमान", "desc": "Bajrangbali carrying Sanjeevani mountain and cute flying Bal Hanuman wallpapers."},
    {"slug": "category-durga.html", "id": "durga", "name": "Maa Durga", "nameHi": "🦁 मां दुर्गा", "desc": "Maa Sherawali lion, Navratri special pandal and Navdurga 9 forms 4K photos."},
    {"slug": "category-lakshmi.html", "id": "lakshmi", "name": "Maa Lakshmi", "nameHi": "🪷 मां लक्ष्मी", "desc": "Goddess Lakshmi gold coins shower and baby Lakshmi on lotus 4K wallpapers."},
    {"slug": "category-ram.html", "id": "ram", "name": "Shri Ram", "nameHi": "🏹 प्रभु श्री राम", "desc": "Lord Ram with bow in Ayodhya dham and Ram Mandir sunset 4K wallpapers."},
    {"slug": "category-saraswati.html", "id": "saraswati", "name": "Maa Saraswati", "nameHi": "🪕 मां सरस्वती", "desc": "Goddess Saraswati playing veena on swan and cute baby Saraswati 4K photos."}
]

print(f"Loaded {len(ITEMS)} items and {len(CATEGORIES)} categories!")
