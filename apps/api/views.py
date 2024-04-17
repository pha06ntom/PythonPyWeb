from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt # чтобы post, put, patch, delete не требовали csrf токена (необязательно)
from apps.db_train_alternative.models import Author
from .serializers import AuthorModelSerializer
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from .serializers import AuthorSerializer

class AuthorAPIView(APIView):
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

class AuthorGenericAPIView(GenericAPIView, RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                           DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

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