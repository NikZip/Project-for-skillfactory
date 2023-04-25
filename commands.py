from django.contrib.auth.models import User
from NewsPortal.models import Author, Category, Post, PostCategory, Comment

# Создать двух пользователей (с помощью метода User.objects.create_user('username')).
User.objects.create_user('best_user')
User.objects.create_user('worst_user')

# Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(user=User.objects.get(username='best_user'))
Author.objects.create(user=User.objects.get(username='worst_user'))

# Добавить 4 категории в модель Category.
Category.objects.create(name='tech')
Category.objects.create(name='stuff')
Category.objects.create(name='django')
Category.objects.create(name='skills')

# Добавить 2 статьи и 1 новость.
Post.objects.create(author=Author.objects.get(user__username='best_user'), post_type='article', title='best_post', text='Text1')
Post.objects.create(author=Author.objects.get(user__username='best_user'), post_type='article', title='best_post2', text='Text2')
Post.objects.create(author=Author.objects.get(user__username='worst_user'), post_type='news', title='worst_post', text='Text3')

# Присвоить им категории.
PostCategory.objects.create(post=Post.objects.get(title='best_post'), category=Category.objects.get(name='tech'))
PostCategory.objects.create(post=Post.objects.get(title='best_post'), category=Category.objects.get(name='stuff'))

PostCategory.objects.create(post=Post.objects.get(title='best_post2'), category=Category.objects.get(name='tech'))
PostCategory.objects.create(post=Post.objects.get(title='best_post2'), category=Category.objects.get(name='skills'))

PostCategory.objects.create(post=Post.objects.get(title='worst_post'), category=Category.objects.get(name='django'))
PostCategory.objects.create(post=Post.objects.get(title='worst_post'), category=Category.objects.get(name='skills'))

# Создать как минимум 4 комментария к разным объектам модели Post
for i in range(4):
    Comment.objects.create(post=Post.objects.get(title='best_post'), user=User.objects.get(username='best_user'),
                           text=f'Best Comment{i}')
    Comment.objects.create(post=Post.objects.get(title='best_post2'), user=User.objects.get(username='best_user'),
                           text=f'Best 2 Comment{i}')
    Comment.objects.create(post=Post.objects.get(title='worst_post'), user=User.objects.get(username='worst_user'),
                           text=f'Worst Comment{i}')


# Применяя функции like() и dislike() к статьям/новостям и комментариям
p1 = Post.objects.get(title='best_post')
p2 = Post.objects.get(title='best_post2')
p3 = Post.objects.get(title='worst_post')

c1 = Comment.objects.get(text=f'Best Comment0')
c2 = Comment.objects.get(text=f'Best 2 Comment1')
c3 = Comment.objects.get(text=f'Worst Comment1')

p1.like()
p2.like()
p3.dislike()

c1.like()
c2.like()
c3.dislike()

# Обновить рейтинги пользователей.
best = Author.objects.get(user=User.objects.get(username='best_user'))
worst = Author.objects.get(user=User.objects.get(username='worst_user'))

best.update_rating()
worst.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_user_check = Author.objects.all().order_by('-rating')[0]
print(best_user_check.user.username, best_user_check.rating)

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
# основываясь на лайках/дислайках к этой статье
best_post = Post.objects.all().order_by('-rating')[0]
print(best_post.creation_date, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(comment.creation_date, comment.user.username, comment.rating, comment.text)