```
./
├── database.py
│   ├── create_tables                             -> None
│   ├── create_user_account               [API]   -> bool
│   ├── user_exists                               -> bool
│   ├── is_active                                 -> bool
│   ├── is_verified                               -> bool
│   ├── is_ban                                    -> bool
│   ├── is_banker                                 -> bool
│   ├── gender                                    -> bool
│   ├── add_email                                 -> bool
│   ├── add_phone                         [HAPI]  -> bool
│   ├── create_invoice                    [API]   -> dict
│   ├── invoice_info                      [API]   -> dict
│   ├── get_user_id_by_api_key            [HAPI]  -> Optional[int]
│   ├── get_user_info                     [API]   -> Optional[dict]
│   ├── get_user_info_api_key                     -> Optional[dict]
│   ├── delete_user                       [API]   -> bool
│   ├── get_user_by_id_and_password       [HAPI]  -> Optional[Union[str, Tuple]]
│   ├── get_user_balance                          -> float
│   ├── award_cash                                -> bool
│   ├── unaward_cash                              -> bool
│   ├── transfer_cash                     [API]   -> dict[str, Union[str, int, bool]]
│   ├── conclusion_cash                   [API]   -> dict[str, Union[str, int, bool]]
│   ├── 
│   ├── 

```


create_tables - Создание таблиц

```python
    async def create_tables(self):        
        await self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                is_active INTEGER,
                is_verified INTEGER,
                is_ban INTEGER,
                is_banker INTEGER,
                gender TEXT,
                email TEXT,
                phone INT,
                password TEXT,
                api_key TEXT,
                address TEXT,
                cash REAL
            )
        ''')

        # await self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS bank_accounts (
        #         user_id INTEGER PRIMARY KEY,
        #         is_active INTEGER,
        #         is_ban INTEGER,
        #         cash REAL
        #     )
        # ''')

        await self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                uuid TEXT PRIMARY KEY,
                hash TEXT,
                user_id INTEGER,
                url TEXT,
                amount REAL,
                status TEXT,
                commission REAL,
                currency TEXT,
                callback_url TEXT,
                created_at INTEGER
            )
        ''')

        await self.connection.commit()
        if self.cursor.rowcount == 0:
            await logger('info', 'Таблицы в базе данных уже существуют')
        else:
            await logger('info', 'Таблицы в базе данных были созданы')
```
