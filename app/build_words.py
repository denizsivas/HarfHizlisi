"""Generate validated words.py."""
from pathlib import Path
from pprint import pformat


def w(word: str, hint: str) -> tuple[str, str]:
    return (word, hint)


RAW = {
    "bilim": (
        "Bilim",
        "Fizik, kimya, biyoloji ve teknoloji",
        {
            3: [
                w("AÇI", "Sinüs ve kosinüsle ölçülen geometrik değer"),
                w("GEN", "Mendel'in bezelyelerinde aradığı kalıtım birimi"),
                w("DNA", "Çift sarmal yapıdaki kalıtım molekülü"),
                w("IŞI", "c·λ ile ilişkilendirilen enerji taşıyıcısı"),
                w("TIP", "Tıp fakültesinden mezun olan kişi"),
                w("AZO", "N₂ ile ilgili bileşik grubunun adı"),
            ],
            4: [
                w("İYON", "Elektron alışverişi sonrası yüklenen tanecik"),
                w("ATOM", "Periyodik tablodaki en küçük birim"),
                w("ASIT", "pH ölçeğinde 7'nin altında kalan madde"),
                w("AMİP", "Tek hücreli, hareketli protist"),
                w("ASAL", "Yalnızca 1 ve kendisine bölünebilen sayı"),
                w("İYOT", "Halojenler grubunda, mor buharlı element"),
            ],
            5: [
                w("FOTON", "Işığın kuantize enerji paketi"),
                w("VİRÜS", "Konak olmadan çoğalamayan patojen"),
                w("ENZİM", "Biyokimyasal tepkimeyi hızlandıran katalizör"),
                w("OKSİT", "Metal ile oksijenin birleşiminden doğan bileşik"),
                w("METAN", "Doğal gazın ana bileşeni, CH₄"),
                w("OKTAV", "Frekansın iki katına çıktığı aralık"),
            ],
            6: [
                w("PROTON", "Atom çekirdeğinde pozitif yüklü parçacık"),
                w("NÖTRON", "Çekirdekte yüksüz ağırlık merkezi"),
                w("İSOTOP", "Aynı proton sayısı, farklı kütle numarası"),
                w("GRAFİT", "Kurşun kalemin ucundaki karbon formu"),
                w("FİZYON", "Çekirdeğin bölünmesiyle enerji açığa çıkması"),
                w("FÜZYON", "Güneşin enerji üretimindeki birleşme süreci"),
            ],
            7: [
                w("PROTEİN", "Amino asit zincirlerinden oluşan makromolekül"),
                w("GRAVİTE", "Newton'un elma hikâyesindeki çekim kuvveti"),
                w("ANTİJEN", "Bağışıklık sistemini uyaran yabancı madde"),
                w("DİNAMİK", "Hareketin nedenlerini inceleyen fizik dalı"),
                w("ELEMENT", "Periyodik tablodaki saf madde birimi"),
                w("MOLEKÜL", "İki veya daha fazla atomun bağlandığı birim"),
            ],
            8: [
                w("ELEKTRİK", "Ampulü yakan, fırtınada çakan enerji"),
                w("MANYETİK", "Demir tozlarını kendine çeken alan özelliği"),
                w("ORGANİZM", "Canlılık gösteren bütün varlık"),
                w("KROMOZOM", "Genlerin sıralandığı yapı"),
                w("BİLİMSEL", "Deney ve kanıta dayanan yöntem"),
                w("HIZLANMA", "Hızın zamana göre değişim oranı"),
            ],
            9: [
                w("MİKROSKOP", "Gözle görülemeyeni büyüten optik alet"),
                w("RADYASYON", "Çernobil'de yayılan görünmez tehlike"),
                w("MATEMATİK", "İspat ve ispat arasındaki disiplin"),
                w("HİPOTENÜS", "Dik üçgende 90° karşısındaki kenar"),
                w("TELESKOP", "Uzak gök cisimlerini yakınlaştıran alet"),
                w("ANTİKOR", "Antijene karşı üretilen savunma proteini"),
            ],
        },
        [
            w("FOTOSENTEZ", "Klorofilin ışıkla CO₂'yi şekere dönüştürmesi"),
            w("ANTROPOLOJİ", "Homo sapiens'in kültürünü inceleyen bilim"),
            w("BİLİNÇALTI", "Freud'un buzdağının su altı katmanı"),
            w("BAKTERİYOLOJİ", "Pasteur'ün mikroskopta incelediği canlılar bilimi"),
            w("ELEKTROMANYETİK", "Maxwell denklemlerinin tanımladığı birleşik alan"),
            w("PSİKOLOJİST", "Rorschach testini uygulayabilen uzman"),
        ],
    ),
    "tarih": (
        "Tarih",
        "Uygarlıklar, savaşlar ve coğrafya",
        {
            3: [
                w("TÜR", "Oğuz boylarının ortak adlandırması"),
                w("KÖK", "Soy ağacında yukarı çıkıldığında varılan nokta"),
                w("ASK", "Orduya katılan silahlı er"),
                w("TUZ", "İpek Yolu'nda değerli takas malı"),
                w("GÖÇ", "Konar göçerlerin mevsimlik hareketi"),
                w("SUR", "Kaleyi çevreleyen taş duvar"),
            ],
            4: [
                w("ORDU", "Fatih'in fetihlerinde yürüttüğü güç"),
                w("TAHT", "Padişahın oturduğu, miras kavgası çıkaran yer"),
                w("TAPU", "Osmanlı'da toprağın mülkiyet belgesi"),
                w("KALE", "Kuşatmalarda son direniş noktası"),
                w("ANIT", "Geçmişi yaşatmak için dikilen taş yapı"),
                w("VAKF", "Osmanlı'da hayır kurumlarının hukuki çatısı"),
            ],
            5: [
                w("TİMAR", "Osmanlı'da sipahiye verilen gelir toprağı"),
                w("VAKIF", "Hayır işleri için ayrılan mülk sistemi"),
                w("FATİH", "1453'te Konstantinopolis'i alan padişah"),
                w("PRENS", "Taht varisi olabilecek soylu erkek"),
                w("SAVAŞ", "Barış antlaşmasıyla sona eren çatışma"),
                w("BEYLİK", "Osmanlı öncesi Türk devletcik yapısı"),
            ],
            6: [
                w("KERVAN", "İpek Yolu'nda develerle ilerleyen ticaret grubu"),
                w("SULTAN", "Osmanlı tahtında oturan unvan"),
                w("GÖÇEBE", "Konar göçer yaşam süren topluluk"),
                w("ORDUSU", "Padişahın emrindeki askerî güç"),
                w("PRENSİ", "Tahtın genç varisi"),
                w("TİMARI", "Sipahiye verilen toprak geliri"),
            ],
            7: [
                w("OSMANLI", "1299'da kurulan imparatorluk"),
                w("YUNANLI", "Antik felsefenin doğduğu halk"),
                w("SARAYLI", "Harem ve divanda görev yapan kişi"),
                w("TAPINAK", "Kutsal ayinlerin yapıldığı ibadet yapısı"),
                w("ANTALYA", "Akdeniz kıyısındaki antik Attaleia"),
                w("FETİHÇİ", "Surları aşarak şehir alan komutan"),
            ],
            8: [
                w("İSTANBUL", "1453'ten sonra fethedilen metropol"),
                w("YARIMADA", "Üç tarafı denizle çevrili kara parçası"),
                w("SICAKLIK", "Termometreyle ölçülen iklim değeri"),
                w("PASAPORT", "Sınır geçişinde sorulan resmî belge"),
                w("PERŞEMBE", "Haftanın Cuma'dan önceki günü"),
                w("ÇARŞAMBA", "Haftanın ortasına yakın günü"),
            ],
            9: [
                w("KARADENİZ", "Türkiye'nin kuzeyindeki iç deniz"),
                w("PAZARTESİ", "Haftanın ilk iş günü"),
                w("CUMARTESİ", "Hafta sonunun ilk günü"),
                w("DEMOKRASİ", "Halk egemenliğine dayanan yönetim"),
                w("ASTRONOMİ", "Gök cisimlerini inceleyen bilim"),
                w("ARKEOLOJİ", "Kazı ile geçmişi ortaya çıkaran bilim"),
            ],
        },
        [
            w("KONSTANTİNOPOLİS", "Bizans'ın başkenti, 1453'te düştü"),
            w("MİLLİMÜCADELE", "1919'da başlayan bağımsızlık savaşı"),
            w("LOZANANTLAŞMASI", "1923'te imzalanan barış belgesi"),
            w("OSMANLIİMPARATORLUĞU", "1299-1922 arası Türk devleti"),
            w("SELÇUKLULAR", "1071 Malazgirt zaferinin sahibi"),
            w("ANADOLUBİRLİĞİ", "Moğol baskısı sonrası kurulan beylikler"),
        ],
    ),
    "kultur": (
        "Kültür",
        "Edebiyat, sanat ve müzik",
        {
            3: [
                w("Şİİ", "Hece ve aruzla kurulan edebî tür"),
                w("NAZ", "Gazeldeki dize bölümü"),
                w("TEM", "Bestenin ana melodik fikri"),
                w("ROL", "Oyuncunun sahnede canlandırdığı karakter"),
                w("AHA", "Klasik Türk müziğinde makam adı"),
                w("EZO", "Anadolu ezgilerinde sık geçen kadın adı"),
            ],
            4: [
                w("DEST", "Epik anlatının uzun türü"),
                w("UYAK", "Şiirdeki ses benzerliği düzeni"),
                w("ARUZ", "Divân edebiyatının vezin sistemi"),
                w("NOTA", "Müzikte sesin yazıya dökülmüş hali"),
                w("OVA", "Antik tiyatroda koronun söylediği bölüm"),
                w("DİZE", "Şiirin tek satırlık birimi"),
            ],
            5: [
                w("GİRİŞ", "Roman ve makalenin açılış bölümü"),
                w("ŞİİR", "Dize, mısra ve nazım birimi"),
                w("MAKAM", "Türk müziğinde melodi dizisi"),
                w("EZGİ", "Kulaktan kulağa aktarılan melodi"),
                w("METİN", "Sahnedeki oyuncunun söyledikleri"),
                w("KİTAP", "Cilt, sayfa ve kapaktan oluşan eser"),
            ],
            6: [
                w("HEYKEL", "Rodin'in düşünen adamı gibi üç boyutlu sanat"),
                w("KONSER", "Canlı icra dinlenen müzik etkinliği"),
                w("POSTER", "Film afişi olarak duvara asılan görsel"),
                w("OYUNCU", "Sahne veya sette rol alan sanatçı"),
                w("MİSAİR", "Antik piramitlerin bulunduğu ülke"),
                w("BESTECİ", "Müzik eseri yazan kişi"),
            ],
            7: [
                w("ROMANCI", "Uzun anlatı yazan edebiyatçı"),
                w("FRAGMAN", "Sinemada film öncesi gösterilen tanıtım"),
                w("ŞAİRANE", "Şiire yakışır, duygusal üslup"),
                w("MAKAMCI", "Klasik Türk müziğinde makam bilgini"),
                w("KONSERİ", "Salonda dinlenen canlı müzik etkinliği"),
                w("SAHNELİ", "Perde ve seyirci gerektiren gösteri"),
            ],
            8: [
                w("FOTOĞRAF", "Işıkla yakalanan donmuş an"),
                w("YÖNETMEN", "Filmin görsel anlatımından sorumlu kişi"),
                w("FİLOLOJİ", "Dilleri inceleyen bilim dalı"),
                w("MÜZİSYEN", "Enstrüman çalan profesyonel sanatçı"),
                w("ELEŞTİRİ", "Eserin niteliğini değerlendiren yazı"),
                w("MANTIKLI", "Tutarlı düşünce zinciri"),
            ],
            9: [
                w("KÜTÜPHANE", "Kitapların korunduğu sessiz mekân"),
                w("PSİKOLOJİ", "Zihinsel süreçleri inceleyen bilim"),
                w("MİMARLIK", "Yapı tasarlama sanatı ve mesleği"),
                w("DEKORATÖR", "Sahne ve set düzenleyen sanatçı"),
                w("BESTECİLİK", "Müzik eseri yazma sanatı"),
                w("SERAMİKÇI", "Kilden kap ve heykel yapan zanaatkâr"),
            ],
        },
        [
            w("FOTOĞRAFÇILIK", "Işık ve gölgeyle an yakalama sanatı"),
            w("ELEŞTİRMEN", "Eserleri değerlendiren yazın adamı"),
            w("KALİGRAFİ", "Güzel yazı sanatı"),
            w("MINYATÜR", "Osmanlı el yazması kitap süslemesi"),
            w("TRANSPOSİZYON", "Müzikte ezgiyi başka tona taşıma"),
            w("EXISTANSİYALİZM", "Sartre'ın varoluşçu felsefesi"),
        ],
    ),
    "doga": (
        "Doğa",
        "Bitkiler, hayvanlar ve doğa olayları",
        {
            3: [
                w("KIŞ", "Kar yağışının baskın olduğu mevsim"),
                w("YAZ", "Gündönümüne en yakın sıcak mevsim"),
                w("ÇIĞ", "Dağ yamacından kopan kar kütlesi"),
                w("GÖL", "Kara içinde kapalı su kütlesi"),
                w("DAĞ", "Yüksek arazi formu"),
                w("NEM", "Havadaki su buharı oranı"),
            ],
            4: [
                w("KURT", "Masallardaki yabani köpek türü"),
                w("YILAN", "Sürüngenler sınıfından, zehirli olabilen"),
                w("KART", "Yırtıcı kuş familyasının büyük üyesi"),
                w("OVAJ", "Yamaçtan aşağı kayan toprak kütlesi"),
                w("AĞAÇ", "Odun dokulu, gövdeli bitki"),
                w("YUNU", "Koyundan elde edilen lif"),
            ],
            5: [
                w("KUNDU", "Ormanlarda yaşayan, misk salgılayan hayvan"),
                w("SELVİ", "Uzun boylu, ince yapraklı ağaç"),
                w("YILKI", "Vahşi doğada yetişen at sürüsü"),
                w("ASLAN", "Ormanların kralı olarak anılan yırtıcı"),
                w("AKREP", "Çöl ve kayalıklarda yaşayan zehirli sürüngen"),
                w("ÇAKAL", "Leşle beslenen, uluyan yırtıcı"),
            ],
            6: [
                w("BAYKUŞ", "Gece avlanan, büyük gözlü kuş"),
                w("KUNDUZ", "Baraj yapabilen kemirgen"),
                w("SİNCAP", "Ağaçta yaşayan, fındık toplayan hayvan"),
                w("JAGUAR", "Güney Amerika'nın benekli yırtıcısı"),
                w("LEOPAR", "Afrika'da benekli büyük kedi"),
                w("SANSAR", "Gece avlanan, kürkü değerli hayvan"),
            ],
            7: [
                w("OKYANUS", "Dünyanın en büyük su kütlesi"),
                w("HABİTAT", "Bir canlının doğal yaşam alanı"),
                w("KASIRGA", "Tropik siklonun şiddetli hali"),
                w("KURAKLI", "Uzun süre yağmur görmeme hali"),
                w("YILDIRI", "Gökyüzünden inen elektrik boşalması"),
                w("TSUNAMİ", "Deprem sonrası okyanusta yükselen dev dalga"),
            ],
            8: [
                w("FLAMINGO", "Pembe tüylü, tek ayakta duran kuş"),
                w("ATMOSFER", "Yeryüzünü saran gaz tabakası"),
                w("YILDIRIM", "Gökyüzünden inen elektrik boşalması"),
                w("ORANGUTA", "Borneo ormanlarında yaşayan primat"),
                w("MANTARCI", "Mantar toplayan veya yetiştiren kişi"),
                w("VOLKANIK", "Volkanlaşmayla ilgili süreç"),
            ],
            9: [
                w("ORANGUTAN", "Borneo ormanlarında yaşayan primat"),
                w("MANTARLIK", "Mantarların doğal olarak yetiştiği alan"),
                w("FOTOPLANK", "Denizde fotosentez yapan mikroskobik canlı"),
                w("OKSİJENLİ", "Solunum için gerekli gazı içeren"),
                w("HEYELANLI", "Toprak kaymasına yatkın arazi"),
                w("MİKROPLAN", "Görünmez canlıların kolonisi"),
            ],
        },
        [
            w("FOTOSENTEZ", "Bitkilerin güneş ışığıyla besin üretmesi"),
            w("BİYOÇEŞİTLİLİK", "Bir ekosistemdeki tür zenginliği"),
            w("MİKROORGANİZMA", "Çıplak gözle görülemeyen canlı"),
            w("KARBONAYAKİZİ", "Fosil yakıt tüketiminin çevresel etkisi"),
            w("OKSİJENKONSANTRASYONU", "Atmosferdeki O₂ oranı"),
            w("EKOSİSTEM", "Canlılar ve çevrelerinin bütünü"),
        ],
    ),
    "kavram": (
        "Kavram",
        "Felsefe, mantık ve soyut düşünce",
        {
            3: [
                w("AKL", "Descartes'in kuşkulanmadığı tek şey"),
                w("VAR", "Heidegger'in sorguladığı temel kavram"),
                w("YOK", "Hiçlik felsefesinin konusu"),
                w("NEF", "Platon'un ideal form düşüncesi"),
                w("İDE", "Platon'un idealar dünyasındaki birim"),
                w("GER", "Gerçekliğin özüne işaret eden kısaltma"),
            ],
            4: [
                w("ÖZDE", "Bir şeyin değişmeyen doğası"),
                w("DİLE", "Dilek ve arzu bildiren sözcük"),
                w("AMAÇ", "Aristoteles'in telos kavramı"),
                w("NİYE", "Neden sorusunun kısaltılmış hali"),
                w("KANT", "Saf aklın eleştirisinin yazarı"),
                w("AKIL", "Muhakeme ve düşünme yetisi"),
            ],
            5: [
                w("ÖZGÜR", "Kant'ın sorduğu irade hali"),
                w("İSPAT", "Tezi doğrulayan mantıksal kanıt"),
                w("ÖNERM", "Doğru veya yanlış olabilen ifade"),
                w("TEORİ", "Gözlemleri açıklayan düşünce sistemi"),
                w("DEİZM", "Tanrı'ya inanıp vahye şüphe duyan görüş"),
                w("TEZİS", "Savunulan ana düşünce"),
            ],
            6: [
                w("MEDENİ", "Uygar toplum düzenine ait"),
                w("DİALET", "Tez antitez sentez yöntemi"),
                w("ÖNERGE", "Meclise sunulan yasa taslağı"),
                w("KANTÇI", "Saf aklın eleştirisi okuluna mensup"),
                w("SOKRAT", "Sorgulama yönteminin kurucusu"),
                w("ÖZGÜRL", "Özgür olma durumunun kökü"),
            ],
            7: [
                w("FELSEFE", "Bilgelik sevgisi, Sokrates'in alanı"),
                w("PARADOK", "Çelişkili görünen ama doğru olabilen önerme"),
                w("DİALETİ", "Tez antitez sentez yöntemi"),
                w("UTILİTE", "Faydacılığın ölçtüğü değer"),
                w("ONTOLOJ", "Varlığın doğasını inceleyen dal"),
                w("EPİSTEM", "Bilgi kuramının kök kavramı"),
            ],
            8: [
                w("NİHİLİZM", "Hiçbir değerin mutlak olmadığı akım"),
                w("UTILİTAR", "En çok sayıya en çok mutluluk ilkesi"),
                w("ONTOLOJİ", "Varlığın doğasını inceleyen dal"),
                w("DETERMİN", "Her olayın nedeni olduğu görüş"),
                w("HERMENEU", "Metin yorumlama sanatının kökü"),
                w("METAFİZİ", "Varlığın ötesini sorgulayan felsefe"),
            ],
            9: [
                w("METAFİZİK", "Varlığın ötesini sorgulayan felsefe dalı"),
                w("POSTMODER", "Büyük anlatıları reddeden akım"),
                w("DETERMİST", "Her olayın nedeni olduğuna inanan"),
                w("VAROLUŞCU", "Sartre'ın temsil ettiği felsefi akım"),
                w("FAYDACILI", "En büyük faydayı hedefleyen etik görüş"),
                w("ONTOLOJİK", "Varlık sorunlarıyla ilgili"),
            ],
        },
        [
            w("EXISTANSİYALİZM", "Sartre'ın varoluşçu felsefesi"),
            w("POSTMODERNİZM", "Büyük anlatıları reddeden akım"),
            w("TRANSCENDENTAL", "Kant'ın deney ötesi sorgulaması"),
            w("HERMENEUTİK", "Metin yorumlama sanatı"),
            w("UTILITARIANISM", "Faydacılık felsefesinin İngilizce adı"),
            w("FENOMENOLOJİ", "Özdeneyimin incelendiği felsefe"),
        ],
    ),
}


