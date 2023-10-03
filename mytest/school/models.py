from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Owner(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)


class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)


class ProductAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    video_link = models.CharField(max_length=200)
    vidio_duration = models.IntegerField()


class ProductLessons(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class LessonViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time_watched = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    viewing_time = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=ProductAccess)
def add_views(sender, instance, created, **kwargs):
    if created:
        lessons = ProductLessons.objects.filter(product__exact=instance.product_id)
        for lesson in lessons:
            LessonViews.objects.create(user_id=instance.user_id, product_id=instance.product_id,
                                       lesson_id=lesson.lesson_id)


@receiver(post_save, sender=LessonViews)
def update_view_status(sender, instance, created, **kwargs):
    if not created and not instance.status:
        vidio_duration = instance.lesson.vidio_duration
        time_watched = instance.time_watched
        if time_watched / vidio_duration >= .8:
            sender.objects.filter(id=instance.id).update(status=True)
