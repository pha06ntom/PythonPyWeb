import django
import os
from django.db.models import Count, Max

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train.models import Author, AuthorProfile, Entry, Tag



    count_articles_by_athors = Author.objects.annotate(count_e=Count('entries')).values('count_e')
    print(count_articles_by_athors[0])

    count_entry_user = Author.objects.annotate(count_entry=Count('entries')).order_by('-count_entry').values('username')[0]
    print(count_entry_user)
    # max_entry = count_entry_user.aggregate(max_entry=Max('count_entry'))['max_entry']
    # print(max_entry)
    # print(count_entry_user.filter(count_entry = max_entry).values('username'))
    # count_articles_by_athors = Author.objects.annotate(entry_count=Count('entries')).values('username', 'entry_count')
    # print(count_articles_by_athors)












