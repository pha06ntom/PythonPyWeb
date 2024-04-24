from rest_framework.views import APIView
from rest_framework import status, filters, authentication
from django.views.decorators.csrf import csrf_exempt # чтобы post, put, patch, delete не требовали csrf токена (необязательно)
from apps.db_train_alternative.models import Author
from .serializers import AuthorModelSerializer
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from .serializers import AuthorSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                author = Author.objects.get(pk=pk)
                serializer = AuthorModelSerializer(author)
                return Response(serializer.data)
            except Author.DoesNotExist:
                return Response({'message': 'Автор не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            authors = Author.objects.all()
            serializer = AuthorModelSerializer(authors, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AuthorModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, requsest, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({'message': 'Автор не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorModelSerializer(author, data=requsest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({'message': 'Автор не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorModelSerializer(author, data=request.data, partical=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({'message': "Автор не найден"}, status=status.HTTP_404_NOT_FOUND)

        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomPermission(permissions.BasePermission):
    """
    Пользователи могут выполнять различные действия в зависимости от их роли.
    """

    def has_permission(self, request, view):
        # Разрешаем только GET запросы для неаутентифицированных пользователей
        if request.method == 'GET' and not request.user.is_authenticated:
            return True

        # Разрешаем GET и POST запросы для аутентифицированных пользователей
        if request.method in ['GET', 'POST'] and request.user.is_authenticated:
            return True

        # Разрешаем все дейтсвия для администраторов
        if request.user.is_superuser:
            return True

        # Во всех остальных случаях возвращаем False
        return False

class AuthorGenericAPIView(GenericAPIView, RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                           DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # Переопределяем атрибут permission_classes для указания нашего собственного разрешения
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request, *args, **kwargs):
        if kwargs.get(self.lookup_field):   # если бы передали id или pk
            try:
                # возвращаем 1 объект
                return self.retrieve(request, *args, **kwargs)
            except Http404:
                return Response({'message': 'Автор не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # иначе возврщаем список объектов
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AuthorPagination(PageNumberPagination):
    page_size = 5 # кол-во объектов на странице
    page_size_query_param = 'page_size' # параметр запроса для настройки кол-ва объектов на странице
    max_page_size = 1000 # максимальное кол-во объектов на странице

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = AuthorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'email'] # Указываем для каких полей можем проводить фильтрацию
    search_fields = ['email'] # Поля, по кот-ым будет выполняться поиск
    ordering_fields = ['name', 'email'] # Поля, по кот-ым можно сортировать

    # http_method_names = ['get', 'post'] ограничение поддерживаемых методов в представлении AuthorViewSet

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset
    @action(detail=True, methods=['post'])
    def my_action(self, request, pk=None):
        # Пользовательская логика здесь
        return Response({'message': f'Пользовательская функция для пользователя с pk={pk}'})