def build_categories() -> dict:
    categories: dict = {}
    for key, (label, description, by_len, bonus) in RAW.items():
        words_by_length: dict[int, list] = {}
        for length, items in by_len.items():
            cleaned = []
            seen: set[str] = set()
            for word, hint in items:
                if len(word) != length or word in seen:
                    continue
                seen.add(word)
                cleaned.append({"word": word, "hint": hint})
            if len(cleaned) < 4:
                bad = [(word, len(word)) for word, _ in items if len(word) != length]
                raise ValueError(f"{key} length {length}: only {len(cleaned)} valid ({bad})")
            words_by_length[length] = cleaned

        bonus_clean = []
        seen = set()
        for word, hint in bonus:
            if len(word) < 10 or word in seen:
                continue
            seen.add(word)
            bonus_clean.append({"word": word, "hint": hint})
        if len(bonus_clean) < 4:
            raise ValueError(f"{key} bonus: only {len(bonus_clean)} valid")

        categories[key] = {
            "label": label,
            "description": description,
            "words_by_length": words_by_length,
            "bonus": bonus_clean,
        }
    return categories


def main() -> None:
    categories = build_categories()
    output = Path(__file__).resolve().parent / "words.py"
    content = (
        '"""Categorized Turkish word bank with harder clues."""\n\n'
        "REVEAL_INTERVAL_SECONDS = 7\n"
        "POINTS_PER_HIDDEN_LETTER = 10\n"
        "TOTAL_QUESTIONS = 8\n\n"
        "CATEGORIES: dict[str, dict] = \\\n"
        f"{pformat(categories, width=120, sort_dicts=False)}\n"
    )
    output.write_text(content, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
