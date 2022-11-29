"""shipper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from views import create_shipment, update_shipment_status, get_shipment, cancel_shipment, print_label
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shipment/create',
         create_shipment,
         name='create_shipment'),
    path('api/shipment/update',
         update_shipment_status,
         name='update_shipment'),
    path('api/shipment/',
         get_shipment,
         name='get_shipment'),
    path('api/shipment/cancel',
         cancel_shipment,
         name='cancel_shipment'),
	path('api/shipment/<int:id>/print',
         print_label,
         name='print_label'),
	# OpenAPI 3 documentation with Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]
