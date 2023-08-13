# YLab_Fastapi_project ДЗ №3

Я постарался максимально облегчить процесс запуска проекта, поэтому все неободимые .env файлы уже внутри репозитория для удобства. Для запуска потребуется docker compose.

## Запуск

### Запуск проекта на локальном компьютере

1. Клонировать репозиторий

    ```bash
    git clone <ссылка с git-hub>
    ```

2. Перейти в папку /YLab_Fastapi_project

3. Поднять контейнеры в фоновом режиме

    ```bash
    docker compose up -d
    ```

4. Чтобы прекратить работу контейнеров воспользуётсь командой

    ```bash
    docker compose down
    ```

    Если хотите прекратить работу контейнеров с удалением томов, то дополните команду флагом -v

    ```bash
    docker compose down -v
    ```

5. Документация доступна по адресу <http://127.0.0.1:8000/docs>

### Запуск проекта с прохождением тестов через pytest

Для прогона написанных мной тестов подготовлен отдельный вариант файла docker compose.
Сценарий тестирования предполагает старт контейнеров, вывод результатов прохождения тестов на экран и удаление контейнеров вместе с томами.

Если проект был запущен локально раньше, то для стабильного запуска по данной инструкции необходимо остановить ранее запущенный сервис, удалить контейнеры, тома и образы, которые использовались для него.

1. Для запуска сценария необходимо после клонирования репозитория выполнить в папке /YLab_Fastapi_project следующую команду

    ```bash
    docker compose -f docker-compose-pytest.yml up -d && docker logs --follow backend && docker compose -f docker-compose-pytest.yml down -v
    ```

### Запуск проекта с прохождением тестов через Postman

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

Это мой первый опыт работы с фреймворком FastAPI.  
Готов ответить на любые вопросы по проекту и буду благодарен за обратную связь.

Мои контакты:  
telegram - @Menshikov_AS  
email - <a.menshikov1989@gmail.com>
