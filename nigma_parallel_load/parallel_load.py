import pandas as pd
import polars as pl
from multiprocessing.pool import ThreadPool
from datetime import datetime, timedelta
import logging
from clickhouse_connect import get_client

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_date_range(start_date, end_date, freq='D'):
    # Преобразую строки в datetime, если это необходимо
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    if freq == 'D':
        return pd.date_range(start=start_date, end=end_date, freq='D')
    elif freq == 'W':
        return pd.date_range(start=start_date, end=end_date, freq='W-MON')
    elif freq == 'M':
        # Генерирую месяцы, начиная с первого числа
        dates = pd.date_range(start=start_date.replace(day=1), end=end_date, freq='MS')
        # Убираю последнюю дату, если она выходит за пределы end_date
        return dates[dates <= end_date]
    else:
        raise ValueError(f"Не поддерживаемая частота. Используйте 'D', 'W' or 'M'.")
def execute_query(args):
    date, sql_template, freq, db_params, output_path, *other_args = args  
    compression = other_args[0] if other_args else 'zstd'  # Установка значения по умолчанию
    client = get_client(**db_params)
    
    if freq == 'W':
        end_date = date + timedelta(days=6)
    elif freq == 'M':
        next_month = date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
    else:
        end_date = date
    
    sql = sql_template.format(date=date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
    try:
        df = pl.DataFrame(client.query_df(sql))
        logger.info(f"Processed data for {date.strftime('%Y-%m-%d')}, shape: {df.shape}")
        
        if output_path:  # Если указан путь, записываем в Parquet
            df.write_parquet(f"{output_path}/data_{date.strftime('%Y%m%d')}.parquet", compression= compression)
            logger.info(f"Saved data for {date.strftime('%Y-%m-%d')} to {output_path}/data_{date.strftime('%Y%m%d')}.parquet")
            return df  # Возвращаю True, если данные сохранены
        else:
            return df  # Возвращаю df, если путь не указан
    except Exception as e:
        logger.error(f"Error processing data for {date.strftime('%Y-%m-%d')}: {str(e)}")
        return None
    finally:
        client.close()  # Закрываю клиент после использования



def nigma_parallel_load(sql_template, start_date, end_date, num_threads=3, freq='D', db_params=None, output_path=None, compression='zstd'):
    if db_params is None:
        raise ValueError("Параметры подключения к базе данных не указаны.")
    
    dates = get_date_range(start_date, end_date, freq)
    start_time = datetime.now()

    with ThreadPool(num_threads) as pool:
        results = pool.map(execute_query, [(date, sql_template, freq, db_params, output_path, compression) for date in dates]) 
    
    end_time = datetime.now()

    # Фильтрую None результаты
    valid_results = [result for result in results if result is not None]
    if valid_results:
        logger.info(f'Total execution time: {end_time - start_time}')
        logger.info(f'Processed {len(valid_results)} days of data.')
        total_size_mb = sum(result.estimated_size() for result in valid_results) / (1024 * 1024)
        logger.info(f'Total size of the resulting DataFrame: {total_size_mb:.2f} MB')
    else:
        logger.warning('No data to load')
        return pl.DataFrame()