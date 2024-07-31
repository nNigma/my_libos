from setuptools import setup, find_packages

setup(
    name="retention_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'polars',
        'clickhouse-connect',
    ],
    author="Ваше Имя",
    author_email="ваш.email@example.com",
    description="Пакет для параллельной загрузки данных из ClickHouse",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ваш_пользователь/retention_analysis",  # Укажите URL вашего репозитория
)