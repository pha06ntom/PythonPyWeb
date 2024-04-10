from django.shortcuts import render
from django.views import View
from .models import Author, Entry, AuthorProfile, Tag
from django.db.models import Q, Max, Min, Avg, Count



class TrainView(View):
    def get(self, request):
        # Запросы к БД

        # Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])

        # Какой автор имеет наибольшее количество опубликованных статей?
        count_entry_user = Author.objects.annotate(count_entry=Count('entries')).order_by('-count_entry').values('username')
        self.answer2 = Author.objects.filter(username=count_entry_user[0]['username'])

        #Какие статьи содержат тег 'Кино' или 'Музыка'?
        self.answer3 = Entry.objects.filter(tags__name__in=['Кино','Музыка']).distinct()

        # Сколько авторов женского пола зарегистрировано в системе?
        self.answer4 = Author.objects.filter(gender='ж').count()

        # Какой процент авторов согласился с правилами при регистрации?
        count_true = Author.objects.filter(status_rule=True).count()
        count_all = Author.objects.count()
        self.answer5 = round((count_true / count_all) * 100, 1)

        # Какие авторы имеют стаж от 1 до 5 лет?
        self.answer6 = Author.objects.filter(authorprofile__stage__range=(1,5))

        # Какой автор имеет наибольший возраст?
        max_age_user = Author.objects.aggregate(max_age=Max('age'))
        self.answer7 = max_age_user.get('max_age')

        # Сколько авторов указали свой номер телефона?
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()

        # Какие авторы имеют возраст младше 25 лет?
        self.answer9 = Author.objects.filter(age__lt=25)

        # Сколько статей написано каждым автором?
        count_articles_by_athors = Author.objects.annotate(count=Count('entries')).values('username', 'count')
        self.answer10 = count_articles_by_athors


        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1,11)}
        return render(request, 'train_db/training_db.html', context=context)

