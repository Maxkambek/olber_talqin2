from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status, authentication, permissions
from rest_framework.response import Response
from cargo.models import Cargo
from cargo.serializers import CargoCreateSerializer, CargoListSerializer, CargoSerializer, CargoAcceptSerializer
from user.models import User
from user.pagination import CustomPagination


class CargoCreateView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
    queryset = Cargo.objects.all()


class CargoListView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'cargo_type']
    pagination_class = CustomPagination
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        statusfilter = self.request.query_params.get('status', None)
        typefilter = self.request.query_params.get('cargo_type', None)
        serializer = self.get_serializer(queryset, many=True)
        count = Cargo.objects.count()
        if count > 0:

            p_min = self.request.GET.get('p_min')
            p_max = self.request.GET.get('p_max')
            d_min = self.request.GET.get('d_min')
            d_max = self.request.GET.get('d_max')
            w_min = self.request.GET.get('w_min')
            w_max = self.request.GET.get('w_max')

            if not p_min or p_min == '':
                p_min = 0
            if not p_max or p_max == '':
                p_max = Cargo.objects.all().order_by('-price').first().price
            if not d_min or d_min == '':
                d_min = 0
            if not d_max or d_max == '':
                d_max = Cargo.objects.all().order_by('-distance').first().distance
            if not w_min or w_min == '':
                w_min = 0
            if not w_max or w_max == '':
                w_max = Cargo.objects.all().order_by('-weight').first().weight

            if p_min or p_max or d_min or d_max or w_min or w_max:
                queryset = Cargo.objects.filter(price__range=(p_min, p_max), distance__range=(d_min, d_max), weight__range=(w_min, w_max),).order_by('-id')
            else:
                queryset = Cargo.objects.all().order_by('-id')

            if statusfilter is not None:
                queryset = Cargo.objects.filter(status=statusfilter)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response({
                'results': serializer.data,
            }, status=status.HTTP_200_OK)#.exclude(user=self.request.user)
        else:
            queryset = "Hozircha e'lonlar yo'q"
            return Response({queryset}, status=status.HTTP_204_NO_CONTENT)


class CargoDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class CargoUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class OfferView(generics.GenericAPIView):
    serializer_class = CargoSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, pk=None):
        cargo = Cargo.objects.get(id=pk)
        user = request.user

        if not cargo.offers.filter(id=user.id).exists():
            if len(user.works) < 3:

                cargo.offers.add(*[user,])
                cargo.save()
                return Response({
                    'msg': f"{cargo.title} uchun offer belgilandi."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': f"Siz maksimal 3 ta ish olishingiz mumkin"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'msg': "Offer yozilib bo'lingan"
            }, status=status.HTTP_423_LOCKED)


class CargoAcceptView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = CargoAcceptSerializer(data = request.data)
        user_id = request.user.id
        if serializer.is_valid():
            item_id = request.data.get("id")
            doer_id = request.data.get("doer")
            cargo = Cargo.objects.filter(id=item_id).first()
            if cargo.user_id == user_id:
                user = User.objects.get(id=doer_id)
                check = cargo.offers.filter(id=doer_id).first()
                if cargo.status != 'new':
                    return Response({
                        'msg': "Bu zakaz band qilingan"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not check:
                    return Response({
                        'msg': "Taklif bermagan odamlarni tanlab bo'lmaydi"
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    cargo.doer = user
                    cargo.status = 'selected'
                    if user.cargos:
                        user.cargos.append(item_id)
                    else:
                        user.cargos.insert(0, item_id)
                        print('none')
                    cargo.offers.clear()

                    user.save()
                    cargo.save()
                    return Response({
                        'msg': "Успешно",
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': "Пользователь не владелец"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseCargoView(generics.GenericAPIView):
    serializer_class = CargoSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk=None):
        cargo = Cargo.objects.get(id=pk)
        user = request.user
        if cargo.user_id == user.id:
            if cargo.doer:
                doer = cargo.doer
                print(doer.cargos)
                doer.workes.remove(cargo)
                doer.cargos.remove(str(pk))
                cargo.status = 'finished'
                cargo.save()
                doer.save()
                return Response({
                    'msg': "Груз закрыта",
                }, status=status.HTTP_200_OK)
            else:
                 cargo.status = 'finished'
                 return Response({
                'msg': "Груз закрыта",

            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': "Пользователь не владелец"
            }, status=status.HTTP_400_BAD_REQUEST)



