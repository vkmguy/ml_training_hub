# ml_app/views.py

import json

import joblib
import numpy as np
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MLAccuracy
from .serializers import MLAccuracySerializer
from .tasks import train_ml_model_task


@api_view(['GET'])
@csrf_exempt
@transaction.atomic
def train_ml_model(request):
    train_ml_model_task.delay()
    return JsonResponse({'message': 'ML model training task has been triggered successfully.'},
                        status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def get_ml_accuracies(request):
    daily_accuracies = MLAccuracy.objects.values('timestamp', 'metrics').order_by('-timestamp')[:10]
    serializer = MLAccuracySerializer(daily_accuracies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def visualize_model(request):
    latest_metrics = MLAccuracy.objects.values('timestamp', 'metrics').order_by('-timestamp')
    serializer = MLAccuracySerializer(latest_metrics, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def get_ml_prediction(request):
    # Load the pre-trained model
    model = joblib.load('random_forest_classifier.joblib')
    try:
        data = json.loads(request.body.decode('utf-8'))
        input_data = np.array([
            data["open"],
            data["low"],
            data["high"],
            data["volume"],
            data["dividends"],
            data["stock_splits"]
        ]).reshape(1, -1)
        prediction = model.predict(input_data)
        return JsonResponse({'prediction': prediction[0]})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def visualization_page(request):
    return render(request, 'tmfa/visualization.html')
