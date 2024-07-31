# Parallel load for ClickHouse

Краткое описание вашего пакета и его функциональности.

## Установка

bash
pip install git+https://github.com/ваш_пользователь/ваш_репозиторий.git

## Использование

python
from libos.parallel_load import parallel_load
db_params = {
'host': '...',
'port': 8123,
'username': 'login',
'password': 'password'
}
sql_template = """
SELECT \*
FROM your_table
WHERE toDate(date) BETWEEN '{date}' AND '{end_date}'
"""
result = parallel_load(sql_template, '2024-05-01', '2024-05-30', num_threads=3, freq='D', db_params=db_params)
