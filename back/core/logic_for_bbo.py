import datetime

from asgiref.sync import sync_to_async
from async_signals import Signal
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import json
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import LabValue, ProjValue
from .serializers import (labValueSerializer, projValueSerializer)


# ParameterFromAnalogSensorForBBOSerializer,
#                           BBOSerializer, ManagementConcentrationFlowForBBOSerializer, CommandForBBOSerializer,
#                           NotificationSerializer)


class GetDatesForLabValue(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date = []
        objs = LabValue.objects.all()
        i = 0
        for obj in objs:
            date.insert(i, obj.datetime.date())
            i = i + 1
        # print(date)
        out = list(dict.fromkeys(date))
        # print(out)
        return JsonResponse(out, status=status.HTTP_200_OK, safe=False)


class GetLabValueFromDates(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        lab = []
        labb = {}
        search_date = request.GET.get('search_date')
        objs = LabValue.objects.filter(datetime__date=search_date)
        i = 0
        for obj in objs:
            lab.insert(i, obj.id)

            labb[obj.id] = obj.modified_time
            i = i + 1
        serializer = self.serializer_class(objs, many=True)
        # print(labb)
        return JsonResponse(labb, status=status.HTTP_200_OK, safe=False)


class GetLabValueFromID(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        lab = []
        lab_id = request.GET.get('id')
        objs = LabValue.objects.filter(id=lab_id)
        print(lab)
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateLabValueByID(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, lab_id):
        # lab_id = request.PUT.get('id')
        try:
            lab_val = LabValue.objects.get(pk=lab_id)
            print(lab_val)
        except labValueSerializer.DoesNotExist:
            return JsonResponse({'message': 'The lab_val does not exist'}, status=status.HTTP_404_NOT_FOUND)
        new_data = JSONParser().parse(request)
        print(new_data)
        tutorial_serializer = labValueSerializer(lab_val, data=new_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLabValueView(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    # def get_all_values(self):
    #     serializers = {}
    #     values = {}
    #     i = 1
    #     for i in 4:
    #         try:
    #             value = ProjValue.objects.all().filter(bbo_id=i).last()
    #             values.pop(value, i)
    #         except Exception as _ex:
    #             print(_ex)
    #
    #     for value in values:
    #         j = 0
    #         serializer = self.serializer_class(value, many=False)
    #         serializers.pop(serializer, j)
    #         j = j + 1
    #     response = {
    #         'data_bbo_1': serializers.get(0),
    #         'data_bbo_2': serializers.get(1),
    #         'data_bbo_3': serializers.get(2),
    #         'data_bbo_4': serializers.get(3),
    #     }
    #     return response

    def post(self, request):
        if request.data['datetime']:
            datetime_lab = request.data['datetime']
        else:
            datetime_lab = datetime.datetime.now()
        del request.data['datetime']
        for i in range(len(request.data)):
            # print(request.data[f'bbo{i+1}'])
            request.data[f'bbo{i + 1}']['bbo_id'] = i + 1
            request.data[f'bbo{i + 1}']['datetime'] = datetime_lab

            serializer = self.serializer_class(data=request.data[f'bbo{i + 1}'])
            valid = serializer.is_valid(raise_exception=True)

            if valid:
                status_code = status.HTTP_200_OK
                serializer.save()

        values1 = LabValue.objects.all().filter(bbo_id=1).last()
        values2 = LabValue.objects.all().filter(bbo_id=2).last()
        values3 = LabValue.objects.all().filter(bbo_id=3).last()
        values4 = LabValue.objects.all().filter(bbo_id=4).last()
        values5 = LabValue.objects.all().filter(bbo_id=5).last()
        values6 = LabValue.objects.all().filter(bbo_id=6).last()
        values7 = LabValue.objects.all().filter(bbo_id=7).last()
        values8 = LabValue.objects.all().filter(bbo_id=8).last()
        # if values1 or values2 or values3 or values4 is None:
        #     response = {
        #         'success': True,
        #         'status_code': status.HTTP_200_OK,
        #         'message': 'Project values is empty',
        #     }
        # else:
        serializer1 = self.serializer_class(values1, many=False)
        serializer2 = self.serializer_class(values2, many=False)
        serializer3 = self.serializer_class(values3, many=False)
        serializer4 = self.serializer_class(values4, many=False)
        serializer5 = self.serializer_class(values5, many=False)
        serializer6 = self.serializer_class(values6, many=False)
        serializer7 = self.serializer_class(values7, many=False)
        serializer8 = self.serializer_class(values8, many=False)
        response = {
            'success': True,
            'status_code': status_code,
            'message': 'Successfully saved laboratory values',
            'datetime': datetime_lab,
            'data': {
                'bbo1': serializer1.data,
                'bbo2': serializer2.data,
                'bbo3': serializer3.data,
                'bbo4': serializer4.data,
                'bbo5': serializer5.data,
                'bbo6': serializer6.data,
                'bbo7': serializer7.data,
                'bbo8': serializer8.data,
            }
        }
        return Response(response, status=status_code)


class GetLabValueView(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bbo_id = request.data.get("bbo_id")
        values = ProjValue.objects.all().filter(bbo_id=bbo_id).last()
        if values is None:
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Laboratory values is empty',
            }
        else:
            serializer = self.serializer_class(values, many=False)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched laboratory values',
                'data': serializer.data,
                'request': request.data

            }
        return Response(response, status=status.HTTP_200_OK)


class PostProjValueView(GenericAPIView):
    serializer_class = projValueSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            serializer.save()

        values1 = ProjValue.objects.all().filter(bbo_id=1).last()
        values2 = ProjValue.objects.all().filter(bbo_id=2).last()
        values3 = ProjValue.objects.all().filter(bbo_id=3).last()
        values4 = ProjValue.objects.all().filter(bbo_id=4).last()
        # if values1 or values2 or values3 or values4 is None:
        #     response = {
        #         'success': True,
        #         'status_code': status.HTTP_200_OK,
        #         'message': 'Project values is empty',
        #     }
        # else:
        serializer1 = self.serializer_class(values1, many=False)
        serializer2 = self.serializer_class(values2, many=False)
        serializer3 = self.serializer_class(values3, many=False)
        serializer4 = self.serializer_class(values4, many=False)
        response = {
            'success': True,
            'status_code': status_code,
            'message': 'Successfully fetched project values',
            'data_bbo_1': serializer1.data,
            'data_bbo_2': serializer2.data,
            'data_bbo_3': serializer3.data,
            'data_bbo_4': serializer4.data,

        }
        return Response(response, status=status_code)


class GetProjValueView(GenericAPIView):
    serializer_class = projValueSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        bbo_id = request.data.get("bbo_id")
        values = ProjValue.objects.all().filter(bbo_id=bbo_id).last()
        if values is None:
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Project values is empty',
            }
        else:
            serializer = self.serializer_class(values, many=False)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched project values',
                'data': serializer.data,
                'request': request.data

            }
        return Response(response, status=status.HTTP_200_OK)


class GetAllBBOProjValueView(GenericAPIView):
    serializer_class = projValueSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        values1 = ProjValue.objects.all().filter(bbo_id=1).last()
        values2 = ProjValue.objects.all().filter(bbo_id=2).last()
        values3 = ProjValue.objects.all().filter(bbo_id=3).last()
        values4 = ProjValue.objects.all().filter(bbo_id=4).last()
        # if values1 or values2 or values3 or values4 is None:
        #     response = {
        #         'success': True,
        #         'status_code': status.HTTP_200_OK,
        #         'message': 'Project values is empty',
        #     }
        # else:
        serializer1 = self.serializer_class(values1, many=False)
        serializer2 = self.serializer_class(values2, many=False)
        serializer3 = self.serializer_class(values3, many=False)
        serializer4 = self.serializer_class(values4, many=False)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched project values',
            'data_bbo_1': serializer1.data,
            'data_bbo_2': serializer2.data,
            'data_bbo_3': serializer3.data,
            'data_bbo_4': serializer4.data,

        }
        return Response(response, status=status.HTTP_200_OK)


class GetAllBBOLabValueView(GenericAPIView):
    serializer_class = labValueSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        values1 = LabValue.objects.all().filter(bbo_id=1).last()
        values2 = LabValue.objects.all().filter(bbo_id=2).last()
        values3 = LabValue.objects.all().filter(bbo_id=3).last()
        values4 = LabValue.objects.all().filter(bbo_id=4).last()
        values5 = LabValue.objects.all().filter(bbo_id=5).last()
        values6 = LabValue.objects.all().filter(bbo_id=6).last()
        values7 = LabValue.objects.all().filter(bbo_id=7).last()
        values8 = LabValue.objects.all().filter(bbo_id=8).last()

        # if values1 or values2 or values3 or values4 is None:
        #     response = {
        #         'success': True,
        #         'status_code': status.HTTP_200_OK,
        #         'message': 'Project values is empty',
        #     }
        # else:
        serializer1 = self.serializer_class(values1, many=False)
        serializer2 = self.serializer_class(values2, many=False)
        serializer3 = self.serializer_class(values3, many=False)
        serializer4 = self.serializer_class(values4, many=False)
        serializer5 = self.serializer_class(values5, many=False)
        serializer6 = self.serializer_class(values6, many=False)
        serializer7 = self.serializer_class(values7, many=False)
        serializer8 = self.serializer_class(values8, many=False)
        datetime_lab = serializer1.data['datetime']
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched laboratory values',
            'datetime': datetime_lab,
            'data': {
                'bbo1': serializer1.data,
                'bbo2': serializer2.data,
                'bbo3': serializer3.data,
                'bbo4': serializer4.data,
                'bbo5': serializer5.data,
                'bbo6': serializer6.data,
                'bbo7': serializer7.data,
                'bbo8': serializer8.data,
            }

        }
        return Response(response, status=status.HTTP_200_OK)

