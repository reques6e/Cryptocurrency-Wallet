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


### Функции в базе данных и как они работают

<details markdown="1">
<summary>Как этим пользовать? Разработчик идио...</summary>

* `[API]`: Функция используется напрямую в API системе 
* `[HAPI]`: Вспомогательная функция используется при обработке запроса (бекенд) в API
* `[EDIT]`: Функция которая редактирует параметры ранее записанные в базе данных
* `[ADD]`: Добавление дополнительных параметров, так же могут использоваться как параметр EDIT
* `[SYS]`: <span style="color:red">Функция, которая используется внутри других функций (Изменение аннотации и ответа функции могут вызывать ошибки в работе скрипта)</span>
* `->`: Формат результата, который возвращается после вызова функции (аннотация функции Python)
</details>

```
./
├── database.py
│   ├── create_tables                                             -> None
│   ├── create_user_account               [API]                   -> bool
│   ├── user_exists                       [SYS]                   -> bool
│   ├── is_active                         [EDIT]                  -> bool
│   ├── is_verified                       [EDIT]                  -> bool
│   ├── is_ban                            [EDIT]                  -> bool
│   ├── is_banker                         [EDIT]                  -> bool
│   ├── gender                            [EDIT]                  -> bool
│   ├── add_email                         [ADD]                   -> bool
│   ├── add_phone                         [ADD]                   -> bool
│   ├── create_invoice                    [API]                   -> dict
│   ├── invoice_info                      [API]                   -> dict
│   ├── get_user_id_by_api_key            [HAPI]                  -> Optional[int]
│   ├── get_user_info                     [API]                   -> Optional[dict]
│   ├── get_user_info_api_key                                     -> Optional[dict]
│   ├── delete_user                       [API]                   -> bool
│   ├── get_user_by_id_and_password       [HAPI]                  -> Optional[Union[str, Tuple]]
│   ├── get_user_balance                                          -> float
│   ├── award_cash                                                -> bool
│   ├── unaward_cash                                              -> bool
│   ├── transfer_cash                     [API]                   -> dict[str, Union[str, int, bool]]
│   ├── conclusion_cash                   [API]                   -> dict[str, Union[str, int, bool]]
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
