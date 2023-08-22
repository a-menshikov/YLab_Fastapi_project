# YLab_Fastapi_project ДЗ №4

Проект выполнен в рамках интенсива от Y_Lab. Проходил в июле-августе 2023г. Состоял из 4-х заданий.

<details>
<summary>Задания:</summary>

1. Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. Даны 3 сущности: Меню, Подменю, Блюдо.

    Зависимости:
    - У меню есть подменю, которые к ней привязаны.
    - У подменю есть блюда.

    Условия:
    - Блюдо не может быть привязано напрямую к меню, минуя подменю.
    - Блюдо не может находиться в 2-х подменю одновременно.
    - Подменю не может находиться в 2-х меню одновременно.
    - Если удалить меню, должны удалиться все подменю и блюда этого меню.
    - Если удалить подменю, должны удалиться все блюда этого подменю.
    - Цены блюд выводить с округлением до 2 знаков после запятой.
    - Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
    - Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.

2. В этом домашнем задании необходимо:

    Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде “docker-compose up -d” или той которая описана вами в readme.md.

    Образы для Docker:
    - (API) python:3.10-slim
    - (DB) postgres:15.1-alpine

    - Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
    - Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в README.md

3. В этом домашнем задании необходимо:

    - Вынести бизнес логику и запросы в БД в отдельные слои приложения.
    - Добавить кэширование запросов к API  с использованием Redis. Не забыть про инвалидацию кэша.
    - Добавить pre-commit хуки в проект.
    - Покрыть проект type hints (тайпхинтами)
    - Описать ручки API в соответствий c OpenAPI
    - Реализовать в тестах аналог Django reverse() для FastAPI

    Дополнительно:

    - Контейнеры с проектом и с тестами запускаются разными командами.

4. В этом домашнем задании необходимо:

    - Переписать текущее FastAPI приложение на асинхронное выполнение
    - Добавить в проект фоновую задачу с помощью Celery + RabbitMQ.
    - Добавить эндпоинт (GET) для вывода всех меню со всеми связанными подменю и со всеми связанными блюдами.
    - Реализовать инвалидация кэша в background task (встроено в FastAPI)
    - Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx

    Фоновая задача:  
    Синхронизация Excel документа и БД. В проекте создаем папку admin. В эту папку кладем файл Menu.xlsx (будет прикреплен к ДЗ). При внесении изменений в файл все изменения должны отображаться в БД. Периодичность обновления 15 сек. Удалять БД при каждом обновлении – нельзя.

</details>

Я постарался максимально облегчить процесс запуска проекта, поэтому все необходимые .env файлы уже внутри репозитория для удобства, дополнительно ничего создавать не нужно. Для запуска потребуется docker compose.

## Запуск

### **Запуск проекта с полным функционалом**

1. Клонировать репозиторий

    ```bash
    git clone <ссылка с git-hub>
    ```

2. Перейти в папку /YLab_Fastapi_project

3. Требуется файл .env - пример в репозитории. Для пробного запуска можно использовать приложенный пример.

4. Поднять контейнеры в фоновом режиме

    ```bash
    docker compose up -d
    ```

5. Чтобы прекратить работу контейнеров воспользуйтесь командой

    ```bash
    docker compose down
    ```

    Если хотите прекратить работу контейнеров с удалением томов (рекомендуется), то дополните команду флагом -v

    ```bash
    docker compose down -v
    ```

6. Документация доступна по адресу <http://127.0.0.1:8000/docs>

### **Запуск проекта с прохождением тестов через pytest**

Для прогона написанных мной тестов подготовлен отдельный вариант файла docker compose.
Сценарий тестирования предполагает старт контейнеров, вывод результатов прохождения тестов на экран и удаление контейнеров вместе с томами.

Если проект был запущен локально раньше, то для стабильного запуска по данной инструкции необходимо остановить ранее запущенный сервис, удалить контейнеры, тома и образы, которые использовались для него.

Требуется файл .env_test - пример в репозитории. Для пробного запуска можно использовать приложенный пример. Переменная CELERY_STATUS должна быть в положении "false".

1. Для запуска сценария необходимо после клонирования репозитория выполнить в папке /YLab_Fastapi_project следующую команду

    ```bash
    docker compose -f docker-compose-pytest.yml up -d && docker logs --follow backend && docker compose -f docker-compose-pytest.yml down -v
    ```

### **Запуск проекта с прохождением тестов через Postman**

Для прогона тестов из самого первого задания подготовлен отдельный вариант файла docker compose.
Это то же самое приложение, но без контейнеров раббита и селери, так как с наполняемой из файла базой данных ожидаемых ответов постман уже не получает и возникают конфликты данных (сценарий постмана наполняет, селери удаляет, так как их нет в файле).

Если проект был запущен локально раньше, то для стабильного запуска по данной инструкции необходимо остановить ранее запущенный сервис, удалить контейнеры, тома и образы, которые использовались для него.

