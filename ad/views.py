from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ad.models import Ad, Review
from ad.paginations import AdsPaginator
from ad.permissions import IsOwner, IsAdminUser
from ad.serializers import AdSerializer, ReviewSerializer, ReviewCreateSerializer


class AdsCreateAPIView(generics.CreateAPIView):
    """ Создание объявления """

    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdsRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр информации об одном объявлении """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class AdsUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование объявления """

    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsOwner, IsAdminUser]

    def perform_update(self, serializer):
        ad = serializer.save()
        ad.save()


class AdsDestroyAPIView(generics.DestroyAPIView):
    """ Удаление объявления """

    queryset = Ad.objects.all()
    permission_classes = [IsOwner, IsAdminUser]

    def perform_destroy(self, instance):
        instance.delete()


class AdsListAPIView(generics.ListAPIView):
    """ Вывод списка всех объявлений """

    serializer_class = AdSerializer
    pagination_class = AdsPaginator
    queryset = Ad.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    permission_classes = [AllowAny]


class ReviewCreateAPIView(generics.CreateAPIView):
    """ Создание отзыва """

    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ad_id=self.kwargs['ad_id'])


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование отзыва """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsOwner, IsAdminUser]

    def put(self, request, *args, **kwargs):
        ad_id = self.kwargs['ad_id']
        review_id = self.kwargs['pk']

        review = get_object_or_404(Review, pk=review_id)

        if review.ad.id != ad_id:
            return Response("Невозможно обновить отзыв из-за некорректного запроса", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """ Удаление отзыва """

    queryset = Review.objects.all()
    permission_classes = [IsOwner, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        ad_id = self.kwargs['ad_id']
        review_id = self.kwargs['pk']

        review = get_object_or_404(Review, pk=review_id)

        if review.ad.id != ad_id:
            return Response("Невозможно удалить отзыв из-за некорректного запроса", status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(review)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAPIView(generics.ListAPIView):
    """ Вывод списка всех отзывов """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [AllowAny]
