# 🔐 Web Security Scanner

Web Security Scanner — это Django-приложение, позволяющее выполнять базовую проверку безопасности веб-сайтов на наличие SQL-инъекций. Использует пользовательские payload'ы, sqlmap API и формирует отчёты, включая экспорт в PDF.

---

## 🚀 Функции

- ✅ Добавление URL для анализа
- 🐍 Проверка на SQL-инъекции с кастомными payload'ами
- 🔄 Интеграция с sqlmap API
- 📄 Отчёты с оценкой уязвимостей и подробностями
- 🧪 Вывод SQL-инъекционных результатов с временем отклика
- 📥 Экспорт отчёта в PDF
- 📊 Прогресс-бар при запуске сканирования (визуальный)

---

## 📦 Установка

```bash
  git clone https://github.com/yourname/web-security-scanner.git
  cd web-security-scanner
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  pip install -r requirements.txt
```

## 📂 Структура проекта
```commandline
   scanner/
│
├── templates/
│   └── scanner/
│       ├── home.html
│       ├── report.html
│       ├── pdf_template.html
│
├── views.py          # Основная логика сканирования и генерации отчёта
├── models.py         # Модель целевого URL
├── sql_injection_checker.py  # Проверка URL на SQL-инъекции (payload-based)
├── utils/sqlmap_client.py    # API-интерфейс для sqlmap
```

## 📑 Примеры URL для тестирования
* http://testphp.vulnweb.com/listproducts.php?cat=1
* http://demo.testfire.net/search.jsp?query=bank
* http://www.webscantest.com/datastore/search_get.php?search=123
* http://php.testsparker.com/?id=1

## 📝 Пример Payload'ов
```commandline
   payloads = [
    "' OR 1=1 -- ",
    "' AND SLEEP(5) -- ",
    "' UNION SELECT NULL -- ",
    "'; DROP TABLE users --",
    ...
]
```



