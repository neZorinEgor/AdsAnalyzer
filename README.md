# TrainMe 📰

![FastAPI](https://img.shields.io/badge/fastapi-%2307405e.svg?style=for-the-badge&logo=fastapi&logoColor=E6882EE)
![Redis](https://img.shields.io/badge/redis-%2307405e.svg?style=for-the-badge&logo=redis&logoColor=E6882EE)
![Celery](https://img.shields.io/badge/celery-%2307405e.svg?style=for-the-badge&logo=celery&logoColor=A9CC54)
![MySQL](https://img.shields.io/badge/MySQL-%2307405e.svg?style=for-the-badge&logo=MySQL&logoColor=E6882EE)
![S3](https://img.shields.io/badge/s3-%2307405e.svg?style=for-the-badge&logo=amazonS3&logoColor=E6882EE)
![Docker](https://img.shields.io/badge/docker-%2307405e.svg?style=for-the-badge&logo=docker&logoColor=E6882EE)
![Sklearn](https://img.shields.io/badge/sklearn-%2307405e.svg?style=for-the-badge&logo=scikit-learn&logoColor=E6882EE)

No-Code платформа для продвинутого анализа рекламных кампаний 


### Генерация пары ключей RSA (приватного и публичного ключей)

```shell
# Сгенерировать приватный ключ RSA размером 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Извлечь публичный ключ из пары ключей, который может быть использован в сертификате
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
