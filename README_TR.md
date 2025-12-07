# 🖼️ Dynamic Screen BG - Dinamik Ekran Arkaplanı

**[🇹🇷 Türkçe](README_TR.md)** | **[🇬🇧 English](README_EN.md)**

---

**Dynamic Screen BG**, çoklu monitör kurulumları için özel olarak tasarlanmış, modern arayüze sahip gelişmiş bir duvar kağıdı yönetim aracıdır. Her monitörünüzü bağımsız olarak yönetin, galeriler oluşturun ve ekranlarınızın havasını otomatik olarak değiştirin.

## 🌟 Öne Çıkan Özellikler

### 🖥️ Çoklu Monitör Yönetimi
- Sisteme bağlı tüm monitörleri **otomatik algılar**
- Her monitör için **bağımsız galeri** ve **zamanlayıcı** ayarı
- Farklı çözünürlükteki monitörler için akıllı **görsel birleştirme (stitching)** teknolojisi
- Her monitör için ayrı duvar kağıdı koleksiyonu oluşturabilme

### 🎨 Modern ve Kullanıcı Dostu Arayüz
- **Karanlık Mod (Dark Theme):** Göz yormayan, şık ve modern renk paleti
- **Drag & Drop (Sürükle-Bırak):** Galeri içindeki görsellerin sırasını kolayca değiştirin
- **Number Stepper:** Süre ayarları için hassas ve kullanımı kolay sayısal kontrol
- **Kompakt Tasarım:** Header ve sidebar alanları kullanımı kolaylaştıran modern ikonlar ve yerleşim
- **Gerçek Zamanlı Önizleme:** Değişiklikleri anında görün

### ⚙️ Sistem Özellikleri
- **System Tray (Sistem Tepsisi) Entegrasyonu:** 
  - Uygulama kapatıldığında sistem tepsisine küçülür
  - Sağ tık menüsü: Uygulamayı Göster / Çıkış
  - Arka planda çalışmaya devam eder
- **Windows Entegrasyonu:** Özel uygulama ikonu (`icon.ico`)
- **Kalıcı Ayarlar:** Tüm tercihleriniz ve galerileriniz otomatik kaydedilir (`monitor_config.json`)
- **Log Sistemi:** Uygulama aktivitelerini izleyin (açılıp kapatılabilir)

### 🌍 Çok Dilli Destek
- **Türkçe** ve **İngilizce** tam destek
- Ayarlar menüsünden anında dil değişimi
- Dil tercihi otomatik olarak kaydedilir

### 🎯 Otomatik Arkaplan Değiştirme
- Monitör bazında özelleştirilebilir zamanlayıcı (saniye cinsinden)
- Her monitör için bağımsız aktif/pasif kontrolü
- Sıralı görsel değişimi (circular rotation)
- Arkaplan değişimini istediğiniz zaman durdurup başlatabilme

## 📸 Ekran Görüntüleri

| Ana Ekran ve Galeri | Ayarlar Paneli |
|:-------------------:|:--------------:|
| ![Screenshot 1](screenshots/main.png) | ![Screenshot 2](screenshots/settings.png) |

*Not: Ekran görüntülerini `screenshots` klasörüne ekleyebilirsiniz.*

## 🚀 Kurulum ve Çalıştırma

### Sistem Gereksinimleri
- **İşletim Sistemi:** Windows 10/11
- **Python:** 3.10 veya üzeri (kaynak koddan çalıştırma için)
- **RAM:** Minimum 2GB
- **Disk Alanı:** ~50MB (kurulum için)

### Gerekli Kütüphaneler
```
flet>=0.21.0          # Modern UI Framework
Pillow>=9.0.0         # Görsel işleme
pystray>=0.19.0       # Sistem tepsisi
pywin32>=305          # Windows API
comtypes>=1.1.10      # COM API
```

### Adım Adım Kurulum

#### 1. Kaynak Koddan Çalıştırma
```bash
# Projeyi klonlayın veya indirin
git clone https://github.com/MustafaBKLZ/DynamicScreenBG.git
cd DynamicScreenBG

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python main_v2.py
```

**Alternatif:** `baslat_v2.bat` dosyasına çift tıklayın.

#### 2. EXE Oluşturma (Standalone)
```bash
# Build işlemini başlatın
build_exe_v2.bat
```
Bu işlem:
- Gerekli paketleri yükler (`flet`, `pyinstaller`)
- Uygulamayı tek bir `.exe` dosyasına paketler
- `dist` klasörü altında `DynamicScreenBG.exe` oluşturur
- Tüm kaynakları (locales, ikonlar, SVG dosyaları) dahil eder

**Not:** EXE dosyası başka bilgisayarlarda Python kurulumu olmadan çalışır.

## 📖 Kullanım Kılavuzu

### İlk Çalıştırma
1. Uygulamayı başlattığınızda sol tarafta mevcut monitörleriniz listelenecektir
2. Bir monitör seçin (tıklayın)
3. Sağ üst köşeden **"Resim Ekle"** butonuna tıklayın
4. Galeri için resimler seçin (çoklu seçim desteklenir)
5. **"Otomatik Değişim"** switch'ini aktif edin
6. Değişim süresini ayarlayın (saniye cinsinden)
7. **"Kaydet"** butonuna tıklayın

### Görsel Sıralama
- Galeri içindeki görselleri **sürükleyip bırakarak** yeniden sıralayabilirsiniz
- Görsellerin üzerindeki **X** butonuyla silebilirsiniz
- **"Tümünü Temizle"** butonu ile tüm galeriyi temizleyebilirsiniz

### Ayarlar Menüsü
- **Dil Değiştirme:** Türkçe ↔ İngilizce
- **Log Gösterimi:** Log panelini açıp kapatın
- Tüm ayarlar otomatik olarak kaydedilir

