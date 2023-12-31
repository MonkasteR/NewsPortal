from django.core.management.base import BaseCommand

from News.models import Category, Post
from NewsPortal.settings import logger


class Command(BaseCommand):
    help = "Удаление статей в определенной категории"

    def add_arguments(self, parser):
        """
        Добавляет указанные аргументы командной строки в объект парсера.

        Параметры:
        - `parser`: Объект парсера, в который добавляются аргументы.

        Возвращаемое значение:
        Нет
        """
        parser.add_argument("category", type=str)

    def handle(self, *args, **options):
        """
        Обрабатывает удаление всех статей в указанной категории.

        Параметры:
        - `args`: Список аргументов переменной длины.
        - `options`: Произвольные именованные аргументы.

        Возвращаемое значение:
        Нет
        """
        category_name = options.get("category")

        if category_name:
            answer = input(
                f"Вы правда хотите удалить все статьи в категории {category_name}? (yes/no): "
            )

            if answer.lower() == "yes":
                try:
                    category = Category.objects.get(name=category_name)
                    Post.objects.filter(postCategory=category).delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Все статьи в категории {category_name} удалены"
                        )
                    )
                    logger.warning(f"Все статьи в категории {category_name} удалены")
                except Category.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"Не найдено категории {category_name}")
                    )
                    logger.error(f"Не найдено категории {category_name}")
            else:
                self.stdout.write(self.style.ERROR("Отменено"))
                logger.error("Отменено")
        else:
            self.stdout.write(self.style.ERROR("Не указана категория"))
            logger.error("Не указана категория")
