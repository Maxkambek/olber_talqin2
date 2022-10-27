from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status, authentication, permissions
from rest_framework.response import Response
from user.models import User
from user.pagination import CustomPagination
from work.models import Work
from work.serializers import WorkListSerializer, WorkSerializer, WorkDetailSerializer, WorkAcceptSerializer


class WorkListView(generics.ListAPIView):
    serializer_class = WorkListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    pagination_class = CustomPagination
    queryset = Work.objects.all().order_by('-id')


class WorkView(generics.CreateAPIView):
    serializer_class = WorkSerializer
    queryset = Work.objects.all()


class WorkDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = WorkDetailSerializer
    queryset = Work.objects.all()


class WorkOfferView(generics.GenericAPIView):
    serializer_class = WorkSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk=None):
        work = Work.objects.get(id=pk)
        user = request.user
        print(user.id)
        if not work.offers.filter(id=user.id).exists():
            work.offers.add(*[user,])
            work.save()
            return Response({
                'msg': f"Offer belgilandi {work.title} uchun"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': "Offer yozilib bo'lingan"
            }, status=status.HTTP_400_BAD_REQUEST)


class WorkAcceptView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        # try:
        serializer = WorkAcceptSerializer(data=request.data)
        user_id = request.user.id
        if serializer.is_valid():
            item_id = request.data.get("id")
            doer_id = request.data.get("doer")
            work = Work.objects.filter(id=item_id).first()
            if work.user_id == user_id:
                user = User.objects.get(id=doer_id)
                check = work.offers.filter(id=doer_id).first()
                if work.status != 'new':
                    return Response({
                        'msg': "Bu zakaz band qilingan"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not check:
                    return Response({
                        'msg': "Taklif bermagan odamlarni tanlab bo'lmaydi"
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    work.doer = user
                    work.status = 'selected'
                    # if user.works is not None:
                    # user.works.append(item_id)
                    # else:
                    #     print('Yo')
                    #     user.works = list(item_id)
                    user.save()
                    work.offers.clear()
                    work.save()
                    return Response({
                        'msg': "Успешно"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': "Пользователь не владелец"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({
        #         'msg': "Bad request"
        #     }, status=status.HTTP_400_BAD_REQUEST)


class CloseWorkView(generics.GenericAPIView):
    serializer_class = WorkSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk=None):
        work = Work.objects.get(id=pk)
        user = request.user
        if work.user_id == user.id:
            work.status = 'finished'
            work.save()
            if work.doer:
                doer = work.doer
                doer.jobs.remove(work)
                doer.works.remove(str(pk))
                doer.save()
                return Response({
                    'msg': "Работа закрыта"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': "Груз закрыта",
                    }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': "Пользователь не владелец"
            }, status=status.HTTP_400_BAD_REQUEST)
