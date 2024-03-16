<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

Скрипт банковской системы.


### Запуск

<div class="block_code">

```console
Libary: https://github.com/tiangolo/fastapi

$ python3 main.py

INFO:     Started server process [x]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

<details markdown="1">
<summary>Дополнения к запуску <code>python3 main.py</code><summary>

Команда `python3 main.p` так же имеет дополнительные параметры к запуску скрипта:

* `example`: Пример ...
* ...
* ...

</details>

### Проверка скрипта

Откройте браузер и введите URL: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:{your_port}</a>.

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


## create_tables - Создание таблиц

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

<details markdown="1">
<summary>Дополнительно <code>Key</code>...</summary>

Уникальный ключ (без шифра) (дефолтный):

```
HelloWorld^&@#$*^*#@&$@!#
Reques6eProject
IsFreeGithubProject^_^
$@#&%*$(*&ASKDJHBckjkasd852654sd23543$#Q!@)
rEques&eP1jec%TF;
$sevenNineS86*&#^#@$)@!($&*@*(!#$&@#^%*$&*&#@$^#65&*(#%^@!*(#&*&@#%)@!(#asashbDH))
```

С шифром m256 (дефолтный):

```python
    unic = (
        'ef681700750ea986789b267d7789789190c32eeda4a855eeafad0f6de211b889',
        '08b612420238588d09c4eddaa6fba316ce438eb69fc89aa2f58b16d1bf4cef6b',
        '8714eebb95b72f21ae7cbbbfba30cccaade480592dbcb2626da39ad093871bd9',
        '3fba659cfe0bbfe38ea1047a5f4268393d36fee426b4ff863422db5b81788d6f',
        '96bafa906fff030fb9482b46a07638ab2c495e47deaa259e08cbb96c9f5d640d',
        '4d0004a2f0f20fde43fb12e029d893787523fa61ed349534aea272b427cc242d'
    )
```

</details>
