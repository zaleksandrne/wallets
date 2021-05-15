### Запуск проекта в Docker Compose
- Соберите и запустите контейнеры
```
docker-compose up -d --build
```
- Выполните миграции
```
docker-compose exec web python manage.py migrate --noinput
```
- Создайте суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```
- Соберите статические файлы
```
docker-compose exec web python manage.py collectstatic --no-input 
