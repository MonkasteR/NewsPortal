# NewsPortal

Учебный проект новостного портала на Django

команды для запуска с нуля, с тестовым контентом лежат в commands.py

**Проект содержит несколько специфических URL:**

* `/test/` - тестовая страницы показывающая разрешения текущего пользователя
* `/admin/` - админка для управления проектом
* `/news/ `- список новостей
* `/accounts/login/ `- адрес для логина пользователя
* `/subscriptions/` - управление подписками текущего пользователя

**Что можем на данный момент:**

* Отображаем список новостей и их краткое содержание
* Реализован поиск по новостям, категориям и датам публикации
* Создана постраничная навигация в списке новостей
* Сделана авторизация на сайте, как локальная так и через аккаунты соцсетей, например [Yandex](https://ya.ru/)
* В зависимости от прав пользователя возможно удаление, создание, редактирования новостей
* Контент для пользователя отображается в соответствии с его правами и допусками
* Возможна подписка на тематические категории новостей
* Создана еженедельная рассылка новостей пользователям по интересующих их темам
* Сделано кеширование главной страницы и новостей
* Добавлена команда `delnews` для удаления новостей в выбранной категории. Использовать `python manage.py delnews IT`
  чтобы удалить все новости в категории `IT`
* В админке изменены представления, добавлены фильтры и новые действия
* Добавлен выбор новостей по категориям в админке

**Нужное**
Перед тем как что-то удалять сначала делаем бекап базы:\
`python -Xutf8 manage.py dumpdata --format=xml --output mydata.xml`\
или:\
`python -Xutf8 manage.py dumpdata --format=json --output mydata.json`\
Если что-то сломалось после удаления, то восстанавливаем:\
`python manage.py loaddata mydata.xml`\
или:\
`python manage.py loaddata mydata.json`\
соответственно. Начальные бекапы положил в репозиторий на всякий случай.




