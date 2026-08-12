# Marka Kiti

## Renkler

Tüm gradyan geçişleri **mavidir**. Yeşil yalnızca güven/onay rozetlerinde kullanılır.

### Mavi — ana palet

| Rol | Ad | HEX | Kullanım |
|---|---|---|---|
| Zemin | Beyaz | `#FFFFFF` | Ana zemin. Logo daima burada durur. |
| Açık yüzey | Ice Blue | `#D6E6F3` | Kart zeminleri, ayırıcılar |
| Orta ton | Powder Blue | `#A6C5D7` | İkincil metin, ince çizgiler |
| Vurgu | **Sapphire** | `#0F52BA` | Başlık vurgusu, CTA, bağlantı |
| Derinlik | **Deep Navy** | `#000926` | Koyu bölümler, gövde metni |

### Logo mavileri — logodan örneklenmiştir

| Ad | HEX | Kullanım |
|---|---|---|
| Logo Deep | `#005478` | Gradyan bitişi, koyu metin vurgusu |
| **Logo Blue** | `#0C6C90` | **Ana aksan** — logonun kendi rengi |
| Logo Mid | `#18789C` | Gradyan ara durağı |
| Logo Bright | `#48B4CC` | Dalga, ikon, canlı vurgu |
| Logo Light | `#9CD8E4` | Dalga katmanı, açık zemin |
| Logo Pale | `#D8F0F0` | En açık su tonu |

### Yeşil — ikincil güven aksanı

| Ad | HEX | Kullanım |
|---|---|---|
| Mint Whisper | `#D1F2EB` | Rozet zemini |
| Emerald | `#50C878` | Onay işareti |
| Forest | `#0B6E4F` | "%0 Faiz", "Kefilsiz" rozet metni |
| Dark Evergreen | `#013220` | Rozet üzerinde koyu metin |

> Yeşil **gradyanlarda kullanılmaz**. Yalnızca küçük rozet, tik işareti ve
> "faizsiz / kefilsiz / bankasız" gibi güven ifadelerinde görünür.

### Marka gradyanı

Derinden yüzeye, her zaman bu sırayla:

```
#000926 → #061A4A → #0F52BA → #0C6C90 → #18789C
Deep Navy  Midnight   Sapphire   Logo Blue  Logo Mid
```

Kısa gradyan (buton, ikon kutusu):
```
#0F52BA → #0C6C90 → #18789C
```

Açık gradyan (dalga, arka plan):
```
#18789C → #48B4CC → #9CD8E4
```

---

## Tipografi

| Rol | Font | Ağırlık | Not |
|---|---|---|---|
| Başlık | **Marcellus** | 400 | Logodaki Trajan tarzı serifin devamı. Tek ağırlık — kalınlaştırmayın, sentetik bold logoyu bozar. |
| Gövde / UI | **Manrope** | 300–800 | Uzun Türkçe metinde yüksek okunabilirlik |

Vurgu, kalınlıkla değil **ölçek ve gradyan** ile verilir.

Ücretsiz indirme: Google Fonts → Marcellus, Manrope.
Depoda hazır: `brand-source/fonts/`

### Etiket (eyebrow) stili
Büyük harf · harf aralığı `0.16em` · Manrope 700 · 12 px

---

## Logo kuralları

### Dosyalar (`public/brand/`)

| Dosya | Kullanım |
|---|---|
| `logo-ocean.png/webp` | Tam kilit, beyaz zeminli — sunum, doküman |
| `logo-ocean-trim.png/webp` | Tam kilit, şeffaf — beyaz yüzeylere yerleştirme |
| `mark-ocean.png/webp` | Yalnız işaret (M + dalga), beyaz zeminli |
| `mark-ocean-trim.png/webp` | Yalnız işaret, şeffaf — profil fotoğrafı |

### Yapılır ✓

- Logo **daima beyaz zeminde** durur
- Koyu görselde logo beyaz, yuvarlatılmış köşeli bir plaketin içine alınır
- Etrafında en az logo yüksekliğinin **%25'i** kadar boşluk bırakılır
- Profil fotoğrafı olarak `mark-ocean-trim` (beyaz zeminli kare) kullanılır

### Yapılmaz ✗

- Renk değiştirilmez, tek renge çevrilmez, gölge/kontur eklenmez
- Fotoğraf üzerine doğrudan bindirilmez (önce beyaz plaket)
- Oranı bozulmaz, döndürülmez, eğilmez
- Üzerine yazı veya rozet yerleştirilmez
- Kelime markası yeniden dizilmez (fontla taklit edilmez)

---

## Dalga motifi — markanın imzası

Logonun altındaki dalga, markanın tekrar eden görsel imzasıdır. Sitede bölüm
geçişlerinde, sayfa geçiş animasyonunda ve arka planda kullanılır. Sosyal
medyada da aynı işi görür:

- **Gönderi üst bandı:** gradyan bant + altında beyaz dalga → içerik beyaz zeminde
- **Story alt bandı:** ters çevrilmiş dalga + gradyan taban
- **Ayırıcı:** iki içerik bloğu arasında ince, tek katman dalga

Dalga her zaman **üç katmanlıdır** (açık → orta → koyu), tıpkı logodaki gibi.
SVG yolları: `src/components/ui/Wave.tsx` → `WAVE_PATHS`.

---

## Ton ve dil

| Evet | Hayır |
|---|---|
| Net, sakin, güven veren | Bağırgan, acele ettiren |
| "Bankasız, faizsiz, kefilsiz" | "Kaçırma!", "Son fırsat!" |
| Rakamla konuşan (660 daire, 60 ay) | Belirsiz abartı ("en iyi", "eşsiz fırsat") |
| Kooperatif modelini açıklayan | Modeli gizleyen |
| Türkçe karakterleri doğru kullanan | "MIA" (doğrusu **MİA**) |

**Yasak ifadeler:** "garanti getiri", "kesin kazanç", "riski yok", "devlet garantili".
Kooperatif mevzuatı ve reklam kuralları açısından risklidir.
