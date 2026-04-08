# Marketly Microservices Blueprint

Bu papka hozirgi `Marketly` saytiga qarab tayyorlangan microservices arxitektura skeleti.

Maqsad:
- mavjud saytni darrov ko'chirmasdan
- aynan hozirgi funksiyalarni servislar bo'yicha ajratib
- `Go`, `Java`, `C++`, `MySQL`, `Spanner`, `Bigtable`, `Google Cloud`, `Kubernetes`
  bilan production darajasidagi yo'nalishni tayyorlab qo'yish

## Hozirgi sayt modullari

Hozirgi Django loyihadagi asosiy modullar:
- foydalanuvchi kirishi va profil to'ldirish
- `Xaridor` va `Tadbirkor` rollari
- mahsulot qo'shish va feed
- admin panel
- xavfsizlik toggle
- AI solishtirish

## Taklif qilinayotgan servislar

1. `api-gateway-go`
   Veb va mobil klientlar uchun yagona kirish nuqtasi.

2. `identity-profile-java`
   Login, profil, rol, admin session, foydalanuvchi lifecycle.

3. `catalog-go`
   Mahsulotlar, kategoriyalar, feed, qidiruv, tadbirkor mahsulot qo'shishi.

4. `compare-ai-cpp`
   Mahsulotlarni solishtirish, scoring, tavsiya chiqarish.

## Ma'lumotlar bazasi bo'linishi

- `MySQL`
  User profile, admin credentials metadata, role mapping, basic product metadata.

- `Spanner`
  Distributed transaction talab qiladigan oqimlar:
  role transition, order/session state, multi-region critical state.

- `Bigtable`
  Compare logs, clickstream, feed behavior, product impression/event log, recommendation features.

## Infratuzilma

- `Google Cloud`
- `GKE / Kubernetes`
- `Cloud Load Balancer`
- `Artifact Registry`
- `Cloud Build`
- `Secret Manager`
- `Pub/Sub`

## Papka tuzilmasi

- `services/api-gateway-go`
- `services/identity-profile-java`
- `services/catalog-go`
- `services/compare-ai-cpp`
- `infra/kubernetes/base`
- `infra/gcp`
- `docs/system-design.md`

## Qanday ishlatiladi

Bu scaffold ishlab turadigan production sistemaning boshlang'ich karkasi hisoblanadi.
Undan keyingi qadam:

1. Django endpointlarni service-contract ga ko'chirish
2. Gateway route'larni real service URL ga ulash
3. MySQL / Spanner / Bigtable connectorlarni ulash
4. GKE ga deploy pipeline yaratish

