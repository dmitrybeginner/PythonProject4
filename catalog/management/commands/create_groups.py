from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Creates user groups and sets permissions'

    def handle(self, *args, **options):
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует.'))

        # Получаем content type для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        # Получаем права
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=product_content_type,
        )
        publish_perm, _ = Permission.objects.get_or_create(
            codename='can_publish_product',
            name='Может публиковать продукт',
            content_type=product_content_type,
        )
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type,
        )

        # Назначаем права группе
        moderator_group.permissions.add(unpublish_perm, publish_perm, delete_perm)
        self.stdout.write(self.style.SUCCESS('Права успешно назначены группе "Модератор продуктов".'))