#
# @api_view(['GET'])
# def stat_detail(request, ):
#     bbo_id = request.GET.getlist('bbo_id')
#     name = request.GET.getlist('name')
#     first_date = request.GET.get('first_date')
#     last_date = request.GET.get('last_date')
#     stat = {}
#     if name and bbo_id is not None:
#         for i in range(len(bbo_id)):
#             for j in range(len(name)):
#                 if first_date is None:
#                     first_date = '2000-01-01 00:00'
#                 if last_date is None:
#                     last_date = datetime.datetime.now()
#                 try:
#                     stat[f'bbo_{bbo_id[i]}_{name[j]}'] = (
#                         ParameterFromAnalogSensorForBBOSerializer(
#                             (
#                                 ParameterFromAnalogSensorForBBO.objects.filter(
#                                     bbo_id=int(bbo_id[i]),
#                                     name=name[j],
#                                     time__range=[first_date, last_date]
#                                 )
#                             ),
#                             many=True).data)
#                     if not stat[f'bbo_{bbo_id[i]}_{name[j]}']:
#                         del stat[f'bbo_{bbo_id[i]}_{name[j]}']
#                 except ParameterFromAnalogSensorForBBO.DoesNotExist:
#                     return JsonResponse({'message': 'Data does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         stat_serializer = []
#         if request.method == 'GET':
#             if stat == {}:
#                 return JsonResponse({'message': 'Data does not exist'}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 # for i in range(len(stat)):
#                 #     stat_serializer.append(ParameterFromAnalogSensorForBBOSerializer(stat[i], many=True).data)
#                 return JsonResponse({'data': stat})
#     else:
#         return JsonResponse({'msg': 'Error, check data'})
#
#
# class ParameterFromAnalogSensorForBBOView(GenericAPIView):
#     serializer_class = ParameterFromAnalogSensorForBBOSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = ParameterFromAnalogSensorForBBOSerializer(data=data)
#         valid = serializer.is_valid(raise_exception=True)
#         if valid:
#             status_code = status.HTTP_200_OK
#             serializer.save()
#
#             # if data['name'] == 'OVP' and data['value'] <= -200.0:
#             #     value = data['value']
#             #     Notification.objects.create(
#             #         bbo_id=BBO.objects.get(id=data['bbo_id']),
#             #         status_code=0,
#             #         title=data['name'],
#             #         message='Возможно идет сброс сточных вод от промышленных промпредприятий, отобрать анализы '
#             #                 'на входе'
#             #     )
#             #
#             # if data['name'] == 'acidity' and (data['value'] <= 6.5 or data['value'] >= 8.5):
#             #     Notification.objects.create(
#             #         bbo_id=BBO.objects.get(id=data['bbo_id']),
#             #         status_code=0,
#             #         title=data['name'],
#             #         message='Необходимо провести обследование на наличие сброса промышленных сточных вод, '
#             #                 'при возможности запустить резервный осветлитель-перегниватель'
#             #     )
#             #
#             # if data['name'] == 'temperature' and data['value'] <= 25.0:
#             #     Notification.objects.create(
#             #         bbo_id=BBO.objects.get(id=data['bbo_id']),
#             #         status_code=0,
#             #         title=data['name'],
#             #         message='Необходимо обратить внимание на интенсивность процесса денитрификации'
#             #     )
#             #
#             # if data['name'] == 'turbidity' and data['value'] <= 2.0:
#             #     Notification.objects.create(
#             #         bbo_id=BBO.objects.get(id=data['bbo_id']),
#             #         status_code=0,
#             #         title=data['name'],
#             #         message='Необходиомо перераспределить потоки активного ила по биоблокам'
#             #     )
#
#         response = {
#             'success': True,
#             'status_code': status_code,
#             'message': 'Successfully saved parameter values',
#         }
#         return Response(response, status=status_code)
#
#
# class AllParameterFromAnalogSensorForBBO1View(ListCreateAPIView):
#     serializer_class = ParameterFromAnalogSensorForBBOSerializer
#     queryset = ParameterFromAnalogSensorForBBO.objects.filter(bbo_id=1)
#
#
# class AirManagerView(GenericAPIView):
#     serializer_class = ManagementConcentrationFlowForBBOSerializer
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         values1 = ManagementConcentrationFlowForBBO.objects.all().filter(bbo_id=1).last()
#         serializer1 = self.serializer_class(values1, many=False)
#         response = {
#             'success': True,
#             'status_code': status.HTTP_200_OK,
#             'message': 'Successfully fetched values',
#             'data_bbo_1': serializer1.data,
#         }
#         return Response(response, status=status.HTTP_200_OK)
#
#     def post(self, request):
#
#         data = JSONParser().parse(request)
#         nam_6 = data['name'][:6]
#         data['current_value'] = ParameterFromAnalogSensorForBBO.objects.filter(bbo_id=data['bbo_id'],
#                                                                                name=nam_6).last().value
#         if ParameterFromAnalogSensorForBBO.objects.filter(bbo_id=data['bbo_id'], name=nam_6).last().is_accident:
#             data['is_not_accident'] = False
#         else:
#             data['is_not_accident'] = True
#         serializer = ManagementConcentrationFlowForBBOSerializer(data=data)
#
#         valid = serializer.is_valid(raise_exception=True)
#         if valid:
#             status_code = status.HTTP_200_OK
#             serializer.save()
#             my_signal = Signal(debug=True)
#
#         response = {
#             'success': True,
#             'status_code': status_code,
#             'message': 'Successfully saved values',
#         }
#         return Response(response, status=status_code)
#
#
# class CommandForBBOView(GenericAPIView):
#     serializer_class = CommandForBBOSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = CommandForBBOSerializer(data=data)
#
#         valid = serializer.is_valid(raise_exception=True)
#         if valid:
#             status_code = status.HTTP_200_OK
#             serializer.save()
#
#         response = {
#             'success': True,
#             'status_code': status_code,
#             'message': 'Successfully saved values',
#         }
#         return Response(response, status=status_code)
