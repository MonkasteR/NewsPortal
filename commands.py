from News.models import *

user1 = User.objects.create_user('Петр')  # Создаем
user2 = User.objects.create_user('Иван')  # трех
user3 = User.objects.create_user('Сергей')  # пользователей
Author1 = Author.objects.create(authorUser=user1)  # Сразу делаем двух
Author2 = Author.objects.create(authorUser=user2)  # пользователей авторами
Category.objects.create(name='Space')  # Создаем
Category.objects.create(name='IT')  # категории
Category.objects.create(name='Sport')  # для
Category.objects.create(name='Policy')  # новостей
Post.objects.create(author_id=1, title='Заголовок новости 1', text='Текст новости 1, про непонятно что', categoryType='AR')
Post.objects.create(author_id=2, title='Заголовок новости 2', text='Текст новости 2, про IT', categoryType='AR')
Post.objects.create(author_id=2, title='Заголовок новости 3', text='Текст новости 3, про Sport', categoryType='NW')
Post.objects.create(author_id=1, title='Заголовок новости 4', text='Текст новости 4, Футбол ', categoryType='NW')
Post.objects.create(author_id=1, title='Заголовок новости 5', text='Текст новости 5, Космос. Найдена Raxxla ', categoryType='NW')
Post.objects.create(author_id=1, title='Заголовок новости 6', text='Текст новости 6, Космос. Таргоиды атакуют мирное население ', categoryType='AR')
post1 = Post.objects.get(pk=1)
post2 = Post.objects.get(pk=2)
post3 = Post.objects.get(pk=3)
post4 = Post.objects.get(pk=4)
post5 = Post.objects.get(pk=5)
post6 = Post.objects.get(pk=6)
category1 = Category.objects.get(name='Sport')
category2 = Category.objects.get(name='Space')
category3 = Category.objects.get(name='IT')
post1.postCategory.add(category1, category2, category3)  # Добавляем категории постам
post2.postCategory.add(category2)
post3.postCategory.add(category3)
post4.postCategory.add(category3, category2, category1)
post5.postCategory.add(category1)
post5.postCategory.add(category1)
Comment.objects.create(commentUser=user3, commentPost=post1, text='Знатная скотина, мех, шкварки, удовольствие')
Comment.objects.create(commentUser=user2, commentPost=post1, text='А о чем эта новость?')
Comment.objects.create(commentUser=user1, commentPost=post1, text='Новость не читал, но осуждаю')
Comment.objects.create(commentUser=user1, commentPost=post5, text='Неужели её нашли?')
Comment.objects.create(commentUser=user2, commentPost=post5, text='Пора отправлять на Ганимед за фейковые новости')
Comment.objects.create(commentUser=user3, commentPost=post6, text='А вы с ними еще в футбол играть хотели')
Comment.objects.create(commentUser=user1, commentPost=post6, text='Все не так однозначно, они просто так видят мир')
Comment.objects.create(commentUser=user2, commentPost=post2, text='Невидимые технологии на страже кавалерии')
Comment.objects.create(commentUser=user3, commentPost=post2, text='Лошадь не прошла через пакетный фильтр благодаря СОРМ')
Comment.objects.create(commentUser=user1, commentPost=post3, text='Спортивные ребята как всегда обыграли неспортивных ребят')
Comment.objects.create(commentUser=user2, commentPost=post3, text='ЗОЖ обман и провокация, занимайтесь НВП и будете здоровы')
Comment.objects.create(commentUser=user2, commentPost=post4, text='Штанга обыграла вратаря')
Comment.objects.create(commentUser=user3, commentPost=post4, text='На юге Москвы сгорел склад с огнетушителями')
comm1 = Comment.objects.get(pk=1)
comm2 = Comment.objects.get(pk=2)
comm3 = Comment.objects.get(pk=3)
comm4 = Comment.objects.get(pk=4)
comm5 = Comment.objects.get(pk=5)
comm6 = Comment.objects.get(pk=6)
comm7 = Comment.objects.get(pk=7)
comm8 = Comment.objects.get(pk=8)
comm9 = Comment.objects.get(pk=9)
comm10 = Comment.objects.get(pk=10)
comm11 = Comment.objects.get(pk=11)

post1.like()  # Накидать по вкусу в любые посты
post2.dislike()
comm1.like() # Накидать по вкусу в любые комменты
comm1.dislike()

Comment.objects.get(commentUser=3, commentPost=1).like()
Author1.update_rating()  # Если шелл не перегружали к этому моменту
Author2.update_rating()  # то можно таким образом обновить рейтинг у авторов
Author.objects.get(authorUser_id=1).update_rating()  # Если шелл перезапускали то
Author.objects.get(authorUser_id=2).update_rating()  # можно обновить рейтинг у авторов таким образом
Author.objects.get(
    authorUser=User.objects.get(username='Петр')).update_rating()  # Если мы хотим обновить рейтинг у Петра
a1 = Author.objects.get(authorUser_id=1)  # Если перезагружали шелл
a2 = Author.objects.get(authorUser_id=2)  # то можно присвоить переменные авторам
a1.update_rating()  # обновить их
a2.update_rating()  # рейтинги
a1.ratingAuthor  # И показать рейтинг
a2.ratingAuthor  # каждого автора

print(Author.objects.all().order_by('-ratingAuthor').values('authorUser__username', 'ratingAuthor')[
          0])  # Лучший автор и его рейтинг
print(Author.objects.all().order_by('-ratingAuthor').values('authorUser__username')[0][
          'authorUser__username'])  # Лучший автор имя
print(Post.objects.all().order_by('-rating').values('author__authorUser__username', 'rating')[0])  # Лучший пост
print(
    Post.objects.all().order_by('-rating').values('dateCreation', 'author__authorUser__username', 'rating', 'title')[0],
    Post.objects.all().order_by('-rating')[
        0].preview())  # Дата добавления, юзернейм,рейтинг, заголовок, превью лучшей статьи
print(Comment.objects.filter(
    commentPost__author__authorUser_id=Post.objects.all().order_by('-rating').values('author__authorUser_id').first()[
        'author__authorUser_id']).values('text'))  # Все комментарии к лучшей статье
print(Comment.objects.filter(
    commentPost__author__authorUser_id=Post.objects.all().order_by('-rating').values('author__authorUser_id').first()[
        'author__authorUser_id']).values('dateCreation', 'commentUser__username', 'rating',
                                         'text'))  # Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье. Что бы не значила эта формулировка
