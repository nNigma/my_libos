from libos.parallel_load import parallel_load
# Пример использования
db_params = {
        'host': '10.20.14.168',
        'port': 8123,
        'username': 'niskhakov',
        'password': 'superL!ft37'
    }
    
sql_template = """
WITH 
base AS (
		SELECT 
				toDate(ym_pv_dateTime) AS date,
				ym_pv_deviceCategory,
				ym_cd_cid
		FROM yandex_metrika.rutube_94863760_hits_visits
		WHERE toDate(ym_pv_dateTime) BETWEEN '{date}' AND '{end_date}'
		GROUP BY 
				date,
				ym_pv_deviceCategory,
				ym_cd_cid
)
SELECT *
FROM base
"""	

result = parallel_load(sql_template, '2024-05-01', '2024-05-30', num_threads=3, freq='D', db_params=db_params)