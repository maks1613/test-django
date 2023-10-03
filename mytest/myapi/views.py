from school.models import User, LessonViews, Product
from .serializers import LessonViewsSerializer, ProductsSerializer
from rest_framework.viewsets import ModelViewSet
from django.db.models import Sum, Count, F, ExpressionWrapper, fields
from django.db.models.functions import Coalesce, Round
from django_filters import rest_framework as filters


class UserLessonsFilterView(ModelViewSet):
    queryset = LessonViews.objects.all()
    serializer_class = LessonViewsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        'user_id',
        'product_id',
    ]


class ProductsFilterView(ModelViewSet):
    queryset = Product.objects.all().annotate(
        product_id=F('id'),
        number_lessons_viewed=Count('lessonviews', filter=F('lessonviews__status')),
        amount_time=Sum('lessonviews__time_watched'),
        number_students=Count('lessonviews__user_id', distinct=True),
        number_users=Coalesce(User.objects.count(), 1),
        percentage_acquisition=ExpressionWrapper(Round((F('number_students') * 100) / F('number_users')),
                                                 output_field=fields.IntegerField())
    ).values('product_id', 'owner_id', 'number_lessons_viewed', 'amount_time', 'number_students',
             'percentage_acquisition')
    serializer_class = ProductsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        'id',
        'owner_id'
    ]
