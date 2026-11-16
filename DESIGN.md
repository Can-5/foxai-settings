# FoxAI Settings — Tasarım Yönü (Redesign)

Bu dosya, 2026-11-16 "AI slop" eleştirisi sonrası arayüzün yönünü belirler.
Amaç: hazır template değil, bu ürüne özgü, elle kurgulanmış bir enstrüman paneli.

## Yön: "Atölye enstrümanı" (instrument workbench)

Sıcak grafit zemin + pirinç (brass) tek vurgu rengi. Düz yüzeyler, 1px hatlar,
yükseltme yok. Cantarell (Türkçe glifleri tam), kod için Liberation Mono.
Araç hissi: her kontrol adı görünür, etiketler sentence-case, büyük harf + tracking yasak.

Neden: uygulama bir sistem ayarları merkezi — fırça değil anahtar takımı gibi
hissettirmeli.

## Bilinçli olarak kullanılmayanlar (anti-references)

- Tailwind slate paleti (`#0f172a` / `#1e293b` / `#409eff`) — en ucuz AI default'u.
- Inter / Roboto / Arial — tema-izsiz font.
- Mor-cyan gradient, cam (glass), neon glow.
- Emoji nav ikonu, uppercase tracked "eyebrow" etiketler.
- Her ekrana aynı uniform kart ızgarası.

## Palet (tokenlar — yalnız `theme.py`'de tanımlı; hardcode hex YASAK)

| Token | Değer | Not |
|---|---|---|
| BG | `#14171a` | pencere zemini |
| SIDEBAR | `#181c20` | sol ray |
| SIDEBAR_HOVER | `#20252a` | hover |
| SIDEBAR_ACTIVE | `#23292f` | seçili öğe (sol accent bar ile) |
| CARD | `#1c2126` | kart yüzeyi |
| CARD_HOVER | `#22282e` | kart hover |
| INPUT | `#232a31` | girdi/selected yüzeyi |
| BORDER | `#2a3138` | 1px hat |
| TEXT | `#e9e6df` | sıcak kırık beyaz |
| TEXT_MUTED | `#a8a59c` | ≈6.6 kontrast ✓ |
| ACCENT | `#d6a13e` | pirinç — kontrast ≈7.6 ✓ |
| DANGER | `#c75450` | |
| SUCCESS | `#8ab06f` | |

Yarıçap: buton/input 6px, kart 10px. Boşluk 4/8 ölçeği. Type: 11 / 12.5 / 13 / 14 / 17 / 22, ağırlık 400/600/700.

## İkonografi

Emoji yok. `QIcon.fromTheme(...)` (Breeze temasında doğrulanmış adlar) — ad bulunamazsa ikonsuz metin yeterli.

## Yedek

Seçili öğe = `#23292f` zemin + sol 3px pirinç bar. Odak = 2px pirinç outline (focus-visible).
