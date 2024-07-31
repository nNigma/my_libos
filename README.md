# Nigma Parallel Load

## Описание
Nigma Parallel Load - это библиотека для параллельной загрузки данных из ClickHouse в формате Parquet с использованием Python. Она позволяет эффективно обрабатывать большие объемы данных, разбивая их на временные интервалы.

## Установка
Убедитесь, что у вас установлены необходимые библиотеки:

Installation
pip install pandas polars clickhouse-connect


### Функция `nigma_parallel_load`
Эта функция выполняет параллельную загрузку данных.

#### Параметры:
- `sql_template` (str): SQL-шаблон для запроса данных.
- `start_date` (str или datetime): Начальная дата для загрузки данных.
- `end_date` (str или datetime): Конечная дата для загрузки данных.
- `num_threads` (int, по умолчанию 3): Количество потоков для параллельной обработки.
- `freq` (str, по умолчанию 'D'): Частота загрузки данных ('D' - день, 'W' - неделя, 'M' - месяц).
- `db_params` (dict): Параметры подключения к базе данных.
- `output_path` (str, по умолчанию None): Путь для сохранения загруженных данных в формате Parquet.

#### Пример использования:

nigma_parallel_load(
sql_template="SELECT FROM my_table WHERE date BETWEEN '{date}' AND '{end_date}'",
start_date="2023-01-01",
end_date="2023-01-31",
num_threads=4,
freq='D',
db_params={"host": "localhost", "port": 9000, "user": "default", "password": "password"},
output_path="/path/to/save"
)

## Логирование
Библиотека использует модуль `logging` для вывода информации о процессе загрузки данных. Уровень логирования можно настроить в начале файла.

## Примечания
- Убедитесь, что у вас есть доступ к ClickHouse и правильные параметры подключения.
- Данные будут сохранены в формате Parquet с использованием сжатия Zstandard.

## Лицензия
Этот проект лицензирован под MIT License.
