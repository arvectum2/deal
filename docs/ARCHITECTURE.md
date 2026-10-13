# Архитектура

Отдельный модульный монолит DealForge. Data Platform владеет общим discovery, acquisition, extraction, evidence, indexing и connector SDK. Discount Parser остаётся самостоятельным продуктом; копировать код лишь после проверки прав, преимущественно переиспользовать контракты/адаптеры. DealForge владеет бизнес-правилами.

Предметные сущности: BuyerOrganization, ConsentGrant, DemandIntent, RequirementRevision, SourceArtifact, Supplier, RFQ, SupplierReply, ComparableOffer, Benchmark, DealRoom, BuyerDecision, SavingsLedger, FeeAgreement; позже DemandPool, PriceTier, RenewalWatch.

Поток: документ/потребность -> Data Platform -> подтверждённые требования -> рыночные альтернативы -> утверждённый покупателем RFQ -> предложения -> сравнительный Deal Room -> самостоятельный выбор покупателя -> контракт -> подтверждённая экономия -> вознаграждение.

Модули по мере реализации: intake, benchmark, sourcing, dealroom, savings, pools, renewals, api. Не создавать пустые микросервисы. SQLite допустим для локальных тестов; PostgreSQL для production по мере потребности.

Инварианты: никакой отправки поставщикам без явного согласия; никакого обещания экономии без сопоставимого baseline; provenance обязательна; данные компаний изолированы; не координировать цены конкурирующих поставщиков; защита персональных данных и SSRF; договор между покупателем и поставщиком напрямую; Demand Pool только после юридической экспертизы.
