from rest_framework import serializers
from school.models import LessonViews, Product


class LessonViewsSerializer(serializers.ModelSerializer):
    date_last_viewing = serializers.SerializerMethodField()

    class Meta:
        model = LessonViews
        fields = ('user_id', 'product_id', 'lesson_id', 'time_watched', 'status', 'date_last_viewing')

    def get_date_last_viewing(self, obj):
        if obj.time_watched:
            return obj.viewing_time
        return 'не смотрел'


class ProductsSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    owner_id = serializers.IntegerField()
    number_lessons_viewed = serializers.IntegerField()
    amount_time = serializers.IntegerField()
    number_students = serializers.IntegerField()
    percentage_acquisition = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
        'product_id', 'owner_id', 'number_lessons_viewed', 'amount_time', 'number_students', 'percentage_acquisition')
