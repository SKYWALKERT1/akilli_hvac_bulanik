# 🌡️ Akıllı Ev HVAC Sistemi — Bulanık Mantık Tabanlı Kontrolcü

> **Bulanık Mantık Dersi — Dönem Projesi**
> Mersin Üniversitesi · 2026

5 giriş ve 2 çıkış değişkenli, **20 kurallı** Mamdani çıkarım sistemi kullanarak akıllı ev iklimlendirme (HVAC) sistemini bulanık mantıkla kontrol eden tam kapsamlı bir uygulama.

---

## 📌 Proje Özeti

Bu proje, gerçek dünyadaki bir HVAC (Heating, Ventilation, Air Conditioning) sisteminin bulanık mantık ile nasıl kontrol edilebileceğini gösterir. Klasik PID kontrolcülerin aksine bulanık mantık, insan deneyimine yakın **dilsel kurallar** ile çalışır:

> _"Eğer **iç sıcaklık SICAK** ve **dış sıcaklık SICAK** ve **kişi sayısı ÇOK** ise → Fan **MAKSİMUM**, Güç **GÜÇLÜ_SOĞUTMA**"_

### Sistem Özellikleri
| Özellik | Değer |
|---|---|
| Giriş değişkeni | **5** (iç sıcaklık, dış sıcaklık, nem, kişi sayısı, saat) |
| Çıkış değişkeni | **2** (fan hızı, ısıtma/soğutma gücü) |
| Toplam dilsel terim | **29** (19 giriş + 10 çıkış) |
| Kural sayısı | **20** (gereksinim ≥15) |
| Çıkarım yöntemi | **Mamdani** |
| Durulaştırma | **Centroid (ağırlık merkezi)** |

---

## 🚀 Kurulum

### 1. Depoyu klonlayın
```bash
git clone https://github.com/SKYWALKERT1/akilli_hvac_bulanik.git
cd akilli-hvac-bulanik
```

### 2. Sanal ortam (önerilir)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları kurun
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı çalıştırın
```bash
streamlit run app.py
```

Tarayıcı otomatik olarak `http://localhost:8501` adresinde açılır.

---

## 🎮 Kullanım

1. **Sol kenar çubuğundan** 5 girişi slider ile ayarlayın:
   - 🏠 İç Sıcaklık (0–40 °C)
   - 🌍 Dış Sıcaklık (-10–45 °C)
   - 💧 Nem (%0–100)
   - 👥 Kişi Sayısı (0–10)
   - 🕐 Günün Saati (0–23)
2. **"Otomatik hesapla"** açıkken sistem anlık sonuç üretir; kapalıysa "HESAPLA" tuşuna basın.
3. Üst panelde:
   - Çalışma Modu (Soğutma / Isıtma / Beklemede)
   - Fan Hızı (%)
   - Isıtma/Soğutma Gücü (-100 .. +100)
4. **"Aktif Kurallar"** bölümünde hangi kuralların hangi güçle ateşlendiğini görün.
5. **"Test Senaryoları"** bölümünde önceden tanımlı 10 senaryonun tablosunu inceleyin.

---

## 🧠 Bulanık Mantık Mimarisi

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────┐
│   GİRİŞLER      │ →  │ BULANIKLAŞTIRMA  │ →  │ ÇIKARIM MOTORU  │ →  │ DURULAŞTIRMA │
│ 5 sayısal değer │    │ Üyelik fonks.    │    │   20 KURAL      │    │   Centroid   │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────┘
                                                                              │
                                                                              ▼
                                                                    ┌─────────────────┐
                                                                    │    ÇIKIŞLAR     │
                                                                    │ Fan%, Güç birim │
                                                                    └─────────────────┘
```

### Üyelik Fonksiyonları
Tüm değişkenler **üçgen (trimf)** ve **yamuk (trapmf)** üyelik fonksiyonları kullanır.

| Değişken | Dilsel Terimler |
|---|---|
| İç Sıcaklık | soğuk, serin, ideal, ılık, sıcak |
| Dış Sıcaklık | çok_soğuk, soğuk, ılıman, sıcak |
| Nem | kuru, normal, nemli, çok_nemli |
| Kişi Sayısı | az, orta, çok |
| Saat | gece, sabah, öğlen, akşam |
| Fan Hızı | kapalı, düşük, orta, yüksek, maksimum |
| Isıtma/Soğutma | güçlü_soğutma, soğutma, kapalı, ısıtma, güçlü_ısıtma |

---

## 📊 Test Sonuçları

| Senaryo | İç °C | Dış °C | Nem % | Kişi | Saat | Fan | Güç | Mod |
|---|--:|--:|--:|--:|--:|--:|--:|---|
| Yaz öğleni kalabalık | 35 | 38 | 70 | 8 | 14 | 92.6% | -80.6 | Soğutma |
| Kış gecesi az kişi | 12 | -5 | 40 | 1 | 2 | 40.0% | +78.9 | Isıtma |
| İdeal bahar | 22 | 20 | 50 | 3 | 11 | 26.9% | 0.0 | Beklemede |
| Tropikal | 32 | 30 | 92 | 4 | 15 | 91.4% | -78.0 | Soğutma |
| Soğuk sabah ofis | 15 | 5 | 45 | 7 | 8 | 37.5% | +55.0 | Isıtma |
| Buz gibi boş oda | 8 | -8 | 35 | 0 | 4 | 40.0% | +80.6 | Isıtma |

> ✅ Tüm sınır durumlarda sistem mantıklı kararlar veriyor.

---

## 📁 Proje Yapısı

```
akilli-hvac-bulanik/
├── app.py                  # Ana Streamlit uygulaması
├── test_system.py          # Streamlit'siz hızlı test scripti
├── requirements.txt        # Python bağımlılıkları
├── README.md               # Bu dosya
└── docs/
    └── RAPOR.md            # Detaylı proje raporu
```

---

## 🛠️ Kullanılan Teknolojiler

- **[scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/)** — Bulanık mantık kütüphanesi
- **[Streamlit](https://streamlit.io/)** — İnteraktif arayüz
- **[NumPy](https://numpy.org/)** — Sayısal işlemler
- **[Matplotlib](https://matplotlib.org/)** — Grafikler
- **[Pandas](https://pandas.pydata.org/)** — Tablo gösterimi

---

## 📄 Lisans

Bu proje eğitim amaçlıdır. Mersin Üniversitesi Bulanık Mantık dersi için hazırlanmıştır.

---

## 👤 Geliştirici

**Furkan Fatih Çiftçi**  
Bilgisayar Mühendisliği · Mersin Üniversitesi  s
🎓 Öğrenci No: 22430070037  
🐙 GitHub: https://github.com/SKYWALKERT1/akilli_hvac_bulanik
