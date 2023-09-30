from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Owner(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)


class Product(models.Model):
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)


class ProductAccess(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    video_link = models.CharField(max_length=200)
    vidio_duration = models.IntegerField()


class ProductLessons(models.Model):
    product_id = models.ManyToManyField(Product)
    lesson_id = models.ManyToManyField(Lesson)


class LessonViews(models.Model):
    lesson_id = models.ManyToManyField(Lesson)
    user_id = models.ManyToManyField(User)
    time_watched = models.IntegerField()
    status = models.BooleanField(default=False)
    viewing_time = models.DateTimeField()


@receiver(post_save, sender=LessonViews)
def update_view_status(instance):
    lesson_data = Lesson.objects.filter(lessonviews__id=instance.id)
    if lesson_data:
        vidio_duration = lesson_data[0].vidio_duration
        if instance.time_watched / vidio_duration >= .8:
            LessonViews.objects.filter(id=instance.id).update(status=True)

