import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8118701964:AAF6wJiIj8DCUdTIc593HZpRLzEeASWrjwk'

questions = [
    {
        "id": 1,
        "question": "O'qituvchi yangi mavzuni o'tdi shundan so'ng bilimlarni mustahkamlash maqsadida bolalar bilan savol-javob o'tkazdi. Bunday holatda o'qituvchi qaysi an'anaviy ta'lim metodidan foydalandi?",
        "options": ["Suhbat", "Tushuntirish", "Namoyish", "Amaliy"],
        "answer": "Suhbat"
    },
    {
        "id": 2,
        "question": "Bolalar bilan muloqot qilish va ularning qadr-qimmatini tan olish o'qituvchining qaysi kompetensiya standartlariga kiradi?",
        "options": ["O'quv jarayonini rejalashtirish", "Ta'lim samaradorligini ta'minlash",
                    "Tarbiyaviy faoliyatni tashkil etish", "O'zlashtirishni baholash"],
        "answer": "Tarbiyaviy faoliyatni tashkil etish"
    },
    {
        "id": 3,
        "question": "Dars mavzusiga mos keladigan namoyish va tarqatma materiallaridan foydalanish o'qituvchining qaysi kompetensiya standartlariga kiradi?",
        "options": ["O'quv jarayonini rejalashtirish", "Ta'lim samaradorligini ta'minlash",
                    "Tarbiyaviy faoliyatni tashkil etish", "O'z-o'zini rivojlantirish"],
        "answer": "Ta'lim samaradorligini ta'minlash"
    },
    {
        "id": 4,
        "question": "Ingliz tili fani o'qituvchilari maktabda ish faoliyatlarida bir-birlarini tushunib, yordam berib faoliyat olib borishlariga barcha o'qituvchilar jamoasi havas qiladilar. Ushbu holatda o'qituvchilarda refleksiyaning qanday turi namoyon bo'lmoqda?",
        "options": ["Shaxsiy refleksiya", "Kooperativ refleksiya", "Kritik refleksiya", "Individual refleksiya"],
        "answer": "Kooperativ refleksiya"
    },
    {
        "id": 5,
        "question": "Pedagogik nizolarning turlarini aniqlang: 1.Tez yakun topuvchi 2.Uzoq muddat davom etuvchi 3.Kuchsiz, sust kechadigan 4.Kuchli, tez kechadigan 5.Kuchsiz, tez kechadigan",
        "options": ["1,2,3,4", "1,2,4,5", "2,3,4,5", "1,3,4,5"],
        "answer": "1,2,3,4"
    },
    {
        "id": 6,
        "question": "O'z ustida ko'p ishlaydigan boshlang'ich sinf o'qituvchisi birxillikdan zerikib, har bir dars uchun texnologik xaritasini tuzib chiqdi va darslarini xilma-xil o'tishini ta'minladi. Ushbu vaziyatda pedagogik texnologiyaning qanday darajasi namoyon bo'lmoqda?",
        "options": ["Umumpedagogik daraja", "Xususiy metodik daraja", "Lokal daraja", "Integrativ daraja"],
        "answer": "Xususiy metodik daraja"
    },
    {
        "id": 7,
        "question": "1. Kimyo fani o'qituvchisi darsda o'quvchilarni kundalik baholab boradi. 2. Biologiya o'qituvchisi o'quv yili boshida o'quvchilar bilimini o'rganish uchun ularni baholab oladi. 3. Fizika fani o'qituvchisi o'quvchilarni semestr tugaganida baholadi. Yuqorida foydalanilgan baholash turlarini moslashtiring: a) Diagnostik, b) Formativ, c) Summativ",
        "options": ["1-a, 2-b, 3-c", "1-b, 2-a, 3-c", "1-c, 2-b, 3-a", "1-b, 2-c, 3-a"],
        "answer": "1-b, 2-a, 3-c"
    },
    {
        "id": 8,
        "question": "Ta’lim amaliyotida “pedagogik texnologiya” tushunchasi uch darajasining ketma-ketligini belgilang: 1. Umumpedagogik (makro) daraja. 2. Lokal daraja (mikro). 3. Xususiy-metodik (mezo) daraja.",
        "options": ["1,2,3", "1,3,2", "2,1,3", "3,2,1"],
        "answer": "1,3,2"
    },
    {
        "id": 9,
        "question": "Maktabda o'quvchilar o'rtasida nizoli vaziyat yuz berdi. O'qituvchi bu jarayonga barham berish uchun har ikki tomonni eshitdi va adolatli xulosa chiqardi. Bunday holat takrorlanmasligi uchun bolalar bilan o'zaro suhbatlar olib bordi. Bunday holatda o'qituvchi nizoni hal qilishning qaysi usulidan foydalandi?",
        "options": ["Ishontirish", "Arbitraj", "Muzokara", "Mediatsiya"],
        "answer": "Arbitraj"
    },
    {
        "id": 10,
        "question": "Ota-onalar majlisida ikki ona o'rtasida bolalar sababli nizo kelib chiqdi. Ular qo'pol so'zlarni ishlata boshladilar. O'qituvchi esa ularga bir-birini eshitishlarini, muloyim ohangda so'zlashishlarini talab qildi. Bunda o'qituvchi pedagogik nizoni hal qilishning qaysi usulidan foydalandi?",
        "options": ["Ishontirish", "Tushuntirish", "Talab", "Muzokara"],
        "answer": "Tushuntirish"
    },
    {
        "id": 11,
        "question": "O'qituvchi suv bug'ga aylanib havoga ko'tariladi va yana yomg'ir va qor ko'rinishida suvga aylanib yerga tushadi dedi va buni doskada chizib ko'rsatdi. Bunda o'qituvchi qaysi metoddan foydalandi?",
        "options": ["Suhbat", "Tushuntirish", "Namoyish", "Tasvir"],
        "answer": "Tushuntirish"
    },
    {
        "id": 12,
        "question": "O'qituvchi darsda yangi mavzuni tushuntirib berdi va mavzu yanada tushunarli bo'lishi uchun mavzuga oid rasmlarni doskaga ilib qo'ydi. Bunday holatda o'qituvchi qaysi an'anaviy ta'lim metodidan foydalandi?",
        "options": ["Tushuntirish", "Suhbat", "Tasvir", "Amaliy"],
        "answer": "Tasvir"
    },
    {
        "id": 13,
        "question": "Boshlang'ich sinf o'qituvchisi ota-onalar va o'qituvchilar suhbatda so'z boyligining kengligi, fikr yuritayotganda mavzuga nisbatan chuqur bilimga ega ekanligi, bilimlarini o'z tafakkuri doirasida tahlil qila olishini namoyon qildi. Suhbat jarayonida gaplarning ketma-ket bir-biriga to'g'ri kelishi va mantiqiy izchilligi hammani hayron qoldirdi. Bunda pedagog nutq xususiyatlaridan qay birini mohirona qo'llagan hisoblanadi?",
        "options": ["Nutqning aniqligi", "Nutqning mantiqiyligi", "Nutqning ta'sirchanligi", "Nutqning ravonligi"],
        "answer": "Nutqning mantiqiyligi"
    },
    {
        "id": 14,
        "question": "Davlat ta'lim standartlari va o'quv dasturlarining maqsadlariga muvofiq o'quv rejalarini ishlab chiqish o'qituvchi kasbiy kompetentligining qaysi sohasiga kiradi?",
        "options": ["Tarbiyaviy faoliyatni tashkil etish", "O'quv jarayonini rejalashtirish",
                    "Ta'lim samaradorligini ta'minlash", "O'zlashtirishni baholash"],
        "answer": "O'quv jarayonini rejalashtirish"
    },
    {
        "id": 15,
        "question": "Muayyan o'quvchining ta'lim olishdagi qiyinchiliklari to'g'risida tegishli soha mutaxassislari bilan maslahatlashish o'qituvchi kasbiy kompetentligining qaysi sohasiga kiradi?",
        "options": ["O'quv jarayonini rejalashtirish", "Ta'lim samaradorligini ta'minlash", "O'zlashtirishni baholash",
                    "Tarbiyaviy faoliyatni tashkil etish"],
        "answer": "O'zlashtirishni baholash"
    },
    {
        "id": 16,
        "question": "Geografiya fani o'qituvchisi dars mavzusini tushuntirishda yerning xaritasi va uning 3D formatidagi rasmidan foydalandi. Bunday holatda o'qituvchi qaysi metoddan foydalangan?",
        "options": ["Tushuntirish", "Suhbat", "Tasvir", "Amaliy"],
        "answer": "Tasvir"
    },
    {
        "id": 17,
        "question": "O'qituvchi o'tilgan mavzuni takrorladi va yangi mavzuni tushuntirdi so'ngra o'quvchilarni bilish o'zlashtirish darajasini aniqlash maqsadida qisqa-qisqa savollar beradi yozma ish oldi bunda o'qituvchi Blum taksonomiyasining qaysi usulidan foydalandi?",
        "options": ["Bilish", "Tushunish", "Qo'llash", "Tahlil"],
        "answer": "Qo'llash"
    },
    {
        "id": 18,
        "question": "Blum taksonomiyasi mezonlarining ketma-ketligini toping.",
        "options": ["Bilish, Tushunish, Qo‘llash, Tahlil, Sintez, Baholash",
                    "Tushunish, Bilish, Qo‘llash, Tahlil, Baholash, Sintez",
                    "Qo‘llash, Tushunish, Bilish, Sintez, Tahlil, Baholash",
                    "Bilish, Qo‘llash, Tushunish, Tahlil, Sintez, Baholash"],
        "answer": "Bilish, Tushunish, Qo‘llash, Tahlil, Sintez, Baholash"
    },
    {
        "id": 19,
        "question": "Nizoni hal qilishning qanday pedagogik usullari bor?",
        "options": ["Suhbat, Iltimos, Ishontirish, Talab", "Arbitraj, Mediatsiya, Tushuntirish, Qo'llash",
                    "Suhbat, Namoyish, Tahlil, Sintez", "Iltimos, Tushuntirish, Qo'llash, Baholash"],
        "answer": "Suhbat, Iltimos, Ishontirish, Talab"
    },
    {
        "id": 20,
        "question": "Bilimdon pedagogga xos sifatlarni aniqlang:",
        "options": ["1,2,3", "1,2,4", "2,3,4", "1,3,4"],
        "answer": "1,2,3"
    },
    {
        "id": 21,
        "question": "Refleksiya so’zining ma’nosi nima?",
        "options": ["Ortga qaytish, aks etish", "Tahlil qilish, sintez qilish", "O'zlashtirish, qo'llash",
                    "Motivatsiya, ilhomlantirish"],
        "answer": "Ortga qaytish, aks etish"
    },
    {
        "id": 22,
        "question": "Pedagogik taktga to’g’ri ta’rif berilgan qatorni toping",
        "options": ["O'qituvchining bilim darajasi", "Pedagogning axloqiy tamoyillarga rioya qilishi",
                    "O'quvchilarning faolligini oshirish", "Darsni rejalashtirish qobiliyati"],
        "answer": "Pedagogning axloqiy tamoyillarga rioya qilishi"
    },
    {
        "id": 23,
        "question": "Yig'ilishda bir o'qituvchi pedagogik mahorati yuqori ekanligi haqida gapirdi. Yosh mutaxassis esa o'z fanini chuqur bilishi, ammo pedagogik mahorati yetishmasligini aytib, u nimalardan iborat bo'lishini so'radi. Quyida 'Pedagogik mahorat' tushunchasi ta'rifini qamrab olgan javoblarni belgilang.",
        "options": ["1,2,3,4", "1,2,3", "2,3,4", "1,3,4"],
        "answer": "1,2,3,4"
    },
    {
        "id": 24,
        "question": "O’qituvchi yangi darsni o’tishdan oldin o’quvchilarning bilimlarini quiz test orqali sinab ko’rdi. Bunday holatda o’qituvchi baholashning qaysi turidan foydalangan?",
        "options": ["Formativ", "Summativ", "Diagnostik", "Integrativ"],
        "answer": "Diagnostik"
    },
    {
        "id": 25,
        "question": "O’qituvchi o’z fikrlarini o’quvchilarga aniq va ta’sirchan yetkazib bera olishi uchun unda qanday sifatlar bo’lishi kerak?",
        "options": ["Nutqning ravonligi va notiqlik", "Bilimning chuqurligi", "Tashkiliy qobiliyat",
                    "Texnologik ko'nikmalar"],
        "answer": "Nutqning ravonligi va notiqlik"
    },
    {
        "id": 26,
        "question": "Yuqori sinflarga ilk marotaba darsga kirgan o’qituvchi dastlab o’quvchilarning qiziqishlari haqida so’radi. O’qituvchi nima maqsadda bu ishni amalga oshirdi?",
        "options": ["O'quvchilarni motivatsiyalash", "Darsni rejalashtirish", "Bilimni baholash", "Tarbiyaviy maqsad"],
        "answer": "O'quvchilarni motivatsiyalash"
    },
    {
        "id": 27,
        "question": "Moslashtiring: 1) Bilim 2) Ko’nikma 3) Malaka",
        "options": ["1-a, 2-b, 3-c", "1-b, 2-a, 3-c", "1-c, 2-b, 3-a", "1-a, 2-c, 3-b"],
        "answer": "1-a, 2-b, 3-c"
    },
    {
        "id": 28,
        "question": "Moslashtiring: 1) Pedagogik jarayon 2) Maqsad",
        "options": ["1-a, 2-c", "1-b, 2-a", "1-c, 2-b", "1-a, 2-b"],
        "answer": "1-a, 2-c"
    },
    {
        "id": 29,
        "question": "Moslashtiring: 1) Masofaviy ta'lim 2) Noan'anaviy ta'lim",
        "options": ["1-a, 2-b", "1-b, 2-a", "1-c, 2-b", "1-a, 2-c"],
        "answer": "1-a, 2-b"
    },
    {
        "id": 30,
        "question": "Tarbiyaning qaysi turini olib borish jarayonida o'qituvchi o'quvchilarda estetik his-tuyg'u, estetik didni tarbiyalaydi, ularning ijodiy qobiliyatlarini rivojlantiradi?",
        "options": ["Aqliy tarbiya", "Estetik tarbiya", "Huquqiy tarbiya", "Jismoniy tarbiya"],
        "answer": "Estetik tarbiya"
    },
    {
        "id": 31,
        "question": "Tarbiyaning qaysi turi yo‘lga qo‘yish asosida o‘quvchilarni ilm-fan, texnika va texnologiya borasida qo‘lga kiritilayotgan yutuqlardan boxabar etadi?",
        "options": ["Estetik tarbiya", "Aqliy tarbiya", "Huquqiy tarbiya", "Jismoniy tarbiya"],
        "answer": "Aqliy tarbiya"
    },
    {
        "id": 32,
        "question": "O'qituvchi o'tilgan mavzuni takrorladi va yangi mavzuni tushuntirdi so'ngra o'quvchilarni bilish o'zlashtirish darajasini aniqlash maqsadida qisqa-qisqa savollar beradi yozma ish oldi bunda o'qituvchi Blum taksonomiyasining qaysi usulidan foydalandi?",
        "options": ["Bilish", "Tushunish", "Qo’llash", "Tahlil"],
        "answer": "Qo’llash"
    },
    {
        "id": 33,
        "question": "O’qituvchi darslarini fanlararo kompetensiyalar predmetining korrelyatsiya va integratsiya tamoyillarini inobatga olgan holda o’tadi bunday holatda kasbiy kompetentlikning qaysi sohasini amalga oshirgan hisoblanadi?",
        "options": ["Ta'lim samaradorligini ta'minlash", "O'quv jarayonini rejalashtirish", "O'zlashtirishni baholash",
                    "Tarbiyaviy faoliyatni tashkil etish"],
        "answer": "O'quv jarayonini rejalashtirish"
    },
    {
        "id": 34,
        "question": "O’qituvchi yangi mavzularni tushuntirib bo’lgach bolalarning bilimlarini TEST QUIZ yordamida tekshirib ko’radi. Bunday holatda o’qituvchi kasbiy kompetentlik qaysi mehnat vazifasini bajargan hisoblanadi?",
        "options": ["O'quv jarayonini rejalashtirish", "Ta'lim samaradorligini ta'minlash",
                    "Ta’lim natijalarini baholash", "Tarbiyaviy faoliyatni tashkil etish"],
        "answer": "Ta’lim natijalarini baholash"
    },
    {
        "id": 35,
        "question": "Tarbiya jarayonining qonuniyatlarini aniqlang",
        "options": ["1,2,3,4", "1,2,3", "2,3,4", "1,3,4"],
        "answer": "1,2,3,4"
    },
    {
        "id": 36,
        "question": "Didaktik o’yin metodiga to’g’ri ta’rif berilgan qatorni toping",
        "options": ["O'quvchilarning faolligini oshirish", "Bilimlarni mustahkamlashga yordam beradi",
                    "Tushuntirish va tasvir usuli", "Amaliy faoliyatni tashkil etish"],
        "answer": "Bilimlarni mustahkamlashga yordam beradi"
    },
    {
        "id": 37,
        "question": "4K modelining tartibini toping",
        "options": ["1,2,3,4", "2,1,3,4", "3,2,1,4", "4,3,2,1"],
        "answer": "2,1,3,4"
    },
    {
        "id": 38,
        "question": "Darsga tayyorgarlik qaysi bosqichda o‘qituvchi dars o‘tkaziladigan sharoitlarni chuqur tahlil qiladi?",
        "options": ["Rejalashtirish", "Tashxislash", "Bashoratlash", "Loyihalash"],
        "answer": "Tashxislash"
    },
    {
        "id": 39,
        "question": "Darsga tayyorgarlikning qaysi bosqichda darsning turli variantlari ko‘rib chiqiladi?",
        "options": ["Tashxislash", "Bashoratlash", "Loyihalash", "Rejalashtirish"],
        "answer": "Bashoratlash"
    },
    {
        "id": 40,
        "question": "Darsga tayyorgarlikning bosqichda o‘qituvchi darsning strukturasi va asosiy vazifalarini rejalashtiradi?",
        "options": ["Tashxislash", "Bashoratlash", "Loyihalash", "Rejalashtirish"],
        "answer": "Loyihalash"
    },
    {
        "id": 41,
        "question": "Ikki o'quvchi sinfda urushib qoldi. O'qituvchi nizoga aralashib qarama-qarshi tomonlarni asosli, aniq faktlar asosida kelishtirdi. Bunday holatda o'qituvchi nizoni hal qilishning qaysi usulidan foydalandi?",
        "options": ["Arbitraj", "Ishontirish", "Muzokara", "Mediatsiya"],
        "answer": "Ishontirish"
    },
    {
        "id": 42,
        "question": "Ota-onalar majlisida ikki ona o'rtasida bolalar sababli nizo kelib chiqdi. O'qituvchi ularga muloyim ohangda so'zlashishlarini, aks holda qattiq chora ko’rishi bilan ogohlantirdi. Bunda o'qituvchi pedagogik nizoni hal qilishning qaysi usulidan foydalandi?",
        "options": ["Tushuntirish", "Talab", "Ishontirish", "Muzokara"],
        "answer": "Talab"
    },
    {
        "id": 43,
        "question": "O'qituvchilar xonasida ikki o'qituvchi o'rtasida kelishmovchilik paydo bo'ldi. Tajribali o'qituvchi ularga bir-birlarini eshitib nizoga birgalikda barham berishlarini aytdi. Bunday holatda nizoni hal qilishning qaysi usulidan foydalanildi?",
        "options": ["Arbitraj", "Muzokara", "Suhbat", "Mediatsiya"],
        "answer": "Suhbat"
    },
    {
        "id": 44,
        "question": "Sinfdagi ba'zi bolalar o'zlashtirishdan orqada. Bunday holatda o'qituvchi bolalardagi muammoni bartaraf etish uchun qanday mehnat harakatini amalga oshirishi kerak?",
        "options": ["Differensial yordam berish", "Motivatsiya qilish", "Summativ baholash", "Darsni rejalashtirish"],
        "answer": "Differensial yordam berish"
    },
    {
        "id": 45,
        "question": "Matematika fani o'qituvchisi darsda o'quvchilar zerikib qolayotganini sezdi. U bolalarni darsga bo'lgan qiziqishlarini qayta uyg'otish uchun turli texnologiyalardan foydalandi. Bunday holatda o'qituvchi kasbiy kompetentlikning qaysi mehnat harakatini bajargan hisoblanadi?",
        "options": ["O'quv dasturini moslashtirish", "Darsni rejalashtirish", "Summativ baholash",
                    "Tarbiyaviy faoliyat"],
        "answer": "O'quv dasturini moslashtirish"
    },
    {
        "id": 46,
        "question": "Direktor o'rinbosari yosh mutaxassisning darslarini nazorat qildi. Yosh mutaxassis har bir o'quvchiga mos vazifalar taqsimlab, yangi mavzuni tushunarli qildi. Shunda o'qituvchi ta'lim samaradorligini ta'minlash uchun qanday ko'nikmalarni namoyon etadi?",
        "options": ["Dars vaqtini boshqarish", "Motivatsiya qilish", "Tarbiyaviy faoliyat", "Diagnostik baholash"],
        "answer": "Dars vaqtini boshqarish"
    },
    {
        "id": 47,
        "question": "O‘qituvchi “Yerning tuzilishi” mavzusini o‘rgatishda darslikdagi rasmlar, atlas xarita, slayd va diagrammalardan foydalandi. Bu holatda o‘qituvchi qaysi metoddan foydalangan?",
        "options": ["Tushuntirish", "Suhbat", "Ilyustratsiya", "Amaliy"],
        "answer": "Ilyustratsiya"
    },
    {
        "id": 48,
        "question": "O'qituvchi dars samaradorligini ta'minlash uchun o'z darslarida Blum taksonomiyasidan foydalanishni reja qildi. O'qituvchi Blum taksonomiyasidan foydalanishda qanday ishlarni amalga oshirishi kerak?",
        "options": ["Bilish, tushunish, qo'llash, tahlil", "Motivatsiya, tushuntirish, namoyish",
                    "Suhbat, tasvir, amaliy", "Rejalashtirish, loyihalash, tashxislash"],
        "answer": "Bilish, tushunish, qo'llash, tahlil"
    },
    {
        "id": 49,
        "question": "7-sinf Tarix fani o‘qituvchisi o‘quvchilarini tarix fanidan darslikka qiziqmayotganini sezdi. O'qituvchi darsni qiziqarli qilish uchun nima qilish lozim?",
        "options": ["Guruhli o‘yinlar tashkil etish", "Summativ baholash", "Darsni rejalashtirish",
                    "Tushuntirish usuli"],
        "answer": "Guruhli o‘yinlar tashkil etish"
    },
    {
        "id": 50,
        "question": "Ingliz tili fani o'qituvchisi o'z darslarini yanada qiziqarli qilish uchun 'Interactive' metodini o'rganib uni darslariga joriy qildi. Bunday holatda o'qituvchi qaysi mehnat ko‘nikmasini amalga oshiradi?",
        "options": ["Yangi bilimlarni qo‘llash", "Darsni rejalashtirish", "Tarbiyaviy faoliyat", "Diagnostik baholash"],
        "answer": "Yangi bilimlarni qo‘llash"
    },
    {
        "id": 51,
        "question": "Ustoz Saida opa doimiy ravishda faniga doir jurnallarni o‘qib, bilimlarini darslarida qo‘llab boradi. Bunda u qaysi mehnat ko‘nikmasini amalga oshiradi?",
        "options": ["Yangi bilimlarni qo‘llash", "O'quv jarayonini rejalashtirish", "Summativ baholash",
                    "Tarbiyaviy fahimselfiyat"],
        "answer": "Yangi bilimlarni qo‘llash"
    },
    {
        "id": 52,
        "question": "7 sinf o‘qituvchisi bir o‘quvchisining o‘zlashtirishini tahlil qilish uchun psixolog va metodist bilan maslahatlashdi. Bunday holatda o'qituvchi qanday mehnat harakatini amalga oshirgan?",
        "options": ["Mutaxassislar bilan maslahatlashish", "Darsni rejalashtirish", "Motivatsiya qilish",
                    "Tarbiyaviy faoliyat"],
        "answer": "Mutaxassislar bilan maslahatlashish"
    },
    {
        "id": 53,
        "question": "Sinfdagi bir o'quvchi savollarga javob berishda ustunlik qiladi. Bunday holatni oldini olish uchun o'qituvchi qanday yo'l tutishi kerak?",
        "options": ["Barchaga javob berish imkoniyatini berish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Barchaga javob berish imkoniyatini berish"
    },
    {
        "id": 54,
        "question": "Agar pedagog o’quvchilarda o’zlari haqida fikr yuritishga yordam bersa, guruhiy loyihalar orqali shaxsning dunyoqarashini tushunishga yordam bersa, tarbiyachilik mahorati tizimining qaysi tarkibiy qismini amalga oshirgan bo’ladi?",
        "options": ["O’zini-o’zi anglash", "Motivatsiya qilish", "Tarbiyaviy faoliyat", "Darsni rejalashtirish"],
        "answer": "O’zini-o’zi anglash"
    },
    {
        "id": 55,
        "question": "Oʻqituvchi xato qilgan oʻquvchilarga salbiy fikir bildirsa ularning fanga boʻlgan qiziqishi pasayib ketayotganligini sezdi, bu holatda oʻqituvchi nima qilishi kerak?",
        "options": ["Xatoni tushuntirish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Xatoni tushuntirish"
    },
    {
        "id": 56,
        "question": "Geografiya fani o‘qituvchisi vulqon va uning turlari haqida ma‘lumot berdi. Darsni yanada qiziqarli bo‘lishi uchun vulqon otilishini 3D formatda namoyish etdi. O‘qituvchi qaysi metoddan foydalandi?",
        "options": ["Tushuntirish", "Suhbat", "Namoyish", "Amaliy"],
        "answer": "Namoyish"
    },
    {
        "id": 57,
        "question": "O'qituvchi tumandagi boshqa maktabga borib tajribali o'qituvchining darsini kuzatdi. O'rgangan bilimlarini o'z darslarida qo'lladi. Bunday holatda o'qituvchi qaysi vazifani bajardi?",
        "options": ["O'zaro darslarda qatnashish", "Darsni rejalashtirish", "Motivatsiya qilish",
                    "Tarbiyaviy faoliyat"],
        "answer": "O'zaro darslarda qatnashish"
    },
    {
        "id": 58,
        "question": "O'qituvchi o‘quvchilarga uyga vazifa sifatida bir maqol berdi. O‘quvchilar maqolni birgalikda sahna ko‘rinishi qilib tayyorlashdi. Bunday holatda o'qituvchi qaysi metodni samarali qo'llandi?",
        "options": ["Loyiha ishi", "Suhbat", "Tushuntirish", "Namoyish"],
        "answer": "Loyiha ishi"
    },
    {
        "id": 59,
        "question": "O'qituvchi yangi mavzuni tushuntirib bergach sinfdagi o'quvchilarni guruhlarga bo'ldi. Doskaga jadval chizib uni mavzuga oid ma'lumotlar bilan to'ldirishlarini so'radi. O'qituvchi bergan topshiriq Blum taksonomiyasining qaysi darajasida qo'llaniladi?",
        "options": ["Bilish", "Tushunish", "Qo'llash", "Tahlil"],
        "answer": "Tushunish"
    },
    {
        "id": 60,
        "question": "Respublika pedagogika fani doktor o'qituvchilari yangi ta'lim metodini ishlab chiqdilar va amaliyotga tatbiq qildilar.",
        "options": ["Umumpedagogik daraja", "Xususiy metodik daraja", "Lokal daraja", "Integrativ daraja"],
        "answer": "Umumpedagogik daraja"
    },
    {
        "id": 61,
        "question": "Maktab rahbari o'qituvchilar har bir dars soatida o'tadigan mavzusini texnologik xaritasi va modelini tuzib kelishi shartligini aytdi.",
        "options": ["Umumpedagogik daraja", "Xususiy metodik daraja", "Lokal daraja", "Integrativ daraja"],
        "answer": "Xususiy metodik daraja"
    },
    {
        "id": 62,
        "question": "Yozgi tatil vaqtida boshlang'ich ta'lim o'qituvchisi tayyorlov guruhlarida ishtirok etdi. O'quvchilarning mantiqiy fikrlashini shakllantirish texnologiyalarini qo'lladi. Bunda pedagogik texnologiyaning qaysi darajasi namoyon bo'lmoqda?",
        "options": ["Umumpedagogik daraja", "Xususiy metodik daraja", "Lokal daraja", "Integrativ daraja"],
        "answer": "Lokal daraja"
    },
    {
        "id": 63,
        "question": "Qaysi kompetensiyaning mehnat harakatlari berilgan? 1. Oʻquvchilar taʼlim jarayonida toʻqnashgan qiyinchiliklarini kuzatish va qayd etish 2. Taʼlim natijalarini diagnostika qilish uchun turli usul va vositalardan foydalanish 3. Muayyan oʻquvchining taʼlim olishdagi qiyinchiliklari toʻgʻrisida mutaxassislar bilan maslahatlashish",
        "options": ["1,2,3", "1,2", "2,3", "1,3"],
        "answer": "1,2,3"
    },
    {
        "id": 64,
        "question": "O'qituvchi tumandagi boshqa maktabga borib tajribali o'qituvchining darsini kuzatdi. O'rgangan bilimlarini o'z darslarida qo'lladi. Bunday holatda o'qituvchi qaysi vazifani bajardi?",
        "options": ["O'zaro darslarda qatnashish", "Darsni rejalashtirish", "Motivatsiya qilish",
                    "Tarbiyaviy faoliyat"],
        "answer": "O'zaro darslarda qatnashish"
    },
    {
        "id": 65,
        "question": "O’qituvchi dars jarayonida turli xil tarqatma materiallari va rag’batlardan foydalandi, bu o’quvchilarni darsga yanada qiziqishlarini orttirdi. O’qituvchi bu orqali ta'lim samaradorligini ta'minlashning qaysi mehnat harakatlarini amalga oshirgan?",
        "options": ["Turli usullardan foydalanish", "Darsni rejalashtirish", "Summativ baholash",
                    "Tarbiyaviy faoliyat"],
        "answer": "Turli usullardan foydalanish"
    },
    {
        "id": 66,
        "question": "Moslashtiring: 1. Diapazon 2. Artikulyatsiya",
        "options": ["1-a, 2-c", "1-b, 2-a", "1-c, 2-b", "1-a, 2-b"],
        "answer": "1-a, 2-c"
    },
    {
        "id": 67,
        "question": "Moslashtiring: 1. Tembr 2. Ritmika",
        "options": ["1-a, 2-b", "1-b, 2-a", "1-c, 2-b", "1-a, 2-c"],
        "answer": "1-a, 2-b"
    },
    {
        "id": 68,
        "question": "10 sinf tarix o'qituvchisi qo'shni maktabdan yangi metod o'rganib, Google Earth-dan foydalanib mavzu haqida ma'lumot olishni o'rgatdi. Bunda u qaysi mehnat harakatlarini bajardi?",
        "options": ["O'z-o'zini rivojlantirish", "Darsni rejalashtirish", "Motivatsiya qilish", "Tarbiyaviy faoliyat"],
        "answer": "O'z-o'zini rivojlantirish"
    },
    {
        "id": 69,
        "question": "Nizoni bartaraf etish ketma-ketligini tartiblang: 1. Tahlil qilinadi 2. Nizo sabablari tinglanadi 3. Aniqlik kiritiladi 4. Vaziyatga baho beriladi 5. Yechim topiladi",
        "options": ["1,2,3,4,5", "2,3,1,5,4", "3,2,1,4,5", "5,4,3,2,1"],
        "answer": "2,3,1,5,4"
    },
    {
        "id": 70,
        "question": "Maktabning rus tili fani o'qituvchisi xulq va odob qoidalariga rioya qilishi bilan ajralib turadi. O'qituvchining 'Pedagogik nazokat'ning uzluksizligini ta'minlovchi omillarni sanang.",
        "options": ["1,2,3", "1,3,4", "2,3,4", "1,2,4"],
        "answer": "1,3,4"
    },
    {
        "id": 71,
        "question": "Agar bolalar ingliz tilidagi so‘zlarni to‘g‘ri qo‘llay olmasa, o‘qituvchi qanday yondashuvni qo‘llaydi?",
        "options": ["To‘g‘ri talaffuzni ko‘rsatish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "To‘g‘ri talaffuzni ko‘rsatish"
    },
    {
        "id": 72,
        "question": "O'qituvchi darsni boshlashdan avval savol-javob shaklida darsini boshlab oldi. O'qituvchi qaysi metoddan foydalandi?",
        "options": ["Suhbat", "Tushuntirish", "Namoyish", "Amaliy"],
        "answer": "Suhbat"
    },
    {
        "id": 73,
        "question": "O’qituvchi mimik harakatlar orqali qanday ishlarni amalga oshiradi?",
        "options": ["Yuz muskullari harakati", "Talaffuzni aniqlash", "Motivatsiya qilish", "Darsni rejalashtirish"],
        "answer": "Yuz muskullari harakati"
    },
    {
        "id": 74,
        "question": "“Pedagogning kasbiy faoliyatni mavjud ijtimoiy talablar, huquqiy me’yorlar va standartlarga muvofiq tashkil etish qobiliyati hamda kasbiy tayyorgarlik darajasi.”",
        "options": ["Pedagogik bilimdonlik", "Tarbiyaviy faoliyat", "O'quv jarayonini rejalashtirish",
                    "Ta'lim samaradorligi"],
        "answer": "Pedagogik bilimdonlik"
    },
    {
        "id": 75,
        "question": "Moslashtiring: 1) Material ta’lim vositalari 2) Ideal ta’lim vositalari",
        "options": ["1-a, 2-c", "1-b, 2-a", "1-c, 2-b", "1-a, 2-b"],
        "answer": "1-a, 2-c"
    },
    {
        "id": 76,
        "question": "Moslashtiring: 1) O‘rgatish vositalari 2) O‘rganish vositalari",
        "options": ["1-a, 2-b", "1-b, 2-a", "1-c, 2-b", "1-a, 2-c"],
        "answer": "1-a, 2-b"
    },
    {
        "id": 77,
        "question": "Bir o'quvchi ona tilidagi maqollarni ingliz tilida noo'rin qo'llab keladi. O'qituvchi bunday holatda nima qilishi kerak?",
        "options": ["Tushuntirish va izohlash", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Tushuntirish va izohlash"
    },
    {
        "id": 78,
        "question": "Tarbiyaning qaysi turini tashkil etish jarayonida o‘quvchilarga davlatimiz Konstitusiyasi, fuqarolik, oila, mehnat huquqlari tushuntiriladi?",
        "options": ["Estetik tarbiya", "Aqliy tarbiya", "Huquqiy tarbiya", "Jismoniy tarbiya"],
        "answer": "Huquqiy tarbiya"
    },
    {
        "id": 79,
        "question": "Blum taksonomiyasining qaysi darajasidagi tafakkurga ega bo‘lganda o‘quvchi faktlar, qoidalar, chizmalarni tushunadi, qayta tuza oladi?",
        "options": ["Bilish", "Tushunish", "Qo'llash", "Tahlil"],
        "answer": "Tushunish"
    },
    {
        "id": 80,
        "question": "Pedagogik relaksatsiya turlarini aniqlang?",
        "options": ["1,2,3", "1,2,4", "2,3,4", "1,3,4"],
        "answer": "1,2,3"
    },
    {
        "id": 81,
        "question": "6-sinf o‘quvchilarning o‘zlashtirishi pasayib ketdi. Sinf rahbari ota-onalarga qo‘ng‘iroq qilib, treninglar o‘tkazdi. Bunday holatda o'qituvchi qaysi mehnat vazifasini bajargan?",
        "options": ["Ota-onalarni jalb qilish", "Darsni rejalashtirish", "Motivatsiya qilish", "Summativ baholash"],
        "answer": "Ota-onalarni jalb qilish"
    },
    {
        "id": 82,
        "question": "Agar qoidalarga asoslangan strukturaviy o'rganishni afzal ko'ruvchi o'quvchi muloqotga asoslangan topshiriqlarni bajarishga qiynalayotgan bo'lsa, o'qituvchi nima qilishi kerak?",
        "options": ["Muloqotning ahamiyatini tushuntirish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Muloqotning ahamiyatini tushuntirish"
    },
    {
        "id": 83,
        "question": "Agar o'quvchilar xorijiy til bilimlari cheklanganligi sababli guruh muhokamalarida ona tillaridan foydalanishni so'rasa, eng maqul yo'l qaysi?",
        "options": ["Ona tili qoidalarini o'rnatish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Ona tili qoidalarini o'rnatish"
    },
    {
        "id": 84,
        "question": "Agar o'quvchining grammatik bilimlari kuchli bo‘lsa, lekin og'zaki muloqotda qiynalsa, o'qituvchi qanday yondashishi kerak?",
        "options": ["Real hayotiy muloqot amaliyoti", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Real hayotiy muloqot amaliyoti"
    },
    {
        "id": 85,
        "question": "O'qituvchi o'quvchilarning o'qish darsidagi tanqidiy fikrlash ko'nikmalarini baholash uchun Blum Taksonomiyasini qo'llamoqchi. Bunga qaysi yondashuv samarali?",
        "options": ["Matnni tahlil qilish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Matnni tahlil qilish"
    },
    {
        "id": 86,
        "question": "O'quvchining yozish ko'nikmalarini baholash uchun topshiriq tanlashda o'qituvchi nimalarga e'tibor berishi kerak?",
        "options": ["Dars maqsadlari va bilim darajasi", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Dars maqsadlari va bilim darajasi"
    },
    {
        "id": 87,
        "question": "O'qituvchi o'quvchilarning o'qish darsidagi tanqidiy fikrlash ko'nikmalarini baholash uchun Blum Taksonomiyasini qo'llamoqchi. Bunga qaysi yondashuv samarali?",
        "options": ["Matnni tahlil qilish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Matnni tahlil qilish"
    },
    {
        "id": 88,
        "question": "Oraliq nazorat davomida o'qituvchi o'quvchilarining gapirish ko'nikmalarini baholamoqchi. Bu vaziyatda u samarali taqriz berish uchun qanday yondashuvni qo'llashi kerak?",
        "options": ["Intervyu formati", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Intervyu formati"
    },
    {
        "id": 89,
        "question": "Rasmiy elektron xat yozish bo'yicha ketma-ket darslarni rejalashtirayotganda nima qilish kerak?",
        "options": ["Namuna tahlilidan boshlash", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Namuna tahlilidan boshlash"
    },
    {
        "id": 90,
        "question": "Agar o'quvchilar grammatika mavzusini tushunishda qiynalishsa, nima qilish kerak?",
        "options": ["Kontekstda namuna ko‘rsatish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Kontekstda namuna ko‘rsatish"
    },
    {
        "id": 91,
        "question": "Agar o'quvchilar darslikdan foydalanishda ishtiyoqni yo'qotishsa, nima qilish kerak?",
        "options": ["Qo'shimcha materiallar qo'shish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Qo'shimcha materiallar qo'shish"
    },
    {
        "id": 92,
        "question": "Agar o'quvchilar yangi grammatik qoidani tushunishda qiynalayotgan bo'lsa, o'qituvchi nima qilishi kerak?",
        "options": ["Mavzuga mos misol keltirish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Mavzuga mos misol keltirish"
    },
    {
        "id": 93,
        "question": "O'qituvchi ko'rsatmalar berayotganda tana a'zolari harakati va mimikadan qanday foydalanishi kerak?",
        "options": ["Imo-ishoralar bilan mustahkamlash", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Imo-ishoralar bilan mustahkamlash"
    },
    {
        "id": 94,
        "question": "Lug'at o'rgatish uchun o'qituvchiga o'quv qurolini tanlashda eng muhim omil nima?",
        "options": ["Tushunishga yordam berishi", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Tushunishga yordam berishi"
    },
    {
        "id": 95,
        "question": "O'zaro fikr-mulohaza almashish jarayonida, o'quvchi boshqa bir o'quvchining insho matnida paragraflar tartibining aniqligi yo'qligini ko'rsatib o'tmoqda. O'qituvchi taqriz berayotgan o'quvchining fikrini qanday nazorat qilishi kerak?",
        "options": ["Kuchli va zaif tomonlarni aytish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Kuchli va zaif tomonlarni aytish"
    },
    {
        "id": 96,
        "question": "Agar o'quvchi guruh muhokamasida so'zlar talaffuzida xatoga yo'l qo'yib, bundan xabarsiz bo'lsa, o'qituvchi nima qilishi kerak?",
        "options": ["Fonemik jadvaldan foydalanish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Fonemik jadvaldan foydalanish"
    },
    {
        "id": 97,
        "question": "O'qituvchi guruh loyiha ishi topshirig'ida bir o'quvchi ustunlik qilayotganini sezdi. Bu holatni bartaraf qilishning eng yaxshi usuli qanday?",
        "options": ["Rollarni belgilash", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Rollarni belgilash"
    },
    {
        "id": 98,
        "question": "Agar o'quvchi o'qitilayotgan fan uning kelajakdagi kasbiy maqsadlariga mos kelmasligini his qilib, ishtiyoqini yo'qotayotgan bo'lsa, o'qituvchi nima qilishi kerak?",
        "options": ["Fanning foydaliligini tushuntirish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Fanning foydaliligini tushuntirish"
    },
    {
        "id": 99,
        "question": "O'qituvchi o'quvchilarning sinfda ko'proq muloqot qilishiga yordam berish uchun so'z orqali qanday ta'sir o'tkazishi mumkin?",
        "options": ["Ijobiy fikr-mulohaza berish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Ijobiy fikr-mulohaza berish"
    },
    {
        "id": 100,
        "question": "O'qituvchi guruhlarda ishlash vaqtida o'quvchilar ona tilida gaplashayotganini kuzatdi. Ularni xorijiy tildan foydalanishga undash uchun nima qilishi kerak?",
        "options": ["Sinf ifodalarini ko'rsatish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Sinf ifodalarini ko'rsatish"
    },
    {
        "id": 101,
        "question": "Agar o'quvchi muhokamalarda boshqalarni cheklayotgan bo'lsa, o'qituvchi nima qilishi kerak?",
        "options": ["Qoidalarni taqdim qilish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Qoidalarni taqdim qilish"
    },
    {
        "id": 102,
        "question": "Agar o'qituvchi salbiy izohlar o'quvchilarning ishtiyoqini pasaytirayotganini bilsa, fikr-mulohazalarini qanday o'zgartirishi kerak?",
        "options": ["Me'yoriy baholash", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Me'yoriy baholash"
    },
    {
        "id": 103,
        "question": "Guruh loyihasida o'quvchi shaxsiy kelishmovchiliklar sababli ishlashdan bosh tortdi. O'qituvchi qanday yo'l tutishi kerak?",
        "options": ["Suhbat o'tkazish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Suhbat o'tkazish"
    },
    {
        "id": 104,
        "question": "Agar o'quvchilar yangi so'zlarni og'zaki nutqda qo'llashda qiynalayotganini o'qituvchi sezsa, nima qilishi kerak?",
        "options": ["Qo'shimcha mashq rejalashtirish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Qo'shimcha mashq rejalashtirish"
    },
    {
        "id": 105,
        "question": "Quyida qayd etilgan tamoyillar o'qituvchining 'O'quv jarayonini rejalashtirish' mehnat vazifalarining qaysi mehnat harakatlariga tegishli?",
        "options": ["O'quv rejalarini ishlab chiqish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "O'quv rejalarini ishlab chiqish"
    },
    {
        "id": 106,
        "question": "Quyida qayd etilgan talablar o'qituvchining 'Ta'lim samaradorligini ta'minlash' mehnat vazifalarining qaysi mehnat harakatlariga tegishli?",
        "options": ["Erishimli vazifalarni belgilash", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Erishimli vazifalarni belgilash"
    },
    {
        "id": 107,
        "question": "Quyida qayd etilgan talablar o'qituvchining 'Ta'lim samaradorligini ta'minlash' mehnat vazifalarining qaysi mehnat harakatlariga tegishli?",
        "options": ["O'z g'oyalarini ifoda etish imkoniyati", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "O'z g'oyalarini ifoda etish imkoniyati"
    },
    {
        "id": 108,
        "question": "Quyida qayd etilgan talablar o'qituvchining 'Ta'lim samaradorligini ta'minlash' mehnat vazifalarining qaysi mehnat harakatlariga tegishli?",
        "options": ["Differensial yordam berish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Differensial yordam berish"
    },
    {
        "id": 109,
        "question": "Pedagog dars davomida test va 'Quizizz' yordamida o'quvchilarning tushunchalarini aniqlab, sharhlar berdi. Bunda pedagog qaysi mehnat harakatlarini amalga oshirgan?",
        "options": ["Turli usullardan foydalanish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Turli usullardan foydalanish"
    },
    {
        "id": 110,
        "question": "Pedagog bir o'quvchisining ta'lim olish va xulq-atvoridagi muammolarini aniqlash uchun izlanishlar olib bordi. Bunda pedagog qaysi mehnat harakatlarini amalga oshirgan?",
        "options": ["Hamkasblar bilan maslahatlashish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Hamkasblar bilan maslahatlashish"
    },
    {
        "id": 111,
        "question": "Pedagog o'quvchilarining mavzuni tushunishda qanday muammolarga duch kelayotganliklarini tushunishga harakat qildi. Bunda pedagog qaysi mehnat harakatlarini amalga oshirgan?",
        "options": ["Qiyinchiliklarni kuzatish", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Qiyinchiliklarni kuzatish"
    },
    {
        "id": 112,
        "question": "Ta'lim maqsadlariga erishishda aniq ta'lim vazifalari ko'rsatilgan javobni belgilang",
        "options": ["1,2,3", "1,2,4", "2,3,4", "1,3,4"],
        "answer": "1,2,3"
    },
    {
        "id": 113,
        "question": "Maktabda ijobiy muloqot muhitini shakllantirish yo'nalishlari to'g'ri ko'rsatilgan javob variantini belgilang",
        "options": ["1,2,3,5", "1,2,4,5", "2,3,4,5", "1,3,4,5"],
        "answer": "1,2,3,5"
    },
    {
        "id": 114,
        "question": "Maktabda ziddiyatlarni oldini olish choralari to'g'ri ko'rsatilgan javob variantini aniqlang",
        "options": ["1,3,4,5", "1,2,3,4", "2,3,4,5", "1,2,4,5"],
        "answer": "1,3,4,5"
    },
    {
        "id": 115,
        "question": "Tarix o'qituvchisi Saida opa yangi yondashuvlarni qo'llash uchun kitob va tadqiqotlarni o'rganib, amaliyotga tadbiq etdi. Bunda u qaysi mehnat harakatlarini amalga oshirdi?",
        "options": ["Yangi bilimlarni qo‘llash", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Yangi bilimlarni qo‘llash"
    },
    {
        "id": 116,
        "question": "Dilmurod aka o'quvchilarni faol ishtirok etishga jalb qilish mexanizmlarini yaxshilashga harakat qildi. Bunda u qaysi mehnat harakatlarini amalga oshirdi?",
        "options": ["O'zgarishlarni amalga oshirish", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "O'zgarishlarni amalga oshirish"
    },
    {
        "id": 117,
        "question": "Farrux aka 'SWOT-analiz' metodidan foydalanib, darslari haqida yozuvlar olib bordi. Bunda u qaysi mehnat harakatlarini amalga oshirdi?",
        "options": ["Faoliyatini baholash", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Faoliyatini baholash"
    },
    {
        "id": 118,
        "question": "Yangi o'quv materiali qanday yo'l bilan o'rgatilganda bolaning aqliy faoliyati ta'rif, qoidalar, xulosalardan amali.digest yotga qarab boradi?",
        "options": ["Deduksiya", "Induksiya", "Tahlil", "Sintez"],
        "answer": "Deduksiya"
    },
    {
        "id": 119,
        "question": "Yangi bilimlarni o'rgatishning qaysi yo'li avval xususiyatlari tahlil etiladi, so'ngra qoida shaklida xulosalar chiqariladi?",
        "options": ["Induksiya", "Deduksiya", "Tahlil", "Sintez"],
        "answer": "Induksiya"
    },
    {
        "id": 120,
        "question": "Oʻqituvchi darsning boshida dars maqsadini bayon qiladi. Bunda oʻqituvchi qaysi mehnat harakatini amalga oshiradi?",
        "options": ["Erishimli vazifalarni belgilash", "Summativ baholash", "Darsni rejalashtirish",
                    "Motivatsiya qilish"],
        "answer": "Erishimli vazifalarni belgilash"
    },
    {
        "id": 121,
        "question": "Abu Nasr Forobiyning o‘qituvchi fikrlarini to‘la va aniq ifodalay olishi haqidagi fikrlari nutqning qaysi xususiyatiga to‘g‘ri keladi?",
        "options": ["Nutqning aniqligi", "Nutqning mantiqiyligi", "Nutqning ravonligi", "Nutqning ta'sirchanligi"],
        "answer": "Nutqning aniqligi"
    },
    {
        "id": 122,
        "question": "Zamonaviy pedagog yangi metod va texnologiyalarni qo‘llaydi. Bu vaziyatda qaysi burch va mas'uliyatni amalga oshiradi?",
        "options": ["Ijodkor va tashabbuskor", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Ijodkor va tashabbuskor"
    },
    {
        "id": 123,
        "question": "Yuqori tajribaga ega o'qituvchi darslarini boshqa fanlarni birlashtirgan holda o'tadi. Bu vaziyatda qaysi burch va mas'uliyatni amalga oshiradi?",
        "options": ["Fanlar integratsiyasi", "Summativ baholash", "Darsni rejalashtirish", "Motivatsiya qilish"],
        "answer": "Fanlar integratsiyasi"
    },
    {
        "id": 124,
        "question": "Darslarda pedagog har bir o'quvchi o'ziga xos shaxs ekanligini unutmagan holda ularning xulq-atvorni yoki qiyinchiliklarining sababini chuqur tushunishga harakat qiladi. Har bir o'quvchiga yangi imkoniyatlar yaratib, avvalgi xatolarini davomiy baho sifatida qabul qilmaslikni o'ziga odat qilgan. Nima maqsadda o'qituvchi o'quvchilar bilan bunday muloqotga kirishish yondashuvini qo'llaydi?",
        "options": [
            "Ayrim o‘quvchilarga nisbatan bir qolipdagi va bir holatdagi salbiy munosabatlarni bartaraf qilish",
            "O'quvchilarni faqat akademik yutuqlarga yo'naltirish",
            "Dars jarayonida faqat intizomga e'tibor berish",
            "O'quvchilarning individual ehtiyojlarini inobatga olmaslik"
        ],
        "answer": "Ayrim o‘quvchilarga nisbatan bir qolipdagi va bir holatdagi salbiy munosabatlarni bartaraf qilish"
    },
    {
        "id": 125,
        "question": "Pedagog o'z darslarida o'quvchilarga hurmat bilan yondashish va ularning shaxsiyatini rivojlantirishni asosiy maqsad sifatida belgilaydi. O'quvchilar darslarda o'zlarini nomaqbul tutgan vaqtda ham jazolash, bosim o'tkazish o'rniga ularni ilhomlantirib, mavzuga qiziqish uyg'otishga urinadi. Qaysi vaziyatda (yoki nima uchun) o'qituvchi o'quvchilar bilan bunday muloqotga kirishish yondashuvini qo'llaydi?",
        "options": [
            "Ta’lim va tarbiya tizimida taqiqlangan pedagogik talablarni qo‘llamaslik, aksincha, yangi, texnologik jihatdan mukammal deb topilgan pedagogik talablarni ko‘paytirish",
            "O'quvchilarni faqat intizomli bo'lishga majburlash",
            "Dars jarayonida faqat akademik bilimlarga e'tibor berish",
            "O'quvchilarning shaxsiy rivojlanishiga e'tibor bermaslik"
        ],
        "answer": "Ta’lim va tarbiya tizimida taqiqlangan pedagogik talablarni qo‘llamaslik, aksincha, yangi, texnologik jihatdan mukammal deb topilgan pedagogik talablarni ko‘paytirish"
    },
    {
        "id": 126,
        "question": "Pedagog darslarini qiziqarli o‘tishga harakat qiladi. Turli innovatsiyalarni qo'llagani tufayli darslari qiziqarli va samarali bo'ladi. O'z darslarida zamonaviy usullardan foydalangani uchun o'quvchilari mavzularni yaxshiroq qabul qiladilar. Bu vaziyatda zamonaviy pedagog talab etiladigan qaysi burch va mas'uliyatni amalga oshiradi?",
        "options": [
            "Zamonaviy ilm-fan, texnika va axborot-kommunikatsion texnologiyalari yangiliklari va yutuqlaridan xabardor bo'lib borish",
            "Faqat an'anaviy ta'lim metodlariga tayanib dars o'tish",
            "O'quvchilarning faqat akademik natijalariga e'tibor berish",
            "Dars jarayonida innovatsiyalarni qo'llamaslik"
        ],
        "answer": "Zamonaviy ilm-fan, texnika va axborot-kommunikatsion texnologiyalari yangiliklari va yutuqlaridan xabardor bo'lib borish"
    },
    {
        "id": 127,
        "question": "Bu pedagog darsning boshida o‘quvchilar bilan birgalikda sinf ichida hurmat va hamkorlik qoidalarini eslab o‘tadi. Ularni bir-birini hurmat qilishga undaydi va bu holatni o‘zining harakatlari bilan namoyon qiladi. Jamoa bo'lib erishilgan yutuqları nishonlash uchun kichik tadbirlar tashkil etadi. Nima maqsadda o'qituvchi o'quvchilar bilan bunday muloqotga kirishish yondashuvini qo'llaydi?",
        "options": [
            "Butun o‘quvchilar jamoasi bilan yaxlit o‘zaro ijobiy munosabat tashkil etish",
            "O'quvchilarni faqat intizomli bo'lishga majburlash",
            "Dars jarayonida faqat akademik bilimlarga e'tibor berish",
            "O'quvchilarning jamoaviy faoliyatini rag'batlantirmaslik"
        ],
        "answer": "Butun o‘quvchilar jamoasi bilan yaxlit o‘zaro ijobiy munosabat tashkil etish"
    },
    {
        "id": 128,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'O'quv jarayonini rejalashtirish' mehnat vazifalarining qaysi yo'nalishiga tegishli? - turli fan va mutaxassislik vakillari bilan samarali muloqot qilish; - hamkorlikda tadqiqot va ta'lim jarayonlarini tashkil etish; - turli sohalardagi bilimlarni solishtirish va bog'liqliklarni aniqlash; - har xil fan manbalarini o'rganish, tahlil qilish va taqqoslash.",
        "options": [
            "Fanlararo kompetensiyalarni fanga singdirish, o'z fanini boshqa fanlar bilan o'zaro",
            "Faqat o'z faniga doir rejalashtirish",
            "O'quvchilarning faqat akademik natijalariga e'tibor berish",
            "Dars jarayonida faqat bitta fan manbalaridan foydalanish"
        ],
        "answer": "Fanlararo kompetensiyalarni fanga singdirish, o'z fanini boshqa fanlar bilan o'zaro"
    },
    {
        "id": 129,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'O'quv jarayonini rejalashtirish' mehnat vazifalarining qaysi yo'nalishiga tegishli? - o'quvchilar bilimini baholash natijalarini tahlil qilish; - har bir o'quvchining bilim darajasini inobatga olib, muvofiqlashtirilgan ta'lim strategiyasini ishlab chiqish; - formativ va summativ baholash usullarini uyg'unlashtirish; - o'quvchilarning ehtiyojlariga qarab yangi usullarni qo'llash.",
        "options": [
            "O'quvchilarning bilimini baholash natijasida olingan ma'lumotlarni inobatga olib, rejalarni muvofiqlashtirish",
            "Faqat umumiy ta'lim rejalariga tayanib dars o'tish",
            "O'quvchilarning individual ehtiyojlarini inobatga olmaslik",
            "Baholash usullarini qo'llamaslik"
        ],
        "answer": "O'quvchilarning bilimini baholash natijasida olingan ma'lumotlarni inobatga olib, rejalarni muvofiqlashtirish"
    },
    {
        "id": 130,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'O'quv jarayonini rejalashtirish' mehnat vazifalarining qaysi yo'nalishiga tegishli? - darsning maqsadi va vazifalarini aniq belgilash; - darsning tuzilishini (bosqichlarini, muddatlarini) to'g'ri rejalashtirish; - dars jarayonida kutilmagan vaziyatlarga moslashish; - dars materialini qiziqarli va tushunarli shaklda yetkazish; - maqsadga erishish uchun turli o'qitish strategiyalarini uyg'unlashtirish.",
        "options": [
            "Dars vaqtini oqilona rejalashtirish, darsning maqsad, vazifa, shakl va usullarini aniqlash",
            "Faqat umumiy ta'lim rejalariga tayanib dars o'tish",
            "Dars jarayonida faqat bitta strategiyadan foydalanish",
            "Dars maqsadlarini aniqlamaslik"
        ],
        "answer": "Dars vaqtini oqilona rejalashtirish, darsning maqsad, vazifa, shakl va usullarini aniqlash"
    },
    {
        "id": 131,
        "question": "Kommunikativ nutqning muvaffaqiyatli bo'lishi o'qituvchi o'zida notiqlik san'atiga xos qator maxsus qobiliyatlarni rivojlantirish talab qilinadi. Quyida berilganlardan o'zini boshiqara olish qobiliyatining asosiy jihatlarini aniqlang. 1) O'z-o'zini tinchlantirish va qobiliyatli vaziyatlarda bardoshli bo'lish; 2) Jamiyandagi bugungi hodisalarni o'z o'tmishdagi voqealar va jarayonlar bilan bog'lash; 3) Maqsadlarga erishishda ishtiyoq va qat'iyatni saqlash; 4) O'z hissiy va intellektual holatini anglash va rivojlantirish.",
        "options": [
            "1,3,4",
            "1,2,3",
            "2,3,4",
            "1,2,4"
        ],
        "answer": "1,3,4"
    },
    {
        "id": 132,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'O'quv jarayonini rejalashtirish' mehnat vazifalarining qaysi yo'nalishiga tegishli? - turli fan va mutaxassislik vakillari bilan samarali muloqot qilish; - hamkorlikda tadqiqot va ta'lim jarayonlarini tashkil etish; - turli sohalardagi bilimlarni solishtirish va bog'liqliklarni aniqlash; - har xil fan manbalarini o'rganish, tahlil qilish va taqqoslash.",
        "options": [
            "Fanlararo kompetensiyalarni fanga singdirish, o'z fanini boshqa fanlar bilan o'zaro",
            "Faqat o'z faniga doir rejalashtirish",
            "O'quvchilarning faqat akademik natijalariga e'tibor berish",
            "Dars jarayonida faqat bitta fan manbalaridan foydalanish"
        ],
        "answer": "Fanlararo kompetensiyalarni fanga singdirish, o'z fanini boshqa fanlar bilan o'zaro"
    },
    {
        "id": 133,
        "question": "Kommunikativ nutqning muvaffaqiyatli bo'lishi uchun o'qituvchi o'zida notiqlik san'atiga xos qator maxsus qobiliyatlarni rivojlantirishi talab qilinadi. Quyida berilganlardan ishontira olish qobiliyatining asosiy tarkibiy qismlarini aniqlang: 1) Aniq dalillar va misollar keltirish orqali o'z fikrini asoslash; 2) Mantiqiy va ijobiy asoslarni ilgari surish; 3) O'z hissiy va intellektual holatini anglash va rivojlantirish; 4) Ijobiy va quvnoq kayfiyat orqali boshqalarning qiziqishini oshirish.",
        "options": [
            "1,2,4",
            "1,2,3",
            "2,3,4",
            "1,3,4"
        ],
        "answer": "1,2,4"
    },
    {
        "id": 134,
        "question": "Kommunikativ nutqning muvaffaqiyatli bo'lishi uchun o'qituvchi o'zida notiqlik san'atiga xos qator maxsus qobiliyatlarni rivojlantirishi talab qilinadi. Quyida berilganlardan muloqotda o'zining ruhiy holatini boshqara olish qobiliyatining asosiy tarkibiy qismlarini aniqlang: 1) Muloqot davomida g'azab, xafalik, stress yoki asabiylik kabi hissiyotlarni aniqlash va boshqarish; 2) Qiyin yoki keskin vaziyatlarda o'zini tinchlantirish va muammoni sovuqqonlik bilan hal qilish; 3) Suhbatdoshning hissiy holatini tushunishga harakat qilish va unga hurmat bilan munosabatda bo'lish; 4) Vaqtni samarali taqsimlash, maqsadlarni belgilash va ularga erishish uchun rejalar tuzish.",
        "options": [
            "1,2,3",
            "1,2,4",
            "2,3,4",
            "1,3,4"
        ],
        "answer": "1,2,3"
    },
    {
        "id": 135,
        "question": "O'qituvchi o'quvchilardan 'Otamdan qolgan dalalar' asari asosida 'Yer - bu boylikmi yoki mas'uliyatmi?' mavzusini guruhlarga bo'lingan holda real hayotiy holatlar bilan bog'lab, o'z fikrlarini bildirishni so'radi. O'qituvchi o'quvchilarning ishlash jarayoni va natijalarini baholadi. Shunda pedagog qaysi ta'lim metodidan foydalandi?",
        "options": [
            "Ta'limda amaliy metod",
            "Ta'limda hikoya metodi",
            "Ta'limda tasvir metodi",
            "Ta'limda suhbat metodi"
        ],
        "answer": "Ta'limda amaliy metod"
    },
    {
        "id": 136,
        "question": "O'quvchilarga mavzuni tushuntirishni osonlashtirish maqsadida o'qituvchi darsni quyidagi so'zlar bilan boshladi: 'Bir kuni kichik qishloqda yashovchi Umar degan bola bobosiga yog'ochdan qoshiq yasab berdi. Chunki avval bobosi unga yog'ochdan buyum yasash sirlari haqida gapirib bergan edi. Unga yog'och tanlashni, keyin esa oddiy asboblar bilan yog'ochni shakllantirishni ko'rsatgan edi...'. O'quvchilarning diqqati jamlangandan so'ng, u asosiy dars mavzusini boshladi. Shunda pedagog qaysi ta'lim metodidan foydalandi?",
        "options": [
            "Ta'limda hikoya metodi",
            "Ta'limda tasvir metodi",
            "Ta'limda amaliy metod",
            "Ta'limda suhbat metodi"
        ],
        "answer": "Ta'limda hikoya metodi"
    },
    {
        "id": 137,
        "question": "Pedagog devorga rasm ildi. Unda mahalladagi eski uylar orasida bir bola toshga o'tirib olgani, uning yuzida charchoq, ko'zlarida esa g'am borligi, qo'lida yirtiq xalta, oyog'iga esa bir juft eskirgan etik kiyib olgani chizilgan edi. O'qituvchi voqeani 'ko'z oldiga keltirish', shaxsiy munosabat bildirish, empatiya tuyg'usini shakllantirish maqsadida bola qanday muammo bilan to'qnash kelgan bo'lishi mumkinligi haqida o'quvchilardan so'radi. Shunda pedagog qaysi ta'lim metodidan foydalandi?",
        "options": [
            "Ta'limda tasvir metodi",
            "Ta'limda hikoya metodi",
            "Ta'limda amaliy metod",
            "Ta'limda suhbat metodi"
        ],
        "answer": "Ta'limda tasvir metodi"
    },
    {
        "id": 138,
        "question": "Pedagogik jarayon kutilmagan hodisa va anglashilmovchiliklardan holi emas. Bunday holatlar turli ko‘rinishdagi nizolarni keltirib chiqaradi. Agar o‘qituvchi yoki rahbarning maqsadi nizoli vaziyatni zudlik bilan bartaraf qilish hamda tartib va intizomni saqlash bo'lsa, muammoni qat'iy va hech qanday muhokamasiz qaror qabul qilish orqali hal qilsa, pedagogik nizolarni hal qilishning qanday usulini qo'llagan hisoblanadi?",
        "options": [
            "Kuch bilan bostirish usuli",
            "Tushuntirish usuli",
            "Sud qarori usuli",
            "Muzokara usuli"
        ],
        "answer": "Kuch bilan bostirish usuli"
    },
    {
        "id": 139,
        "question": "Pedagogik jarayon kutilmagan hodisa va anglashilmovchiliklardan holi emas. Bunday holatlar turli ko'rinishdagi nizolarni keltirib chiqaradi. Bu pedagogik nizolarni hal qilishning huquqiy mexanizmi bo'lib, nizoli vaziyat tomonlarning o'zaro kelisha olmagan holatida amalga oshiriladi. Bu usul asosan o'ta jiddiy, murakkab va huquqiy talablarga yopishgan nizolarni adolatli hal qilishda qo'llaniladi. Pedagogik nizolarni hal qilishning qanday usuli haqida gap ketyapti?",
        "options": [
            "Sud qarori usuli",
            "Kuch bilan bostirish usuli",
            "Tushuntirish usuli",
            "Muzokara usuli"
        ],
        "answer": "Sud qarori usuli"
    },
    {
        "id": 140,
        "question": "Pedagogik jarayon kutilmagan hodisa va anglashilmovchiliklardan holi emas. Bunday holatlar turli ko'rinishdagi nizolarni keltirib chiqaradi. Agar o'qituvchi o‘quvchining noto'g'ri xatti-harakatini tanqid qilmasdan, uning sabab va oqibatlari haqida gapirsa, nizo sabab bo'lgan tomonlarga nisbatan muloyim va izchil muloqot orqali qanday qilib to'g'ri va maqbul tarzda harakat qilish mumkinligini ko'rsata olsa, pedagogik nizolarni hal qilishning qanday usulini qo'llagan hisoblanadi?",
        "options": [
            "Tushuntirish usuli",
            "Kuch bilan bostirish usuli",
            "Sud qarori usuli",
            "Muzokara usuli"
        ],
        "answer": "Tushuntirish usuli"
    },
    {
        "id": 141,
        "question": "Pedagog global dunyoqarashga ega va xalqaro standartlarga mos ta'lim berishga harakat qiladi. Turli innovatsiyalarni qo'llagani tufayli darslari qiziqarli va samarali bo'ladi. O'z darslarida zamonaviy usullardan foydalangani uchun o'quvchilari mavzularni yaxshiroq qabul qiladilar. Bu vaziyatda zamonaviy pedagog talab etiladigan qaysi burch va mas'uliyatni amalga oshiradi?",
        "options": [
            "Zamonaviy o'qituvchining ilm-fan, texnika va axborot-kommunikatsion texnologiyalari yangiliklaridan va yutuqlaridan xabardor bo'lib borishi talab etiladi",
            "Faqat an'anaviy ta'lim metodlariga tayanib dars o'tish",
            "O'quvchilarning faqat akademik natijalariga e'tibor berish",
            "Dars jarayonida innovatsiyalarni qo'llamaslik"
        ],
        "answer": "Zamonaviy o'qituvchining ilm-fan, texnika va axborot-kommunikatsion texnologiyalari yangiliklaridan va yutuqlaridan xabardor bo'lib borishi talab etiladi"
    },
    {
        "id": 142,
        "question": "Pedagog o'z darslarini qiziqarli, interfaol va samarali bo'lish uchun yangi metod va texnologiyalarni o'ylab topadi va qo'llaydi. Ta'lim jarayonini takomillashtirishiga yo'naltirilgan yangi loyihalar, dasturlar va tadbirlarni ishlab chiqadi. O'quvchilarning qobiliyatlarini rivojlantirib, ularga o'z maqsadlariga erishish uchun zarur bo‘lgan bilim va ko'nikmalarni berib boradi. Bu vaziyatda zamonaviy pedagog talab etiladigan qaysi burch va mas'uliyatni amalga oshiradi?",
        "options": [
            "O‘qituvchi ijodkor, ta'lim-tarbiyaviy faoliyat tashabbuskori va yosh avlod kelajagi uchun javobgar shaxsdir",
            "Faqat an'anaviy ta'lim metodlariga tayanib dars o'tish",
            "O'quvchilarning faqat akademik natijalariga e'tibor berish",
            "Dars jarayonida yangi loyihalar ishlab chiqmaslik"
        ],
        "answer": "O‘qituvchi ijodkor, ta'lim-tarbiyaviy faoliyat tashabbuskori va yosh avlod kelajagi uchun javobgar shaxsdir"
    },
    {
        "id": 143,
        "question": "Yuqori tajribaga ega o‘qituvchi o'quvchilarga yanada kengroq va aniqroq tasavvur berish maqsadida o'z darslarini boshqa fanlarni birlashtirgan holda o'tadi. Buning uchun ta'lim sohasidagi yangiliklarni va global o‘zgarishlarni muntazam ravishda kuzatib boradi. Bu vaziyatda zamonaviy pedagog talab etiladigan qaysi burch va mas'uliyatni amalga oshiradi?",
        "options": [
            "O‘qituvchi o'z mutaxassisligi bo‘yicha chuqur bilimga ega bo'lishi, barcha fanlar integratsiyasini o'zlashtirib borish, bunda o‘z ustida tinimsiz ilmiy izlanishlar olib borishi lozim",
            "Faqat o'z faniga doir bilimlarga e'tibor berish",
            "Dars jarayonida faqat bitta fan manbalaridan foydalanish",
            "Ta'lim sohasidagi yangiliklarni kuzatmaslik"
        ],
        "answer": "O‘qituvchi o'z mutaxassisligi bo‘yicha chuqur bilimga ega bo'lishi, barcha fanlar integratsiyasini o'zlashtirib borish, bunda o‘z ustida tinimsiz ilmiy izlanishlar olib borishi lozim"
    },
    {
        "id": 144,
        "question": "Pedagog 'O‘tgan kunlar' asari bo'yicha bir nechta o‘quvchiga individual mini-proyekt tayyorlash, bir nechtasiga shu mavzu bilan bog'liq real hayotiy vazifalar, qolganlarga esa 'muhabbat va sadoqat tushunchasini tasviriy shaklda ifoda etish' vazifasi berdi. Baholash vaqtida har bir o'quvchiga individual fikr-mulohaza bildirdi. Bunda pedagog 'O'zlashtirishni baholash va qayta aloqani taqdim etish' mehnat vazifalarining qaysi ko'nikmalarini namoyon qildi?",
        "options": [
            "O‘quvchilarning turli xil ehtiyojlari va qobiliyatlari bilan bog'liq holda baholash jarayonini shaxsga yo'naltirish",
            "Faqat umumiy baholash usullaridan foydalanish",
            "O'quvchilarning individual ehtiyojlarini inobatga olmaslik",
            "Baholash jarayonida fikr-mulohaza bildirmaslik"
        ],
        "answer": "O‘quvchilarning turli xil ehtiyojlari va qobiliyatlari bilan bog'liq holda baholash jarayonini shaxsga yo'naltirish"
    },
    {
        "id": 145,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'Ta'lim samaradorligini ta'minlash' mehnat vazifalarining qaysi yo'nalishiga tegishli? - real hayotga mos bo'lgan topshiriqlar orqali o'quvchilarga fanning ahamiyatini ko'rsatish; - motivatsiya usullaridan foydalanish, mukofot tizimi, o'yin shaklidagi topshiriqlar; - turli ilhomlantiruvchi vaziyatlarni yaratishdan so'ng, ularning samaradorligini baholash, faoliyatni tahrirlash.",
        "options": [
            "Motivatsion vaziyatlarni yaratish, ularning samaradorligini tahlil qilish va kerakli natijalarga erishishda o'z harakatlarini o'zgartirish",
            "Faqat akademik bilimlarga e'tibor berish",
            "O'quvchilarning motivatsiyasiga e'tibor bermaslik",
            "Dars jarayonida faqat an'anaviy usullardan foydalanish"
        ],
        "answer": "Motivatsion vaziyatlarni yaratish, ularning samaradorligini tahlil qilish va kerakli natijalarga erishishda o'z harakatlarini o'zgartirish"
    },
    {
        "id": 146,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'Ta'lim samaradorligini ta'minlash' mehnat vazifalarining qaysi yo'nalishiga tegishli? - o'quv jarayonida differensial va shaxsiy yondashuvni qo'llash; - darslar davomida rivojlanish va individual imkoniyatlarni hisobga olish; - emotsional intellektni rivojlantirish, o'quvchilarning ehtiyojlarini to'g'ri anglash; - ta'lim jarayonidagi muvaffaqiyatlar va kamchiliklarni muhokama qilish.",
        "options": [
            "Pedagogik va psixologik bilimlardan foydalanib, pedagogik vaziyat va hodisalarni kuzatib borish, ularni tahlil qilish",
            "Faqat umumiy ta'lim usullaridan foydalanish",
            "O'quvchilarning individual ehtiyojlarini inobatga olmaslik",
            "Dars jarayonida faqat akademik bilimlarga e'tibor berish"
        ],
        "answer": "Pedagogik va psixologik bilimlardan foydalanib, pedagogik vaziyat va hodisalarni kuzatib borish, ularni tahlil qilish"
    },
    {
        "id": 147,
        "question": "MOSLASHTIRING! 1. Arbitraj. A) Bunday holda o'qituvchi vaziyatni o'rganish asosida 'qaror qabul qiladigan' hakam rolini o'z zimmasiga oladi. 2. Muzokara. B) O'qituvchi nizoning sabablarini tushunishga yordam beradi va o'quvchilarga kelishmovchilikni hal qilish yo'llari bo'yicha mustaqil ravishda qaror qabul qilish imkonini beradi. 3. Mediatsiya. C) O'quvchilar nizoni o'zlari qanday hal qilishni bilmasalar, ular muloqotga xolis yordam beradigan, his-tuyg'ular darajasini pasaytiradigan va yakuniy qarorni qabul qiladigan vositachi yordamida ta'minlanishi mumkin.",
        "options": [
            "1-a; 2-b; 3-c",
            "1-b; 2-a; 3-c",
            "1-c; 2-b; 3-a",
            "1-a; 2-c; 3-b"
        ],
        "answer": "1-a; 2-b; 3-c"
    },
    {
        "id": 148,
        "question": "Oʻqituvchi oʻquvchilarga yangi mavzuni tushuntirdi. Dars yakunida oʻquvchilarning mavzuni qanday oʻzlashtirganliklarini sinash maqsadida 'Bu qayerdan keldi? Bu nima? Bu nega aynan shunday boʻldi?' mazmunida savollar berdi. Blum taksonomiyasining qaysi bosqichi namoyon boʻlmoqda?",
        "options": [
            "Tushunish",
            "Bilish",
            "Qo'llash",
            "Tahlil"
        ],
        "answer": "Tushunish"
    },
    {
        "id": 149,
        "question": "Anvar aka o'quvchilarga nazorat ishi berdi va baholadi, o'qituvchi o'quvchilarning natijalarida faqat ijobiy taraflarini emas salbiy taraflarini ham aytib o'tdi. O'qituvchi o'quv samaradorligini ta'minlashning qaysi vazifasini bajargan?",
        "options": [
            "Oʻquvchilar bilimini baholash natijasida olingan maʼlumotlar asosida darsni tashkil etish va taʼlim berishdagi yondashuvlarining samaradorligini tahlil qilish",
            "Faqat ijobiy natijalarga e'tibor berish",
            "O'quvchilarning salbiy natijalarini e'tiborsiz qoldirish",
            "Dars jarayonida baholashni olib bormaslik"
        ],
        "answer": "Oʻquvchilar bilimini baholash natijasida olingan maʼlumotlar asosida darsni tashkil etish va taʼlim berishdagi yondashuvlarining samaradorligini tahlil qilish"
    },
    {
        "id": 150,
        "question": "O'qituvchi loyiha ishini amalga oshirish jarayonida o'quvchilaridan biri boshqalarga nisbatan ustunlik qilayotganini va boshqa o'quvchilarga bajarishga biron bir ish qoldirmayotganligini sezib qoldi. Quyida o'qituvchi qanday yo'l tutadi?",
        "options": [
            "Loyiha ishidagi rollarni barcha o'quvchilar saviyasiga mos qilib muqobillashtirish",
            "Ustunlik qilayotgan o'quvchiga faqat ishlashga ruxsat berish",
            "Loyiha ishini butunlay bekor qilish",
            "Boshqa o'quvchilarni loyihadan chetlashtirish"
        ],
        "answer": "Loyiha ishidagi rollarni barcha o'quvchilar saviyasiga mos qilib muqobillashtirish"
    },
    {
        "id": 151,
        "question": "O'qituvchi yuqori sinf o'quvchilarining xulqida o'zgarishlar bo'layotganligini sezdi. Bunday yoshda ular bilan sodir bo'lishi mumkin bo'lgan turli xil ko'ngilsizliklarni oldini olish uchun huquq-tartibot organlari bilan hamkorlikni yo'lga qo'ydi. Bu holatda o'qituvchi kasbiy kompetentlikning qaysi mehnat vazifasini bajargan hisoblanadi?",
        "options": [
            "Tarbiyaviy muammolarni hal qilishda va oʻquvchilarni hayotga tayyorlashda boshqa pedagogik xodimlar va mutaxassislar, jamoat tashkilotlari va boʻlimlari (Yoshlar ittifoqi) bilan hamkorlik qilish",
            "Faqat o'z sinfi bilan ishlash",
            "O'quvchilarning xulqidagi o'zgarishlarga e'tibor bermaslik",
            "Huquq-tartibot organlari bilan hamkorlik qilmaslik"
        ],
        "answer": "Tarbiyaviy muammolarni hal qilishda va oʻquvchilarni hayotga tayyorlashda boshqa pedagogik xodimlar va mutaxassislar, jamoat tashkilotlari va boʻlimlari (Yoshlar ittifoqi) bilan hamkorlik qilish"
    },
    {
        "id": 152,
        "question": "Oʻqituvchi ketma-ket ulash zanjir sxemasini amaliy o'quvchilarga ko'rsatib berdi va 'lampochkani uzsak nima bo'ladi?' deb so'radi? O'qituvchi quyidagilardan qaysi metoddan foydalangan?",
        "options": [
            "Namoyish",
            "Tushuntirish",
            "Suhbat",
            "Amaliy"
        ],
        "answer": "Namoyish"
    },
    {
        "id": 153,
        "question": "Maktabda nizo (konflikt) yuzaga kelib, kuchaygan taqdirda rahbar qanday usuldan foydalangan holda maktab ichida nizoni tahlil qilib, uni tinchitishi eng maqbul hisoblanadi?",
        "options": [
            "Nizo taraflarini xolisona tinglash, vaziyatni tahlil qilish va murosaga chaqirish",
            "Nizoni e'tiborsiz qoldirish",
            "Faqat bir tomonni qo'llab-quvvatlash",
            "Nizoni kuch bilan bostirish"
        ],
        "answer": "Nizo taraflarini xolisona tinglash, vaziyatni tahlil qilish va murosaga chaqirish"
    },
    {
        "id": 154,
        "question": "Oʻqituvchi oʻquvchilarga internetdan toʻgʻri foydalanishni, feyk xabarlarni ajratishni va ishonchli manbalarni tekshirishni oʻrgatdi. Bu holatda oʻqituvchi kasb standartidagi qaysi mehnat vazifasini bajarmoqda?",
        "options": [
            "Oʻquvchilarga mediasavodxonligini shakllantirish",
            "Faqat akademik bilimlarga e'tibor berish",
            "Internetdan foydalanishni taqiqlash",
            "O'quvchilarning media bilan ishlashiga e'tibor bermaslik"
        ],
        "answer": "Oʻquvchilarga mediasavodxonligini shakllantirish"
    },
    {
        "id": 155,
        "question": "O'qituvchi o'quvchilarni baholari haqida doimo ota-onalarni xabardor qiladi. Ota-onalarning telegram guruhida baholashga doir barcha ma'lumotlar: kundalik baholash, yakuniy baholash, diagnostik baholash turlari haqidagilarni yuborib turadi. Bunday holatda o'qituvchi o'zlashtirishni baholash va qayta aloqani taqdim etishning qaysi zaruriy ko'nikmasini bajargan hisoblanadi?",
        "options": [
            "Oʻquvchilarga va ota-onalar(ularning oʻrnini bosuvchi shaxslar)ga taʼlim va baholash natijalari toʻgʻrisida qayta aloqani oʻrnatish uchun turli xil strategiyalardan foydalanish",
            "Faqat o'quvchilar bilan ishlash",
            "Ota-onalarni baholash jarayoniga jalb qilmaslik",
            "Baholash natijalarini faqat o'quvchilarga taqdim etish"
        ],
        "answer": "Oʻquvchilarga va ota-onalar(ularning oʻrnini bosuvchi shaxslar)ga taʼlim va baholash natijalari toʻgʻrisida qayta aloqani oʻrnatish uchun turli xil strategiyalardan foydalanish"
    },
    {
        "id": 156,
        "question": "Quyidagilar o'quv jarayonini rejalashtirish kompetensiya standartining qaysi zaruriy ko'nikmasiga to'g'ri keladi? - Smart maqsadlar qo'yish; - ta'lim natijalarini turlarga ajratish; - maqsadga erishish muddatlarini belgilangan taqvimiy tahririy rejasini tuzish; - natijalarni baholash va monitoring qilish.",
        "options": [
            "Taʼlimning aniq va oʻlchanadigan natijalarini, shuningdek ushbu natijalarga erishishda aniq muddatlar (yil, chorak, dars) uchun vazifalarni aniqlash va ularni rejalarda shakllantirish",
            "Faqat umumiy ta'lim rejalariga tayanib dars o'tish",
            "Dars jarayonida faqat bitta strategiyadan foydalanish",
            "Ta'lim natijalarini monitoring qilmaslik"
        ],
        "answer": "Taʼlimning aniq va oʻlchanadigan natijalarini, shuningdek ushbu natijalarga erishishda aniq muddatlar (yil, chorak, dars) uchun vazifalarni aniqlash va ularni rejalarda shakllantirish"
    },
    {
        "id": 157,
        "question": "Pedagog o'quvchilarning bilimlarini aniqlash, qaysi mavzular da o'zlashtirishga qiynalishlari aksincha qaysi mavzularni yengilroq o'zlashtirishlarini bilish maqsadida testlardan foydalanadi. Bundan tashqari rasm, diagramma va sxemalar orqali ham baholashga harakat qiladi. Bunday holatda o'qituvchi o'zlashtirishni baholash va qayta aloqani taqdim etishning qaysi zaruriy ko'nikmasini bajargan hisoblanadi?",
        "options": [
            "Diagnostik va baholash testlarining har xil turlarini ishlab chiqish",
            "Faqat bitta baholash usulidan foydalanish",
            "O'quvchilarning o'zlashtirish darajasini aniqlamaslik",
            "Baholash jarayonida faqat testlardan foydalanish"
        ],
        "answer": "Diagnostik va baholash testlarining har xil turlarini ishlab chiqish"
    },
    {
        "id": 158,
        "question": "Oʻqituvchi sinfdagi oʻquvchilarga tez-tez “Ajoyib”, “Juda zoʻr” deb qoʻyadi, kulib kallasini qimirlatib qoʻyadi, oʻrni kelganda yelkasiga qoʻlini qoʻyib qoʻyadi. Oʻqituvchi nima uchun bunday qiladi?",
        "options": [
            "Yaxlit oʻzaro ijobiy munosabatlarni shakllantirish uchun",
            "Faqat intizomga e'tibor berish",
            "O'quvchilarning faqat akademik natijalariga e'tibor berish",
            "O'quvchilar bilan muloqot qilmaslik"
        ],
        "answer": "Yaxlit oʻzaro ijobiy munosabatlarni shakllantirish uchun"
    },
    {
        "id": 159,
        "question": "Quyidagilar Mehnat samaradorligini oshirishning qaysi yoʻnalishiga mos keladi? - Har bir oʻquvchining darslardagi faolligini kuzatish; - Oraliq test, nazorat ishlari olish orqali oʻquvchilarning bilim darajasini aniqlash; - Intellektual qobiliyatlari va tanqidiy fikrlashlarini oʻrganish uchun testlar oʻtkazish; - Qiziqishlari boʻyicha yoʻnaltirilgan fanlarni chuqur oʻrganish imkoniyatini yaratish.",
        "options": [
            "Har bir oʻquvchining ehtiyoji va qobiliyatini diagnostika qilish uchun",
            "Faqat umumiy ta'lim usullaridan foydalanish",
            "O'quvchilarning individual ehtiyojlarini inobatga olmaslik",
            "Dars jarayonida faqat akademik bilimlarga e'tibor berish"
        ],
        "answer": "Har bir oʻquvchining ehtiyoji va qobiliyatini diagnostika qilish uchun"
    },
    {
        "id": 160,
        "question": "Musiqa fani o'qituvchisi darsda sinf doskasiga do, mi, sol notasini chizdi va uni pianinoda sol, mi, do shaklida chalib berdi. O'quvchilar bu yerda o'qituvchining xato qilganligini birdaniga anglab xatoni to'g'irlashdi. Bunday holatda o'qituvchi qaysi metoddan foydalandi?",
        "options": [
            "Didaktik o'yin",
            "Tushuntirish",
            "Namoyish",
            "Amaliy"
        ],
        "answer": "Didaktik o'yin"
    },
    {
        "id": 161,
        "question": "O'qituvchi jismoniy yuklamadan oldin o'quvchilarga turli mashqlar: boshni aylantirish, qo'llarni yon tomonga cho'zish va pastga tushirish kabilarni ko'rsatib berdi. Keyin o'quvchilar bu mashqlarni xuddi o'qituvchi ko'rsatgandek takrorlashdi. Bunday holatda o'qituvchi qaysi metoddan foydalandi?",
        "options": [
            "Amaliy",
            "Tushuntirish",
            "Namoyish",
            "Suhbat"
        ],
        "answer": "Amaliy"
    },
    {
        "id": 162,
        "question": "Oʻqituvchi o'quvchilar bilan suhbatda so'z boyligining kengligi, fikr yuritayotganda mavzuga nisbatan chuqur bilimga ega ekanligi, bilimlarini o'z tafakkuri doirasida tahlil qila olishini namoyon qildi. Suhbat jarayonida gaplarning ketma-ket bir-biriga to'g'ri kelishi va izchilligi hammani hayron, lol qoldirdi. Bunda tarix fani o'qituvchisi Jasur aka nutqning asosiy xususiyatlaridan qay birini mohirona qo'llagan hisoblanadi?",
        "options": [
            "Nutqning mantiqiyligi",
            "Nutqning aniqligi",
            "Nutqning ravonligi",
            "Nutqning ta'sirchanligi"
        ],
        "answer": "Nutqning mantiqiyligi"
    },
    {
        "id": 163,
        "question": "Kommunikativ muloqot qilish orqali irodaviy ta'sir koʻrsatish qobiliyatining asosiy jihatlarini koʻrsating: 1) Boshqalarni ilhomlantirish, oʻrnak koʻrsatish; 2) Odamlarga motivatsiya berish; 3) Oʻzining kasbiy va intellektual holatini anglash; 4) Jamoani qabul qilgan qarorlarini qoʻllab-quvvatlash.",
        "options": [
            "2,3",
            "1,2",
            "3,4",
            "1,4"
        ],
        "answer": "2,3"
    },
    {
        "id": 164,
        "question": "Sinfda o'quvchilar o'rtasida nizo paydo bo'ldi. O'qituvchi esa ularga tanbeh bermasdan muloyimlik bilan urushmasliklari kerakligini aytdi. Bunday holatda o'qituvchi nizoni hal qilishning qanday usulidan foydalandi?",
        "options": [
            "Iltimos",
            "Tushuntirish",
            "Arbitraj",
            "Muzokara"
        ],
        "answer": "Iltimos"
    },
    {
        "id": 165,
        "question": "Oʻqituvchi elektr zanjirining ishlashini sxema asosida tushuntirib, uning elementlarini chizmada koʻrsatib berdi. Bu qaysi metod hisoblanadi?",
        "options": [
            "Tasvir",
            "Tushuntirish",
            "Namoyish",
            "Amaliy"
        ],
        "answer": "Tasvir"
    },
    {
        "id": 166,
        "question": "Quyida qayd etilgan ko'nikmalar o'qituvchining 'Ta'lim samaradorligini ta'minlash' mehnat vazifalarining qaysi yo'nalishiga tegishli? - Mavzuga nisbatan noodatiy yondashuvlarni qo'llash; - Real hayotdagi muammolarni modellashtirish; - Analitik maqola yozishni rivojlantirish; - Virtual laboratoriyalar yordamida muammolar yechimini topish; - Manbalarni tahlil qilish.",
        "options": [
            "Umumiy oʻrta taʼlimning taʼlim standartlarida belgilangan oʻquvchilarning asosiy kompetensiyalari va hayotiy koʻnikmalarini rivojlantirishga yoʻnaltirilgan usullardan foydalanish",
            "Faqat an'anaviy ta'lim usullaridan foydalanish",
            "O'quvchilarning hayotiy ko'nikmalariga e'tibor bermaslik",
            "Dars jarayonida faqat akademik bilimlarga e'tibor berish"
        ],
        "answer": "Umumiy oʻrta taʼlimning taʼlim standartlarida belgilangan oʻquvchilarning asosiy kompetensiyalari va hayotiy koʻnikmalarini rivojlantirishga yoʻnaltirilgan usullardan foydalanish"
    },
    {
        "id": 167,
        "question": "Qaysi oʻqitish usuli quyidagi afzallik va kamchilikka ega? Afzalligi: doimo mavjud boʻlganligi tufayli oʻquvchi xohlagan payti qayta koʻrib chiqishi, mustahkamlashi mumkin. Kamchiligi: oʻqituvchi va jamoa boʻlib ishlanmaydi.",
        "options": [
            "Onlayn (masofaviy) oʻqitish",
            "An'anaviy sinf darsi",
            "Guruhli loyiha ishi",
            "Amaliy mashg'ulot"
        ],
        "answer": "Onlayn (masofaviy) oʻqitish"
    },
    {
        "id": 168,
        "question": "Ota-ona farzandiga faqat akademik bilimlar yetarli ekanini, boshqa hech narsa kerak emasligini aytdi. Sinf rahbari esa ota-onaga tadbirda farzandining nutqi ravon bo‘lishi, sahnada o‘zini erkin tuta olishini kuzatish zarurligini aytdi. Sinf rahbari bu yerda qanday usuldan foydalanadi?",
        "options": [
            "Ishontirish usuli",
            "Tushuntirish usuli",
            "Talab usuli",
            "Muzokara usuli"
        ],
        "answer": "Ishontirish usuli"
    },
    {
        "id": 169,
        "question": "Oʻqituvchi ota-onalarga telefon qilib zudlik bilan ota-onalari seminari oʻtkazish kerakligi, sinfda oʻquvchilar kundan-kunga past baho olayotganligi haqida gapirdi. Ota-onalar bilan birga muammoga yechim topishga muvaffaq boʻldi. Oʻqituvchi kasb standartining 'Hamkasblar va ota-onalari bilan hamkorlik' kompetensiya sohasining qaysi mehnat harakatini bajardi?",
        "options": [
            "Oʻquvchilarning ota-onalarni taʼlim jarayoniga jalb qilish",
            "Faqat o'quvchilar bilan ishlash",
            "Ota-onalarni ta'lim jarayoniga jalb qilmaslik",
            "Muammolarni faqat o'zi hal qilish"
        ],
        "answer": "Oʻquvchilarning ota-onalarni taʼlim jarayoniga jalb qilish"
    },
    {
        "id": 170,
        "question": "O‘qituvchi o‘quvchilarning davomatini pasaygani sababli mahalla faollari va maktab psixologi bilan suhbat tashkil qildi. Ular bilan birgalikda ota-onalarni xabardor qilish va tashriflar rejasini tuzdi. Bu qaysi mehnat harakatiga mos keladi?",
        "options": [
            "Tarbiyaviy muammolarni hal qilishda va oʻquvchilarni hayotga tayyorlashda boshqa pedagogik xodimlar va mutaxassislar, jamoat tashkilotlari va boʻlimlari (Yoshlar ittifoqi) bilan hamkorlik qilish",
            "Faqat o'z sinfi bilan ishlash",
            "Davomat muammosiga e'tibor bermaslik",
            "Mahalla faollari bilan hamkorlik qilmaslik"
        ],
        "answer": "Tarbiyaviy muammolarni hal qilishda va oʻquvchilarni hayotga tayyorlashda boshqa pedagogik xodimlar va mutaxassislar, jamoat tashkilotlari va boʻlimlari (Yoshlar ittifoqi) bilan hamkorlik qilish"
    }

]

user_data = {}

# Klaviatura yaratish
def get_keyboard(options):
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)

    keyboard = []
    for i, option in enumerate(shuffled_options):
        letter = chr(65 + i)  # A, B, C, D
        keyboard.append([InlineKeyboardButton(f"{letter}. {option}", callback_data=option)])

    return InlineKeyboardMarkup(keyboard), shuffled_options

# Natija formatlash
def format_result(question_text, user_answer, correct_answer, shuffled_options):
    result_text = f"Savol:\n{question_text}\n\n"

    for idx, option in enumerate(shuffled_options):
        letter = chr(65 + idx)
        if option == user_answer and option == correct_answer:
            result_text += f"{letter}. {option} ✅\n"
        elif option == user_answer:
            result_text += f"{letter}. {option} ❌\n"
        elif option == correct_answer:
            result_text += f"{letter}. {option} ✅\n"
        else:
            result_text += f"{letter}. {option}\n"
    return result_text

def get_next_question_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Keyingi savol", callback_data="next_question")]
    ])

def get_final_keyboard(score, total):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Natija: {score}/{total}", callback_data="result")],
        [InlineKeyboardButton("Qayta boshlash", callback_data="restart")]
    ])

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {"question_index": 0, "score": 0, "shuffled_options": []}

    question = questions[0]
    reply_markup, shuffled = get_keyboard(question["options"])
    user_data[user_id]["shuffled_options"] = shuffled

    await update.message.reply_text(
        f"Savol {question['id']}/{len(questions)}: {question['question']}",
        reply_markup=reply_markup
    )

# /menu komandasi
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = "Savollar ro'yxati:\n\n"
    for q in questions:
        menu_text += f"{q['id']}. {q['question']}\n"
    await update.message.reply_text(menu_text)

# Javobni tekshirish
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_answer = query.data

    index = user_data[user_id]["question_index"]
    question = questions[index]
    correct_answer = question["answer"]
    shuffled_options = user_data[user_id]["shuffled_options"]

    if user_answer == correct_answer:
        user_data[user_id]["score"] += 1

    result_text = format_result(question["question"], user_answer, correct_answer, shuffled_options)

    user_data[user_id]["question_index"] += 1

    if user_data[user_id]["question_index"] < len(questions):
        await query.edit_message_text(result_text, reply_markup=get_next_question_keyboard())
    else:
        score = user_data[user_id]["score"]
        total = len(questions)
        await query.edit_message_text(
            result_text + f"\n\nViktorina tugadi! Sizning natijangiz: {score}/{total}",
            reply_markup=get_final_keyboard(score, total)
        )
        del user_data[user_id]

# Keyingi savol va qayta boshlash
async def handle_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "next_question":
        index = user_data[user_id]["question_index"]
        question = questions[index]
        reply_markup, shuffled = get_keyboard(question["options"])
        user_data[user_id]["shuffled_options"] = shuffled

        await query.edit_message_text(
            f"Savol {question['id']}/{len(questions)}: {question['question']}",
            reply_markup=reply_markup
        )
    elif data == "restart":
        user_data[user_id] = {"question_index": 0, "score": 0, "shuffled_options": []}
        question = questions[0]
        reply_markup, shuffled = get_keyboard(question["options"])
        user_data[user_id]["shuffled_options"] = shuffled

        await query.edit_message_text(
            f"Savol {question['id']}/{len(questions)}: {question['question']}",
            reply_markup=reply_markup
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(check_answer, pattern="^(?!next_question|restart|result).*$"))
    app.add_handler(CallbackQueryHandler(handle_result, pattern="^(next_question|restart|result)$"))
    app.run_polling()

if __name__ == '__main__':
    main()
