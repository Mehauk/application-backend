# Backend

### Prerequisites
install dependencies
```
pip install -r requirements.txt
```

## Architecture
### Folder Structure
```
.
├── apps
│   └── example
│       ├── models.py
│       └── routes.py
├── config
│   └── database.py
├── services
│   └── database.py
├── .env
├── .env.example
├── dependencies.py
└── main.py
```

## Database setup
First update `.env` to point to the correct database connection URL.
```
# .env
DATABASE_URL={connectionString}
```

Next Generate and run migrations
```
# cd root/of/backend
python scripts/migrate.py gen -m "{Message}"
python scripts/migrate.py run
# useful to alias as `migrate` gen/run
```
