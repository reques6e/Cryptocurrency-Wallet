import aiosqlite
import secrets
import uuid

from data._logger import logger
from typing import Union, Optional, Tuple
from config.environment import DB_DIR

class BadRequestDataBase(Exception):
    pass

class DataBase:
    def __init__(self, db_path = DB_DIR) -> None:
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_path)
        self.cursor = await self.connection.cursor()
        await logger('debug', 'База данных была подключена')

    async def close(self):
        await self.connection.close()

    async def create_tables(self) -> None:        
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


    async def create_user_account(
        self,
        user_id: Optional[int] = None,
        is_active: int = 1,
        is_verified: int = 0,
        is_ban: int = 0,
        is_banker: int = 0,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[int] = None,
        password: Optional[str] = None,
        api_key: str = None,  
        address: str = None,
        cash: Optional[int] = 0
    ) -> bool:
        
        """Создания пользователя в базе данных

        :param user_id: Уникальный аутентификатор 
        :param is_active: Статус аккаунта
        :param is_verified: Подтвержденный/Неподтвержденный
        :param is_ban: Заблокирован/Незаблокирован
        :param is_banker: Банкир/Обычный пользователь
        :param gender: Муж/Жен
        :param email: Контактная почта 
        :param phone: Контактный номер телефона 
        :param password: Пароль 

        :return: Ответ в виде bool"""

        try:
            await self.cursor.execute('''
                INSERT INTO users (user_id, is_active, is_verified, is_ban, is_banker, gender, email, phone, password, api_key, address, cash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (int(user_id), int(is_active), int(is_verified), int(is_ban), int(is_banker), str(gender), str(email), int(phone), str(password), str(api_key), str(address), float(cash)))
            await self.connection.commit()
        except:
            await logger('warning', f'В процессе создания пользователя "{user_id}" произошла ошибка')
            return False

        await logger('info', f'Создан новый пользователь "{user_id}"')
        return True
    
    async def user_exists(self, user_id: int) -> bool:

        """Проверка существования пользователя по user_id.

        :param user_id: Уникальный идентификатор пользователя
        
        :return: Ответ в виде bool """

        result = await self.cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
        return bool(await result.fetchone())
    
    async def is_active(self, user_id: int, value: Optional[bool] = True) -> bool:

        """Изменение статуса аккаунта

        :param user_id: Уникальный аутентификатор 
        :param is_active: Новый статус аккаунта

        :return: Ответ в виде bool """

        try:
            await self.cursor.execute('''
                    UPDATE users
                    SET is_active = ?
                    WHERE user_id = ?
                ''', (int(value), int(user_id),))
            
            await self.connection.commit()
        except:
            await logger('warning', f'В процессе изменения статуса (is_active) пользователя "{user_id}" произошла ошибка')
            return False
        
        await logger('info', f'Статус (is_active) пользователя "{user_id}", был изменён на "{value}"')
        return True
    
    async def is_verified(self, user_id: int, value: Optional[bool] = True) -> bool:

        """Изменение подтверждения аккаунта

        :param user_id: Уникальный аутентификатор 
        :param value: Новый статус подтверждения (1 = True, 0 = False)

        :return: Ответ в виде bool """

        try:
            await self.cursor.execute('''
                    UPDATE users
                    SET is_verified = ?
                    WHERE user_id = ?
                ''', (int(value), int(user_id),))
            
            await self.connection.commit()
        except:
            await logger('warning', f'В процессе изменения статуса (is_verified) пользователя "{user_id}" произошла ошибка')
            return False
        
        await logger('info', f'Статус (is_verified) пользователя "{user_id}", был изменён на "{value}"')
        return True
    
    async def is_ban(self, user_id: int, value: Optional[bool] = True) -> bool:

        """Изменение статуса блокировки аккаунта

        :param user_id: Уникальный аутентификатор 
        :param value: Новый статус подтверждения (1 = True, 0 = False)

        :return: Ответ в виде bool """

        try:
            await self.cursor.execute('''
                    UPDATE users
                    SET is_ban = ?
                    WHERE user_id = ?
                ''', (int(value), int(user_id),))
            
            await self.connection.commit()
        except:
            await logger('warning', f'В процессе изменения статуса (is_ban) пользователя "{user_id}" произошла ошибка')
            return False

        await logger('info', f'Статус (is_ban) пользователя "{user_id}", был изменён на "{value}"')
        return True

    async def is_banker(self, user_id: int, value: Optional[bool] = True) -> bool:

        """Изменение должности аккаунта

        :param user_id: Уникальный аутентификатор 
        :param value: Новый статус подтверждения (1 = True, 0 = False)

        :return: Ответ в виде bool """

        try:
            await self.cursor.execute('''
                    UPDATE users
                    SET is_banker = ?
                    WHERE user_id = ?
                ''', (int(value), int(user_id),))
            
            await self.connection.commit()
        except:
            await logger('warning', f'В процессе изменения статуса (is_ban) пользователя "{user_id}" произошла ошибка')
            return False

        await logger('info', f'Статус (is_ban) пользователя "{user_id}", был изменён на "{value}"')
        return True
    
    async def gender(self, user_id: int, gender: str) -> bool:

        """Изменение гендера аккаунта

        :param user_id: Уникальный аутентификатор 
        :param gender: Новый пол

        :return: Ответ в виде bool """

        if gender == 'Male' or 'Female':
            try:
                await self.cursor.execute('''
                    UPDATE users
                    SET gender = ?
                    WHERE user_id = ?
                ''', (gender, int(user_id),))

                await self.connection.commit()

                return True
            except:
                return False
        else:
            return False
    
    async def add_email(self, user_id: int, email: str) -> bool:

        """Изменение контактной почты аккаунта

        :param user_id: Уникальный аутентификатор 
        :param email: Новая почта 

        :return: Ответ в виде bool """

        try:
            await self.cursor.execute('''
                UPDATE users
                SET email = ?
                WHERE user_id = ?
            ''', (str(email), int(user_id),))

            await self.connection.commit()
        except:
            await logger('warning', f'В процессе изменения почты пользователя "{user_id}" произошла ошибка')
            return False
        
        await logger('info', f'Почта пользователа "{user_id}", была изменёна на "{email}"')
        return True
    
    async def add_phone(self, user_id: int, phone: int) -> bool:
        
        """Изменение контактного телефона аккаунта

        :param user_id: Уникальный аутентификатор 
        :param phone: Новый телефон 

        :return: Ответ в виде bool """

        try:
            await self.cursor.execute('''
                UPDATE users
                SET phone = ?
                WHERE user_id = ?
            ''', (int(phone), int(user_id),))

            await self.connection.commit()
        except:
            await logger('warning', f'В процессе изменения номера телефона пользователя "{user_id}" произошла ошибка')
            return False

        await logger('info', f'Номер телефона пользователа "{user_id}", была изменёна на "{phone}"')
        return True

    async def create_invoice(self,
        user_id: int, 
        amount: float, 
        currency: str, 
        created_at: int,
        commission: Optional[int] = 0, 
        callback_url: Optional[str] = '127.0.0.1'
    ) -> dict:
        
        """Создание счёта на оплату

        :param user_id: Уникальный аутентификатор пользователя
        :param amount: Сумма платежа
        :param currency: Валюта
        :param created_at: Дата создания платежа
        :param commission: Коммисия
        :param callback_url: Возврат данных на url

        :return: Ответ в виде dict """

        data = {
            'uuid': str(uuid.uuid4()),  
            'hash': secrets.token_urlsafe(24),
            'user_id': user_id,
            'url': 'https://example.com/invoices/',
            'amount': amount,
            'status': 'not_paid',
            'commission': commission,
            'currency': currency,
            'callback_url': callback_url,
            'created_at': created_at,
        }

        await self.cursor.execute('''
            INSERT INTO invoices (uuid, hash, user_id, url, amount, status, commission, currency, callback_url, created_at)
            VALUES (:uuid, :hash, :user_id, :url, :amount, :status, :commission, :currency, :callback_url, :created_at)
        ''', data)


        await self.connection.commit()
        
        return data

    async def invoice_info(self, param: str, value: str) -> dict:

        """Получение информации о счете по заданному параметру и его значению

        :param search_param: Параметр поиска (например, 'uuid', 'hash', и т.д.)
        :param search_value: Значение для поиска

        :return: Информация о счете в виде dict
        """

        valid_search_params = ['uuid', 'hash'] 

        if param not in valid_search_params:
            raise ValueError(f"Параметр не найден. Доступные параметры: {valid_search_params}")

        result = await self.cursor.execute(f'''
            SELECT uuid, hash, user_id, url, amount, status, commission, currency, callback_url, created_at
            FROM invoices WHERE {param} = ?
        ''', (value,))

        row = await result.fetchone()

        if row:
            invoice_info = {
                'state': 0,
                'result': {
                    'uuid': row[0],
                    'hash': row[1],
                    'user_id': row[2],
                    'url': row[3],
                    'amount': row[4],
                    'status': row[5],
                    'commission': row[6],
                    'currency': row[7],
                    'callback_url': row[8],
                }
            }

        else:
            invoice_info = {
                'state': 404,
                'result': {
                    'error': 'data_not_found'
                }
            }

        return invoice_info


    async def get_user_id_by_api_key(self, api_key: str) -> Optional[int]:
        if not self.cursor:
            await self.connect()

        result = await self.cursor.execute('SELECT user_id FROM users WHERE api_key = ?', (api_key,))
        row = await result.fetchone()

        if row and row[0]:
            return row[0]
        else:
            return None

    async def get_user_info(self, user_id: int) -> Optional[dict]:

        """Получение всей информации о пользователе по его user_id

        :param user_id: Уникальный аутентификатор пользователя

        :return: Информация о пользователе в виде dict
        """

        result = await self.cursor.execute('''
            SELECT user_id, is_active, is_verified, is_ban, is_banker, gender, email, phone, password, api_key, address, cash
            FROM users WHERE user_id = ?
        ''', (user_id,))

        row = await result.fetchone()

        if row:
            user_info = {
                'user_id': row[0],
                'is_active': bool(row[1]),
                'is_verified': bool(row[2]),
                'is_ban': bool(row[3]),
                'is_banker': bool(row[4]),
                'gender': row[5],
                'email': row[6],
                'phone': row[7],
                'password': row[8],  
                'api_key': row[9],
                'address': row[10],
                'cash': row[11]
            }
        else:
            user_info = None

        return user_info
    
    async def get_user_info_api_key(self, api_key: str) -> Optional[dict]:

        """Получение всей информации о пользователе по его api_key

        :param user_id: Уникальный аутентификатор пользователя

        :return: Информация о пользователе в виде dict
        """

        result = await self.cursor.execute('''
            SELECT user_id, is_active, is_verified, is_ban, is_banker, gender, email, phone, password, api_key, address
            FROM users WHERE api_key = ?
        ''', (api_key,))

        row = await result.fetchone()

        if row:
            user_info = {
                'user_id': row[0],
                'is_active': bool(row[1]),
                'is_verified': bool(row[2]),
                'is_ban': bool(row[3]),
                'is_banker': bool(row[4]),
                'gender': row[5],
                'email': row[6],
                'phone': row[7],
                'password': row[8],  
                'api_key': row[9],
                'address': row[10],
            }
        else:
            user_info = None

        return user_info

    async def delete_user(self, user_id: int) -> bool:

        """Удаление пользователя из базы данных по user_id

        :param user_id: Уникальный аутентификатор пользователя

        :return: Ответ в виде bool
        """

        try:
            await self.cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            await self.connection.commit()
            await logger('info', f'Пользователь с user_id {user_id} был удален')
            return True
        except:
            await logger('warning', f'В процессе удаления пользователя с user_id {user_id} произошла ошибка')
            return False

    async def get_user_by_id_and_password(
        self, user_id: int, password: str
    ) -> Optional[Union[str, Tuple]]:
        try:
            result = await self.cursor.execute(
                'SELECT * FROM users WHERE user_id = ? AND password = ?', (user_id, password)
            )
            user_data = await result.fetchone()

            if user_data:
                return user_data  # * Пользователь найден
            else:
                return None  # ! Пользователь не найден

        except Exception as e:
            print(f'Произошла ошибка при поиске пользователя: {e}')
            return 'Error'
        
    async def get_user_balance(self, user_id: int) -> float:
        """Получение баланса пользователя по его user_id

        :param user_id: Уникальный аутентификатор пользователя

        :return: Баланс пользователя в виде float (или 0, если баланс не определен или не является числом)
        """
        result = await self.cursor.execute('SELECT cash FROM users WHERE user_id = ?', (user_id,))
        row = await result.fetchone()

        if row and row[0]:
            try:
                return float(row[0])
            except ValueError:
                return 0.0
        else:
            return 0.0

    
    async def award_cash(self, user_id: int, amount: float) -> bool:

        """Зачисление средств на баланс пользователя по его user_id

        :param user_id: Уникальный аутентификатор пользователя
        :param amount: Сумма для зачисления

        :return: Ответ в виде bool
        """
        try:
            current_balance = await self.get_user_balance(user_id)
            
            if current_balance is not None:
                new_balance = current_balance + amount
            else:
                new_balance = 0 + amount
            
            await self.cursor.execute('''
                    UPDATE users
                    SET cash = ?
                    WHERE user_id = ?
                ''', (new_balance, user_id))

            await self.connection.commit()
            await logger('info', f'На баланс пользователя {user_id} зачислено {amount}')
            return True
        
        except Exception as e:
            print(f'Произошла ошибка при зачислении средств: {e}')
            await logger('warning', f'В процессе зачисления средств на баланс пользователя {user_id} произошла ошибка: {e}')
            return False



    async def unaward_cash(self, user_id: int, amount: float) -> bool:

        """Списание баланса пользователя по его user_id

        :param user_id: Уникальный аутентификатор пользователя
        :param amount: Сумма для списания

        :return: Ответ в виде bool
        """
        try:
            current_balance = await self.get_user_balance(user_id)
            new_balance = current_balance - amount

            await self.cursor.execute('''
                UPDATE users
                SET cash = ?
                WHERE user_id = ?
            ''', (new_balance, user_id))

            await self.connection.commit()
            await logger('info', f'Пользователь {user_id} списал с баланса {amount} валюты')
            return True
        except:
            await logger('warning', f'В процессе списания баланса пользователя {user_id} произошла ошибка')
            return False
        
    async def transfer_cash(
        self,
        user_id: int, 
        to_user_id: int, 
        amount: int, 
        comment: Optional[str] = ''
    ) -> dict[str, Union[str, int, bool]]:
        
        """Передача денег от клиента к клиенту"""
        
        if await self.get_user_info(user_id=user_id) is None or await self.get_user_info(user_id=to_user_id) is None:
            return {'success': False, 'message': 'Пользователь не найден.'}
        
        if await self.get_user_balance(user_id=user_id) >= amount:
            if await self.unaward_cash(user_id=user_id, amount=amount) and await self.award_cash(user_id=to_user_id, amount=amount):
                await logger('info', f'Пользователь {user_id} передал {amount} валюты пользователю {to_user_id}')
                return {'success': True, 'message': 'Перевод выполнен успешно.'}
        
        return {'success': False, 'message': 'Недостаточно средств для перевода.'}
    
    async def conclusion_cash(
            self,
            user_id: int,
            amount: int,
            atm: int
    ) -> dict[str, Union[str, int, bool]]:
        
        """Вывод денег из банкомата (ATM)"""

        if await self.get_user_balance(user_id=user_id) >= amount:
            if await self.unaward_cash(user_id=user_id, amount=amount) == True:
                await logger('info', f'Пользователь {user_id} вывел {amount} валюты из банкомата {atm}')
                return {'success': True, 'message': 'Успешный вывод средств'}
            else:
                await logger('error', f'Пользователь {user_id} не смг вывести {amount} валюты из банкомата {atm}, ошибка')
                return {'success': False, 'message': 'Вывод средств не удался'}
        else:
            await logger('info', f'Пользователь {user_id} не смг вывести {amount} валюты из банкомата {atm}, не достаточно средств')
            return {'success': False, 'message': 'Не достаточно средств'}
