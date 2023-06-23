from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        # ordering = ["name"]
        verbose_name='Category'
        verbose_name_plural='Categories'

    def _str_(self):
        return self.name


class Post(models.Model):

    def get_queryset(self):
        return super().get_queryset().filter(status='publishded')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    category = models.ManyToManyField(Category, default=1)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(
        max_length=10, choices=options, default='published')

    objects = models.Manager()  # default manager

    class Meta:
        # ordering = ('-published')                        
        verbose_name='Post'
        verbose_name_plural='Posts'

    # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.title
