from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField('Author rating', default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        if post_rating.get('postRating') is None:
            p_rating = 0
        else:
            p_rating = 0
            p_rating += post_rating.get('postRating')

        comment_rating = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        if comment_rating.get('commentRating') is None:
            c_rating = 0
        else:
            c_rating = 0
            c_rating += comment_rating.get('commentRating')

        comment_post_rating = 0
        for post in self.post_set.all():
            x = post.comment_set.aggregate(Sum('rating'))
            if x.get('rating__sum') is not None:
                print(x.get('rating__sum'))
                comment_post_rating += x.get('rating__sum')

        self.rating = p_rating * 3 + c_rating + comment_post_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField('Category name', max_length=16, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    ARTICLE = 'AR'
    NEWS = 'NW'
    PUBLICATION_TYPE = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )
    # publication_type = models.CharField(max_length=2, choices=PUBLICATION_TYPE, default=ARTICLE)
    publication_type = models.CharField(max_length=2, choices=PUBLICATION_TYPE)
    post_title = models.CharField('Post name', max_length=256)
    time_in = models.DateTimeField('Post date', auto_now_add=True)
    category = models.ManyToManyField("Category", through='PostCategory')
    post_text = models.TextField('Post text')
    rating = models.SmallIntegerField('Post rating', default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def preview(self):
        preview = self.post_text[:20] + '...'
        return preview

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def norm_date(self):
        return self.time_in.strftime('%d.%m.%Y')

    def __str__(self):
        return f'{self.post_title} : {self.post_text[0:20]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField('Comment text', max_length=512)
    time_in = models.DateTimeField('Post date', auto_now_add=True)
    rating = models.SmallIntegerField('Comment rating', default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_text}'
