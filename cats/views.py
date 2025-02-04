from rest_framework import viewsets, permissions, throttling, pagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .pagination import CatsPagination
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHouseRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, OwnerOrReadOnly]
    # Подключили встроенный класс ограничителя AnonRateThrottle,
    # его лимит прописан в settings
    throttle_classes = (throttling.AnonRateThrottle,)
    # кастомный пагинатор. У остальных дефолтный из settings
    # временно отключен для настройки фильтрации
    pagination_class = CatsPagination
    # подключаем фильтрацию (по полям, поиск, сортировка)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('color', 'birth_year')
    search_fields = ('$name', 'achievements__name')  # по name можно regexp
    # сортировка
    ordering_fields = ('name',)  # поля, доступные для сортировки
    ordering = ('birth_year',)  # сортировка по умолчанию

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # один из вариантов доступа анонимов к информации о единичном объекте
    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень без изменений
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # а тут свой пагинатор с явным лимитом и офсетом
    pagination_class = pagination.LimitOffsetPagination


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    # Подключили кастомный класс ограничителя,
    # его лимит прописан в settings
    throttle_classes = (throttling.ScopedRateThrottle,
                        WorkingHouseRateThrottle
                        )
    throttle_scope = 'low_request'
