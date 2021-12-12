from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        #обновляет рейтинг пользователя, переданный в аргумент этого метода
        #состоит из рейтинг каждой статьи автора *3 + рейтинг все коммент
        #+ рейт коментов к статье автора
        a1 = 0
        for i in Post.objects.filter(author = self).values('rating'):
            a1 += i['rating'] * 3
        a2 = 0
        for i in Comment.objects.filter(user = self.user).values('rating'):
            a2 += i['rating']
        a3 = 0
        for i in Comment.objects.filter(post__author = self).values('rating'):
            a3 += i['rating']
        self.rating = a1 + a2 + a3
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length = 64, unique = True)

class Post(models.Model):

    NEWS = 'NEWS'
    ARTICLE = 'ART'
    TYPEOFPOST = [
        ('NEWS', 'News'),
        ('ART', 'Article'),
    ]
    author = models.ForeignKey('Author', on_delete = models.CASCADE)
    news_or_article = models.CharField(max_length =4, choices=TYPEOFPOST)
    time_in = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField('Category', through = 'PostCategory')
    heading = models.CharField(max_length = 64)
    text = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

class PostCategory(models.Model):
    post = models.ForeignKey('Post',on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
