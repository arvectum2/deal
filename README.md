# Arvectum DealForge

Платформа переговорной силы для малого бизнеса. Превращаем коммерческие потребности покупателей в сравнимые запросы поставщикам и проверяем реализованную экономию.

Три режима: Deal Challenge (сначала), Demand Pool (после проверки пилота), Renewal Autopilot (позже).

Зависимости: arvectum2/data-platform — универсальный сбор/извлечение/доказательства; arvectum2/discount-parser — избирательное переиспользование ценовых адаптеров и проверенной бизнес-логики после проверки прав. Deal хранит собственную доменную модель и не импортирует клиентское приложение целиком.

Документация: docs/ROADMAP.md, docs/ARCHITECTURE.md, docs/PRODUCT.md, docs/SYNC.md.

## Разработка и проверки (Mac mini)

Нужен Python 3.11+; на Mac mini используется Python 3.12 и uv.

~~~bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[dev]'
.venv/bin/ruff check src tests
.venv/bin/pytest -q
.venv/bin/dealforge health
.venv/bin/uvicorn dealforge.api.app:app --host 127.0.0.1 --port 8767
~~~

Команда `dealforge discover-url https://example.com` проверяет и регистрирует потенциальный публичный URL. Это **не проверка скидки и не отправка запроса поставщику**. Для всех внешних коммуникаций в S3 потребуется явное согласие покупателя.

Дополнительно:
- [S0: аудит SDK и лицензий](docs/S0_REUSE_AUDIT.md)
- [ADR-0001: границы и зависимости](docs/adr/0001-product-boundaries.md)

В S0 права на повторное использование кода клиентского заказа Kwork пока не подтверждены договором. В DealForge код Discount Parser не копировался.