1. Для запуска сценария необходимо после клонирования репозитория выполнить в папке /YLab_Fastapi_project следующую команду

    ```bash
    docker compose -f docker-compose-postman.yml up -d
    ```

2. Чтобы завершить работу сервиса воспользуйтесь командой

    ```bash
    docker compose -f docker-compose-postman.yml down -v
    ```

## Комментарии к 4-му ДЗ

1. Celery-задача.

    - реализация находится в папке tasks/. Представлена двумя отдельными репозиториями парсера и обработчика. Оперирование данными производится с помощью эндпоинтов ранее написанного API.
    - в контейнере приложения файл с меню находится в папке /code/app/admin/
    - успешность использования автоматического наполнения базы из файла **сильно зависит от соблюдения правил форматирования таблицы.** Все поля для каждой сущности должны быть заполнены валидными данными. Если данные невалидны - каждую итерацию будут проходить неудачные запросы к API.
    - при добавлении строки с новой сущностью необходимо добавить также ее uuid в соответствующую ячейку. для генерации uuid-ов рекомендую использовать [этот ресурс](https://www.uuidgenerator.net/). Uuid должен быть уникальным.
    - поле цены требуется вводить в формате двух знаков после запятой.
    - при наличии большего времени, я бы уделил больше внимания обработке кейсов из серии "что может пойти не так" и убеждению заказчика, что ведение админки в экселе - ненадёжное решение - давайте лучше сделаем простенькую веб-версию сайта администратора. А пока надеемся, что наш пользователь молодец и не будет слишком сильно испытывать решение на прочность.

2. Фоновые задачи для кэша.

    - принял решение увести в фоновые задачи не только инвалидацию кэша, но и установку значений. Таким образом вся работа с кэшем проходит в фоне. Тесты проходят успешно, проблем с работой не наблюдается.

3. Новый эндпоинт.

    - полная информация по всем объектам базы в древовидной структуре доступна по новому эндпоинту  
    **{{LOCAL_URL}}/api/v1/fullbase**
    - тесты для нового эндпоинта находятся в файле tests/test_05_fullbase_endpiont.py

## Задачки со звездочкой

1. **Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest**

    Сценарий реализован в файле tests/test_04_counter.py

2. **Описать ручки API в соответствий c OpenAPI**

    В целом сваггер достаточно неплохо справляется с документированием, поэтому доделал не слишком много. Разбил ручки на теги и добавил описания, форматы ответов, статусы.

3. **Реализовать в тестах аналог Django reverse() для FastAPI**

    Реализация находится в файле tests/service.py  
    Функция так и названа reverse()  
    При первом обращении собираю для нее словарь значений из всех маршрутов зарегистрированных в приложении в формате ключ - имя функции привязанной к эндпоинту, значение - путь к этому эндпоинту. При использовании в тестах по названию фунцкции получаю путь и возвращаю форматированную переданными аргументами строку.

4. **Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx**

    Так как задание сделано уже после 13.00 понедельника (но до конца среды) - положил версию с ним в отдельную ветку sale. Чтобы проверить - нужно переключиться через git checkout. Файл xlsx также дополнен в той ветке скидками.  

    Детали реализации:  

    - скидка хранится в базе отдельным полем. Цена со скидкой считается на лету в валидаторе и отдается пользователю в ответе вместе с размером скидки. Цена без скидки не отдаётся нигде.
    - скидка может быть в диапазоне от 0 до 100. Вносится только целым числом.
    - в связи с этим обратная проверка сделана следующим образом - я применяю к цене из файла скидку и если результат сходится с ответом апи - считаю что цена не менялась
    - такая проверка может иметь погрешность - минимальное изменения цены в файле (например на 1 копейку) может не повлиять на цену со скидкой (так как у нас есть округление до 2 знаков), и чем выше скидка тем выше вероятность такого события. Поэтому алгоритм не поймет что в файле была изменена цена. Как только скидка пропадёт - все изменения в базе встанут верно. В текущей реализации - потерь денег не будет, так как по всем ручкам мы отдаем только цену со скидкой.
    - делать проверку с обращением в базу не считаю правильным - пока файл не меняется мы пользуемся кэшем (кэш я храню достаточно долго), а если проверять каждый раз в базе - гарантировано добавляем запросы в базу каждые 15 секунд. Учитывая что могут не сходиться копейки - считаю возможным принять эти риски в текущей реализации.

Это мой первый опыт работы с фреймворком FastAPI.  
Благодарю за возможность участвовать в интенсиве и учиться. Опыт за время написания проекта я получил колоссальный. Из всего стека до этого видел только алхимию.  
Готов ответить на любые вопросы по проекту и буду благодарен за обратную связь.  
Надеюсь на встречу на собеседовании))  

Мои контакты:  
telegram - @Menshikov_AS  
email - <a.menshikov1989@gmail.com>
