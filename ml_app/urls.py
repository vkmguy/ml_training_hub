"""
URL configuration for ml_training_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from ml_app.views import visualize_model, train_ml_model, get_ml_prediction, get_ml_accuracies, visualization_page

urlpatterns = [
    path('accuracies', get_ml_accuracies, name='get_ml_accuracies'),
    path('trainModel', train_ml_model, name='train_ml_model'),
    path('predict', get_ml_prediction, name='get_ml_prediction'),
    path('visualize_model', visualize_model, name='visualize_model'),
    path('visualization', visualization_page, name='visualization_page'),
]
