# Culture of Extensions — Website

**cultureofextensions.com** — Premium hair extension salon in Burbank, CA

> Dark luxury aesthetic. K-Tip & micro-capsule extensions by Lana.

---

## Структура репозитория

```
/
├── index.html                    # Главная страница (React bundle, НЕ редактировать)
├── generate.py                   # Python генератор SEO-страниц ← редактировать здесь
├── sitemap.xml                   # Sitemap
├── robots.txt                    # Robots
├── vercel.json                   # Vercel config
├── icon.svg                      # Логотип
│
├── services/                     # Страницы услуг (авто-генерация)
│   ├── k-tip-extensions.html
│   ├── volume-density.html
│   ├── length-transformation.html
│   └── bio-tape-color.html
│
├── hair-extensions-*.html        # Городские SEO-страницы (авто-генерация)
│
└── photos/                       # Фотографии
    ├── g1.jpg — g7.jpg           # Галерея
    └── lana.jpg                  # Портрет
```

---

## Как обновить SEO-страницы

```bash
# 1. Редактируешь generate.py
# 2. Запускаешь генерацию
python generate.py

# 3. Проверяешь результат локально (открой любой .html файл)
# 4. Коммитишь
git add .
git commit -m "update: описание изменений"
git push
```

Vercel автоматически деплоит после push в `main`.

---

## Технический стек

| | |
|--|--|
| **Главная** | React 19 + Framer Motion (minified bundle) |
| **SEO-страницы** | Pure HTML (Python generator) |
| **Хостинг** | Vercel Static |
| **Booking** | Square Appointments |
| **Domain** | cultureofextensions.com |

---

## Контакты

- **Instagram:** [@cultureofextensions_la](https://www.instagram.com/cultureofextensions_la/)
- **Адрес:** 2119 N Glenoaks Blvd, Burbank, CA 91504
- **Телефон:** (424) 428-9074
- **Email:** cultureofextensions@gmail.com

---

## AI-агенты

Этот репо управляется с помощью AI-агентов.
Правила работы → см. `CLAUDE.md` и `AGENTS.md`
