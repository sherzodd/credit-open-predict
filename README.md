# credit-open-predict - 
  Это сервис который использует ML Model для предсказание открытие кредитного счета клиентом в данном банке. Модель создано с помощью библиотеки sklearn, 
  в основном с помощью KNeighborsClassifier. 
  Сервис написан на Python, FastAPI. Ещё использовал PostgreSQL и Sqlalchemy для 
  базы данных где сохраняются все данные. 
  Сервис выгружен на Heroku. 
  Точность модели: 79%
  
  В файле training_process.py можно посмотреть как была обучана модель.
  
  Сервис можно использовать с помощью HTTP Post request(в Postman).
  Нужно ввести данные как "row json" с определенными параметрами. 
  
  
  Параметры:
  Endpoint URL = https://credit-open-prediction.herokuapp.com/predict
  
  {
   "gender":"str",
   "age":"int",
   "marital_status":"str",
   "job_position":"str",
   "credit_sum":"float",
   "credit_month":"int",
   "tariff_id":"float",
   "score_shk":"float",
   "education":"str",
   "living_region":"str",
   "monthly_income":"float",
   "credit_count":"float",
   "overdue_credit_count":"float",
}
  
  ![alt text](https://github.com/sherzodd/credit-open-predict/blob/main/image1.png?raw=true)


  

Некоторые результаты:

![alt text](https://github.com/sherzodd/credit-open-predict/blob/main/image0.png?raw=true)


![alt text](https://github.com/sherzodd/credit-open-predict/blob/main/image.png?raw=true)
