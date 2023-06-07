from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Basket, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Subscribe, User

from .pagination import CustomPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, RecipeSerializer,
                          SetPasswordSerializer, SubscribeAuthorSerializer,
                          SubscriptionsSerializer, TagSerializer,
                          UserGetSerializer, UserPostSerializer)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserGetSerializer
        return UserPostSerializer

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserGetSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'Вы изменили пароль.'})

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            pagination_class=CustomPaginator)
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(page, many=True,
                                             context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        following = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = SubscribeAuthorSerializer(
                following, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=request.user, following=following)
            # return Response({'detail': 'Тест все ок'})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Subscribe, user=request.user,
                              following=following).delete()
            return Response({'detail': 'Вы отписались от пользователя'},
                            status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    search_fields = ('name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    search_fields = ('name',)
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        """Переопределение сохранения объекта"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = RecipeSerializer(recipe, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not Favorite.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Рецепт был ранее добавлен.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(Favorite, user=request.user,
                              recipe=recipe).delete()
            return Response({'detail': 'Рецепт  удален из списка избранного.'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None
            )
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = RecipeSerializer(recipe, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not Basket.objects.filter(user=request.user,
                                         recipe=recipe).exists():
                Basket.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(
                {'errors': 'Рецепт был ранее добавлен  в корзину.'},
                status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(Basket, user=request.user,
                              recipe=recipe).delete()
            return Response(
                {'detail': 'Рецепт удален из корзины.'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            IngredientRecipe.objects
            .filter(recipe__bascets__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit'))
        shopping_list = []
        for ingredient in ingredients:
            shopping_list.append(
                f"{ingredient[0]}: {ingredient[1]} {ingredient[2]}.")
        response = HttpResponse(
            'Cписок покупок:\n' +
            '\n'.join(map(str, shopping_list)),
            content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    search_fields = ('name',)
    pagination_class = None