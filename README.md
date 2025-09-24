phantom-supportbot/
├─ alembic/                # миграции базы данных
├─ phantom_supportbot/     # основной пакет бота
│  ├─ __init__.py
│  ├─ main.py              # точка входа (aiohttp + webhook)
│  ├─ core/                # ядро приложения
│  │  ├─ __init__.py
│  │  ├─ bot.py            # инициализация Bot и Dispatcher
│  │  ├─ config.py         # Pydantic settings
│  │  ├─ db.py             # SQLAlchemy engine, session
│  │  └─ logging.py        # настройка логирования
│  ├─ handlers/            # обработчики aiogram
│  │  ├─ __init__.py
│  │  ├─ users.py          # пользовательские команды
│  │  └─ admins.py         # админские команды и ответы
│  ├─ models/              # модели БД
│  │  ├─ __init__.py
│  │  ├─ user.py
│  │  └─ ticket.py
│  ├─ schemas/             # Pydantic-схемы
│  │  ├─ __init__.py
│  │  └─ ticket.py
│  ├─ services/            # бизнес-логика
│  │  ├─ __init__.py
│  │  ├─ crud.py           # CRUD-операции
│  │  └─ notifier.py       # фоновые задачи (напоминания)
│  └─ utils/               # вспомогательные утилиты
│     └─ __init__.py
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
└─ README.md
