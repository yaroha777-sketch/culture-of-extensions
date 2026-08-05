# CLAUDE.md — Culture of Extensions
*Инструкции для Claude и всех AI-агентов работающих с этим репозиторием*

---

## Проект

| Параметр | Значение |
|----------|----------|
| Сайт | https://www.cultureofextensions.com |
| GitHub | https://github.com/yaroha777-sketch/culture-of-extensions |
| Хостинг | Vercel (auto-deploy из main) |
| Владелец | Lana (мастер-стилист), VEGAS (tech/marketing) |

---

## Архитектура — КРИТИЧНО ПОНЯТЬ

### Два слоя в одном репо:

**Слой 1 — Главная страница (`index.html`)**
- Это **minified bundle** (React 19 + Framer Motion + Vite build)
- Размер: ~1.6MB, 105 строк (весь код в одной строке)
- **НЕЛЬЗЯ редактировать руками** — файл сгенерирован, правки затрутся
- Исходники (JSX компоненты) отсутствуют в репо
- `culture-of-extensions.html` — дубль index.html, УДАЛИТЬ

**Слой 2 — SEO-страницы (всё остальное)**
- Генерируются Python-скриптом `generate.py`
- Редактировать нужно **только `generate.py`**, не HTML-файлы напрямую
- После правки `generate.py` → запустить → закоммитить результат

### Схема деплоя:
```
Правки в generate.py → python generate.py → git commit → git push → Vercel auto-deploy
```

---

## Правила безопасности

### НЕЛЬЗЯ без явного разрешения VEGAS:
- Редактировать `index.html` напрямую (он сгенерирован)
- Делать `git push` в ветку `main`
- Запускать `npm install` или менять зависимости
- Удалять любые файлы (даже очевидные дубли)
- Деплоить на Vercel
- Коммитить `.env` файлы или секреты

### МОЖНО самостоятельно:
- Редактировать `generate.py` и показывать diff перед коммитом
- Создавать новые файлы и показывать их на проверку
- Читать все файлы репо
- Запускать `python generate.py` (только для проверки, не для коммита)

---

## Stack

| Компонент | Технология |
|-----------|-----------|
| Главная страница | React 19 + Framer Motion (minified bundle) |
| SEO страницы | Pure HTML (генерируется Python) |
| Генератор | `generate.py` (Python) |
| Хостинг | Vercel (Static) |
| Booking | Square Appointments |
| Шрифты | Google Fonts (Bodoni Moda, Syncopate, Inter) |
| Цвета | `--bg: #131210`, `--gold: #C9B896`, `--ink: #EDE8DC` |

---

## Константы проекта (из generate.py)

```python
DOMAIN = "https://www.cultureofextensions.com"
BOOK   = "https://app.squareup.com/appointments/book/oireayuannjp07/LQYSJW8GJE1Y6/start"
PHONE  = "(424) 428-9074"
ADDR   = "2119 N Glenoaks Blvd, Burbank, CA 91504"
EMAIL  = "cultureofextensions@gmail.com"
```

---

## Контекст бренда

- **Позиционирование:** Премиум К-Тип наращивание, Burbank/LA
- **Тон:** Роскошь, профессионализм, individuality
- **Цветовая схема:** Тёмный (почти чёрный) фон, золото, кремовый текст
- **Аудитория:** Русскоязычные + англоязычные женщины, LA, готовые платить за качество
- **Instagram:** @cultureofextensions_la

---

## Задачи в работе (статус)

- [ ] Удалить `culture-of-extensions.html` (дубль)
- [ ] Создать `.gitignore`
- [ ] Создать `AGENTS.md`
- [ ] Создать `README.md`
- [ ] Найти/восстановить исходники главной страницы
- [ ] Настроить ветку `develop` для безопасной разработки
- [ ] Подключить Square API key
- [ ] AI-агент для Instagram DM (RAG + ChromaDB + n8n)

---

## Координация агентов

Этот репо используется совместно: **Claude** (основной), **Codex**, **Gemini**.
Все агенты работают только через PR/ветки, не напрямую в `main`.
Подробности — в `AGENTS.md`.
