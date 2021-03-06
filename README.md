# Cервис подсчета MD5-хеш от файла, расположенного в сети Интернет

Сервис реализует API работающее по протоколу HTTP. 

Реализованы методы:
* POST /submit - по этому запросу происходит создание задачи на подсчет MD5-хеш суммы.
* GET /check - по этому запросу происходит получение статуса задачи.

### POST
Доступен по адресу */submit?url=<url файла>&email=<Email для результата>*

В параметре *<url файла>* содержится url файла, для которого необходимо подсчитать MD5-хеш сумму. В параметре *<Email для результата>* содержится адрес электронной почты, на которую нужно выслать письмо в случае, успешной выполненной задачи. Параметр *email* необязателен.

В случае успешного создания задачи, в ответ возвращается код ответа *201* и JSON-объект c идентификатор задачи вида:

```json
{
    "id": "24bb1139-d8f0-4c54-8141-137a552890b2"
}
```

В случае неудачи, возвращается код *422*.

### GET
Доступен по адресу */check?id=<id задачи>*

Где в *<id задачи>* содержится id задачи, статус которой необходимо получить. Все сгенерированные объекты сохраняются в БД, поэтому их можно получить в любое время.

В случае выполненой задачи, в ответ возвращается код ответа *200* и JSON-объект вида:

```json
{
    "md5": "6bb4590b9e635a083fe82516e6e4d910",
    "status": "done",
    "url": "http://example.com/file.txt"
}
```

который содержит в поле *md5* содержит MD5-хеш сумму файла доступного по адресу находящегося в поле *url*. В поле *status* содержится статус задачи (В данном случае значение *done*)

В случае если задача еще выполняется, в ответ возвращается код ответа *200* и JSON-объект:

```json
{
    "status": "running"
}
```

В случае если задача завершилась с ошибкой, в ответ возвращается код ответа *200* и JSON-объект:

```json
{
    "status": "error"
}
```

В случае если если задача с *<id задачи>* не существует,в ответ возвращается код ответа *404*.

## Запуск сервиса

#### Настройка почтового сервера
Настройки почтового сервера, находятся в файле /md5rest/md5rest/mail_settings.py

При неправильной настройке почтового сервера, сервис будет функционировать в обычном режиме, но без возможности отправки писем.

#### Сборка образа
Для сборки образа необходимо перейти в каталог с *Dockerfile* и выполнить команду:

##### docker build -t v1/django .

#### Запуск
Для сборки образа необходимо перейти в каталог с *Dockerfile* и выполнить команду:

###### docker run -p 8080:8080 v1/django

Сервис станет доступен на 8080 порту.
