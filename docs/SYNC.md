# GitHub — GitVerse — Mac mini

Источник истины: github.com/arvectum2/deal, branch main.
GitVerse: gitverse.ru/arvectum/deal — однонаправленное зеркало всех веток/тегов. Не коммитить в GitVerse.
Mac mini: /Volumes/ArvectumSSD/Arvectum/repos/deal — канонический локальный checkout для разработки.

Порядок: разработка Mac mini -> push GitHub -> GitHub Actions push GitVerse. GitHub Actions требует секрет GITVERSE_TOKEN с правом записи в arvectum/deal. Динамическое имя GitVerse repo не нужно.

В workflow используется force/prune исключительно к зеркалу, поскольку истории двух независимо созданных начальных репозиториев не совпадали. Писать в GitVerse напрямую запрещено: это уничтожит независимые изменения.

На Mac mini сначала git pull --ff-only origin main, затем рабочая feature-ветка; завершение через PR/push GitHub. Для автоматического локального обновления: только чистое рабочее дерево, fast-forward-only; при грязном дереве автоматический pull пропустить.

Проверка: git rev-parse main и git ls-remote origin refs/heads/main и git ls-remote gitverse refs/heads/main должны совпадать после работы зеркала.