### Sistem Tepsisi Kullanımı
- Pencereyi kapattığınızda uygulama arka planda çalışmaya devam eder
- Sistem tepsisindeki ikona **sağ tıklayarak**:
  - Uygulamayı tekrar açabilirsiniz
  - Tamamen kapatabilirsiniz

## 🛠️ Teknik Detaylar

### Mimari ve Teknolojiler
```
┌─────────────────────────────────────────┐
│           Flet UI (Flutter)             │  ← Modern, responsive UI
├─────────────────────────────────────────┤
│      App Logic (main_v2.py)             │  ← Ana uygulama mantığı
├─────────────────────────────────────────┤
│  Wallpaper Service (wallpaper_service)  │  ← Monitör ve duvar kağıdı yönetimi
├─────────────────────────────────────────┤
│    Windows API (pywin32, ctypes)        │  ← Sistem entegrasyonu
└─────────────────────────────────────────┘
```

### Kullanılan Kütüphaneler
- **[Flet](https://flet.dev/):** Flutter tabanlı Python UI framework
- **[Pillow (PIL)](https://pillow.readthedocs.io/):** Görsel işleme, resizing, center-crop, image stitching
- **[pystray](https://pystray.readthedocs.io/):** Sistem tepsisi entegrasyonu
- **[pywin32](https://github.com/mhammond/pywin32):** Windows API erişimi (`SystemParametersInfoW`, `EnumDisplayMonitors`)

### Görsel İşleme Algoritması
1. **Monitör Algılama:** `EnumDisplayMonitors` ile tüm monitörler ve konumları tespit edilir
2. **Görsel Boyutlandırma:** Her görsel, hedef monitörün aspect ratio'suna göre yeniden boyutlandırılır
3. **Center Crop:** Fazla alanlar kesilerek görsel merkezlenir
4. **Stitching:** Tüm monitör görselleri tek bir canvas üzerinde birleştirilir
5. **Sistem Duvar Kağıdı:** Birleştirilmiş görsel Windows duvar kağıdı olarak ayarlanır

### Konfigürasyon Dosyası
`monitor_config.json` yapısı:
```json
{
  "app_settings": {
    "language": "tr",
    "show_logs": true
  },
  "\\\\.\\DISPLAY1": {
    "images": ["C:/path/to/image1.jpg", "C:/path/to/image2.jpg"],
    "interval": 60,
    "enabled": true,
    "last_index": 0
  }
}
```

### Thread Yönetimi
- **Ana Thread:** UI render ve kullanıcı etkileşimi
- **Background Timer Thread:** Her monitör için zamanlayıcı kontrolü ve duvar kağıdı güncelleme
- **System Tray Thread:** Sistem tepsisi ikonu yönetimi

## 🔧 Geliştirici Notları

### Kod Yapısı
```
DynamicScreenBG/
├── main_v2.py              # Ana uygulama ve UI
├── wallpaper_service.py    # Servis katmanı
├── locales/                # Dil dosyaları
│   ├── tr.json
│   └── en.json
├── monitor_config.json     # Kullanıcı ayarları (otomatik)
├── icon.ico                # Uygulama ikonu
├── github.svg              # GitHub ikonu
├── x.svg                   # X (Twitter) ikonu
├── requirements.txt        # Python bağımlılıkları
├── baslat_v2.bat          # Çalıştırma script'i
└── build_exe_v2.bat       # Build script'i
```

### Custom UI Components
- **`NumberStepper`:** Increment/decrement butonları ile sayısal input
- **`MonitorCard`:** Sidebar'daki monitör kartları
- **`LanguageManager`:** Çok dilli destek sistemi

### Yeni Özellik Ekleme
1. UI değişiklikleri için `main_v2.py` / `App` sınıfını düzenleyin
2. Servis mantığı için `wallpaper_service.py` / `WallpaperService` sınıfını düzenleyin
3. Yeni dil stringleri için `locales/tr.json` ve `locales/en.json` güncelleyin

## 🐛 Bilinen Sorunlar ve Çözümler

### Sorun: EXE çalışmıyor
**Çözüm:** Windows Defender veya antivirüs yazılımınız engelliyor olabilir. Uygulamayı güvenilir listesine ekleyin.

### Sorun: Duvar kağıdı değişmiyor
**Çözüm:** 
- "Otomatik Değişim" switch'inin aktif olduğundan emin olun
- En az 2 resim eklediğinizden emin olun
- Log panelini açıp hata mesajlarını kontrol edin

### Sorun: Monitör algılanmıyor
**Çözüm:** Uygulamayı yeniden başlatın. Sorun devam ederse, Windows ekran ayarlarından monitörün aktif olduğundan emin olun.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:
1. Projeyi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Değişiklik Geçmişi

### v2.0.0 (Mevcut)
- ✨ Modern Flet UI
- ✨ Çok dilli destek (TR/EN)
- ✨ Drag & drop galeri sıralaması
- ✨ Log sistemi
- ✨ Sistem tepsisi entegrasyonu
- 🐛 Monitör algılama iyileştirmeleri

## 📄 Lisans

Bu proje açık kaynaklıdır ve özgürce kullanılabilir.

---

<div align="center">

**Geliştirici: Mustafa Bükülmez**

[![GitHub](https://img.shields.io/badge/GitHub-MustafaBKLZ-181717?style=for-the-badge&logo=github)](https://github.com/MustafaBKLZ)
[![Twitter](https://img.shields.io/badge/X-@BukulmezMustafa-1DA1F2?style=for-the-badge&logo=x)](https://x.com/BukulmezMustafa)

</div>
