# Infrastructure Overview

Bu papkadagi fayllar `Marketly` saytini quyidagi modelga tayyorlaydi:

- Google Cloud deploy
- Kubernetes orchestration
- multi-service runtime
- DB split: MySQL / Spanner / Bigtable

`base/` ichidagi manifestlar production-ready emas, lekin real GKE loyiha uchun yaxshi starting point.
