"""restaurant URL Configuration

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
from django.urls import path, include
from payments import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("<str:lang>/table/<int:table_id>/", views.index, name="index"),
    path(
        "<str:lang>/table/<int:table_id>/item-details/",
        views.item_details,
        name="item-details",
    ),
    path(
        "<str:lang>/table/<int:table_id>/payment/start/",
        views.start_payment,
        name="start_payment",
    ),
    path(
        "<str:lang>/table/<int:table_id>/payment/ok/",
        views.payment_ok,
        name="payment_ok",
    ),
    path(
        "<str:lang>/table/<int:table_id>/payment/nok/",
        views.payment_nok,
        name="payment_nok",
    ),
    path(
        "<str:lang>/table/<int:table_id>/payment/notify/",
        views.payment_notify,
        name="payment_notify",
    ),
    # path("checkout/", views.process_checkout, name="process_checkout"),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/",
        views.order_details,
        name="order_details",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/remove_item_from_cart/",
        views.remove_item_from_cart,
        name="remove_item_from_cart",
    ),
    path(
        "<str:lang>/table/<int:table_id>/notification/",
        views.notification,
        name="notification",
    ),
    path(
        "<str:lang>/table/<int:table_id>/add_to_cart/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/change_variant/",
        views.change_variant,
        name="change_variant",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/item_quantity/",
        views.update_order_item_quantity,
        name="item_quantity",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/cash_payment/",
        views.cash_payment,
        name="cash_payment",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/card_payment/",
        views.start_payment,
        name="card_payment",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/update_order_item_quantity/",
        views.update_order_item_quantity,
        name="update_order_item_quantity",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/update_total/",
        views.update_total,
        name="update_total",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/save_tip_percentage/",
        views.save_tip_percentage,
        name="save_tip_percentage",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/thanks/",
        views.thanks,
        name="thanks",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/thanks/notification_thanks/",
        views.notification_thanks,
        name="notification_thanks",
    ),
    path(
        "<str:lang>/table/<int:table_id>/order/<str:order_id>/order_details/thanks_pt/",
        views.thanks,
        name="thanks_pt",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
