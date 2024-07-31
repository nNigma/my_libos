from setuptools import setup, find_packages

setup(
    name='my_libos',  # Название вашей библиотеки
    version='0.1.0',  # Версия вашей библиотеки
    packages=find_packages(),  # Автоматически находит пакеты
    install_requires=[  # Зависимости, если есть
        # 'numpy',  # Пример зависимости
    ],
    author='nigma',  # Ваше имя
    author_email='nigma.st@gmail.com',  # Ваш email
    description='Библиотека позволяет загружать данные из ClickHouse и сохранять их в Parquet',
    url='https://github.com/nNigma/my_libos',  # URL вашего репозитория
)