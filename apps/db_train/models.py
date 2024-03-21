from django.db import models

# Создайте свои модели здесь
class Author(models.Model):
    username = models.SlugField(verbose_name="Имя авторского аккаунта")
    email = models.EmailField(verbose_name="Email")
    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    middle_name = models.CharField(verbose_name="Отчество", max_length=100)
    gender = models.CharField(verbose_name="Пол", max_length=1, choices=[('м', 'мужской'), ('ж', 'женский')])
    self_esteem = models.DecimalField(verbose_name="Уровень самооценки", max_digits=2, decimal_places=1)
    phone_number = models.CharField(verbose_name="Телефон", max_length=12)
    city = models.CharField(verbose_name="Город", max_length=100)
    bio = models.TextField(verbose_name="Биография")
    age = models.IntegerField(verbose_name="Возраст", null=True, editable=False)
    date_birth = models.DateField(verbose_name="Дата рождения")
    status_rule = models.BooleanField(verbose_name="Согласие с правилами")
    image = models.ImageField(verbose_name="Фото профиля", upload_to='foto_profile')
    create_at = models.DateTimeField(verbose_name="Дата и время создания записи в БД", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Дата и время обновления записи в БД", auto_now=True)