from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from .forms import PaymentForm, ClientForm
from django.http import HttpResponse
from .models import (
    Payment,
    Category,
    MenuItem,
    Variant,
    Staff,
    Order,
    OrderItem,
    Client,
    Subcategory,
)
import hashlib
import hmac
import requests
import time
import json
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from OpenSSL import crypto
from telegram import Bot
import requests
import logging
from django.utils import translation
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.utils.translation import activate

SECRET_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCf0TdcTuphb7X+Zwekt1XKEWZDczSGecfo6vQfqvraf5VPzcnJ
2Mc5J72HBm0u98EJHan+nle2WOZMVGItTa/2k1FRWwbt7iQ5dzDh5PEeZASg2UWe
hoR8L8MpNBqH6h7ZITwVTfRS4LsBvlEfT7Pzhm5YJKfM+CdzDM+L9WVEGwIDAQAB
AoGAYfKxwUtEbq8ulVrD3nnWhF+hk1k6KejdUq0dLYN29w8WjbCMKb9IaokmqWiQ
5iZGErYxh7G4BDP8AW/+M9HXM4oqm5SEkaxhbTlgks+E1s9dTpdFQvL76TvodqSy
l2E2BghVgLLgkdhRn9buaFzYta95JKfgyKGonNxsQA39PwECQQDKbG0Kp6KEkNgB
srCq3Cx2od5OfiPDG8g3RYZKx/O9dMy5CM160DwusVJpuywbpRhcWr3gkz0QgRMd
IRVwyxNbAkEAyh3sipmcgN7SD8xBG/MtBYPqWP1vxhSVYPfJzuPU3gS5MRJzQHBz
sVCLhTBY7hHSoqiqlqWYasi81JzBEwEuQQJBAKw9qGcZjyMH8JU5TDSGllr3jybx
FFMPj8TgJs346AB8ozqLL/ThvWPpxHttJbH8QAdNuyWdg6dIfVAa95h7Y+MCQEZg
jRDl1Bz7eWGO2c0Fq9OTz3IVLWpnmGwfW+HyaxizxFhV+FOj1GUVir9hylV7V0DU
QjIajyv/oeDWhFQ9wQECQCydhJ6NaNQOCZh+6QTrH3TC5MeBA1Yeipoe7+BhsLNr
cFG8s9sTxRnltcZl1dXaBSemvpNvBizn0Kzi8G3ZAgc=
-----END RSA PRIVATE KEY-----"""

TELEGRAM_BOT_TOKEN = "7925230097:AAFkE1ltyStxpwOx_bxWU8xWXGSAQN6f5Sc"

chat_ids = Staff.objects.values_list("chat_id", flat=True)

logger = logging.getLogger(__name__)


def index(request, table_id, lang):

    order_id = request.session.get("order_id")
    if order_id:

        order = get_object_or_404(Order, order_id=order_id)
    else:

        order_id = str(int(time.time()))
        order = Order.objects.create(
            order_id=order_id, total_amount="0.00", table_id=table_id
        )
        request.session["order_id"] = order_id

    # Загружаем категории
    oysters_category = Category.objects.get(name="Oysters")
    food_category = Category.objects.get(name="Food")
    cocktails_category = Category.objects.get(name="Cocktails")
    wine_category = Category.objects.get(name="Wine")
    soft_category = Category.objects.get(name="Soft Drinks")
    noalc_category = Category.objects.get(name="No Alcohol")
    categories = Category.objects.all().order_by("order")
    order_items = OrderItem.objects.filter(order=order)

    for category in categories:
        category.sorted_subcategories = category.subcategories.all().order_by("order")

    if lang == "en":
        return render(
            request,
            "index.html",
            {
                "category": Category.objects.all,
                "oysters": oysters_category,
                "food": food_category,
                "variants": Variant.objects.all,
                "item": MenuItem.objects.all,
                "cocktails": cocktails_category,
                "soft-drinks": soft_category,
                "wine": wine_category,
                "no-alcohol": noalc_category,
                "category_list": categories,
                "order": order,
                "table_id": table_id,
                "lang": lang,
                "order_items": order_items,
            },
        )
    elif lang == "pt":
        return render(
            request,
            "index_pt.html",
            {
                "category": Category.objects.all,
                "oysters": oysters_category,
                "food": food_category,
                "variants": Variant.objects.all,
                "item": MenuItem.objects.all,
                "cocktails": cocktails_category,
                "soft-drinks": soft_category,
                "wine": wine_category,
                "no-alcohol": noalc_category,
                "category_list": categories,
                "order": order,
                "table_id": table_id,
                "lang": lang,
                "order_items": order_items,
            },
        )
    else:
        print("Language is not supported")
        return JsonResponse({"status": "error", "message": "Language is not supported"})


@require_POST
def add_to_cart(request, table_id, lang):
    item_id = request.POST.get("item_id")
    price = float(request.POST.get("price"))
    quantity = int(request.POST.get("quantity"))
    variant = request.POST.get("variant", None)

    print(f"Recieved data: {item_id}, {price}, {quantity}")

    # Получение заказа из сессии
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, order_id=order_id)

    menu_item = MenuItem.objects.get(id=item_id)
    variant_instance = None
    if variant:
        try:
            variant_instance = Variant.objects.get(name=variant, menu_item=menu_item)
        except Variant.DoesNotExist:
            variant_instance = None

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        menu_item=menu_item,
        variant=variant_instance,
        defaults={"quantity": quantity, "price": price},
    )
    if not created:
        order_item.quantity += quantity
        order_item.price = price
        order_item.save()

    total_amount = sum(item.price * item.quantity for item in order.items.all())
    order.total_amount = total_amount
    order.save()

    return JsonResponse(
        {
            "success": True,
            "total_amount": total_amount,
            "item_quantity": order_item.quantity,
        }
    )


def send_telegram_message(chat_id, message, parse_mode):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Notification sent to Telegram bot")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")


@csrf_exempt
def notification(request, table_id, lang):
    try:
        data = json.loads(request.body)
        table_id = table_id
        message = f"TABLE#{table_id} is calling"

        for chat_id in chat_ids:
            try:

                send_telegram_message(
                    chat_id=chat_id, message=message, parse_mode="HTML"
                )
                print(f"Message sent to chat {chat_id}")
            except Exception as e:
                print(f"Couldnt send massage to chat {chat_id}: {e}")

        response_data = {
            "status": "success",
            "message": "Order processed successfully!",
        }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def notification_thanks(request, table_id, lang, order_id):
    try:
        data = json.loads(request.body)
        table_id = table_id
        message = f"TABLE#{table_id} is calling"

        for chat_id in chat_ids:
            try:

                send_telegram_message(
                    chat_id=chat_id, message=message, parse_mode="HTML"
                )
                print(f"Message sent to chat {chat_id}")
            except Exception as e:
                print(f"Couldnt send massage to chat {chat_id}: {e}")

        response_data = {
            "status": "success",
            "message": "Order processed successfully!",
        }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def item_details(request, table_id, lang):
    cart = request.session.get("cart", [])
    item_id = request.GET.get("item_id")
    item = get_object_or_404(MenuItem, id=item_id)
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, order_id=order_id)

    if lang == "en":
        return render(
            request,
            "item-details.html",
            {"item": item, "cart": cart, "order": order, "lang": lang},
        )
    elif lang == "pt":
        return render(
            request,
            "item-details_pt.html",
            {"item": item, "cart": cart, "order": order, "lang": lang},
        )

    else:
        print("Language is not supported")
        return JsonResponse({"status": "error", "message": "Language is not supported"})


@csrf_exempt
def change_variant(request, lang, table_id, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")
            variant_name = data.get("variant")

            order = get_object_or_404(Order, order_id=order_id)
            menu_item = get_object_or_404(MenuItem, id=item_id)

            variant_instance = Variant.objects.filter(
                name=variant_name, menu_item=menu_item
            ).first()

            order_item = OrderItem.objects.filter(
                order=order,
                menu_item=menu_item,
                variant=variant_instance,
            ).first()

            if order_item:
                return JsonResponse(
                    {"status": "success", "quantity": order_item.quantity}
                )
            else:
                # Item does not exist
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Order item not found",
                        "quantity": 0,
                    },
                    status=404,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"An error occurred: {str(e)}"},
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@csrf_exempt
def update_order_item_quantity(request, lang, table_id, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")
            quantity = int(data.get("quantity"))
            variant_name = data.get("variant")  # Проверяем, есть ли вариант

            print(
                f"Received data: item_id={item_id}, quantity={quantity}, variant={variant_name}, order_id={order_id}"
            )

            order = get_object_or_404(Order, order_id=order_id)

            menu_item = get_object_or_404(MenuItem, id=item_id)

            variant_instance = None
            if variant_name:
                variant_instance = Variant.objects.filter(
                    name=variant_name, menu_item=menu_item
                ).first()
                if not variant_instance:
                    return JsonResponse(
                        {"status": "error", "message": "Variant not found"},
                        status=404,
                    )

            order_item = get_object_or_404(
                OrderItem,
                order=order,
                menu_item=menu_item,
                variant=variant_instance,
            )
            print(f"OrderItem found: {order_item}")

            if quantity <= 0:
                order_item.delete()

                subtotal = sum(item.price * item.quantity for item in order.items.all())
                order.total_amount = subtotal
                order.save()

                return JsonResponse(
                    {
                        "status": "success",
                        "subtotal": float(subtotal),
                        "total_amount": float(order.total_amount),
                        "message": "Item removed successfully",
                    }
                )
            else:
                order_item.quantity = quantity
                order_item.save()

                subtotal = sum(item.price * item.quantity for item in order.items.all())
                order.total_amount = subtotal
                order.save()

                return JsonResponse(
                    {
                        "status": "success",
                        "subtotal": float(subtotal),
                        "total_amount": float(order.total_amount),
                        "message": "Quantity updated successfully",
                    }
                )

        except OrderItem.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Order item not found"}, status=404
            )

        except ValueError as e:
            return JsonResponse(
                {"status": "error", "message": f"Invalid quantity value: {str(e)}"},
                status=400,
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"An error occurred: {str(e)}"},
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


def save_tip_percentage(request, order_id, table_id, lang):
    if request.method == "POST":
        tip_percentage = request.POST.get("tip_percentage")
        request.session["tip_percentage"] = float(tip_percentage)
        return JsonResponse(
            {"status": "success", "currentTipPercentage": tip_percentage}
        )
    return JsonResponse({"status": "error"}, status=400)


def update_total(request, order_id, table_id, lang):
    if request.method == "POST":
        try:

            data = json.loads(request.body)
            total_amount = data.get("total_amount")
            order_id = data.get("order_id")
            order = get_object_or_404(Order, order_id=order_id)
            order.total_amount = float(total_amount)
            order.save()

            return JsonResponse({"status": "success", "total_amount": total_amount})
        except Order.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Order not found"}, status=404
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


def cash_payment(request, order_id, table_id, lang):
    if request.method == "POST":
        try:

            data = json.loads(request.body)
            print("Data received:", data)

            order_id = data.get("order_id")
            print("Order ID:", order_id)

            order = Order.objects.get(order_id=order_id)
            print("Order found:", order)
            order.total_amount = data.get("total_amount")

            created_at = order.created_at
            client_name = data.get("name")
            client_surname = data.get("surname")
            client_email = data.get("email")
            client_birthday = data.get("birthday")
            invoice_choice = data.get("invoice")
            print(invoice_choice)
            if invoice_choice:
                invoice_choice = "invoice"
            else:
                invoice_choice = "no invoice"

            # Формируем сообщение
            message = f"""<b>TABLE # {table_id}</b>
            <b>ORDER # {order_id}</b>§
            {order.formatted_created_at}
            Client name: {client_name} ({lang})
            Email: {client_email}
            ______________________________________
            Payment method: <b>$CASH</b>
            """
            message += "______________________________________"

            for item in order.items.all():
                menu_item = item.menu_item
                variant = item.variant
                variant_name = variant.name if variant else ""
                message += f"{menu_item.name} {variant_name} - {item.quantity}\n"
                # x €{item.price:.2f} = €{item.price * item.quantity:.2f}

            message += f"""______________________________________
            <b>TOTAL: €{order.total_amount:.2f}</b>
            """
            message += f"Invoice: {invoice_choice}"

            for chat_id in chat_ids:
                try:
                    send_telegram_message(
                        chat_id=chat_id, message=message, parse_mode="HTML"
                    )
                    print(f"Message sent to chat {chat_id}")
                except Exception as e:
                    print(f"Couldn't send message to chat {chat_id}: {e}")

            client = Client.objects.create(
                name=client_name,
                surname=client_surname,
                birthday=client_birthday,
                email=client_email,
            )
            print("Client created:", client_name)

            order.client = client

            if lang == "en":
                redirect_url = reverse("thanks", args=[lang, table_id, order_id])
            elif lang == "pt":
                redirect_url = reverse("thanks_pt", args=[lang, table_id, order_id])

            return JsonResponse({"redirect_url": redirect_url})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"error": "An error occurred during payment processing."}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)


def thanks(request, table_id, order_id, lang):
    return render(request, "thanks.html", {"table_id": table_id, "lang": lang})


def order_details(request, order_id, table_id, lang):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    if lang == "en":
        return render(
            request,
            "order_details.html",
            {
                "order": order,
                "order_items": order_items,
                "form": ClientForm,
                "table_id": table_id,
                "lang": lang,
            },
        )
    elif lang == "pt":
        return render(
            request,
            "order_details_pt.html",
            {
                "order": order,
                "order_items": order_items,
                "form": ClientForm,
                "table_id": table_id,
                "lang": lang,
            },
        )
    else:
        print("Language is not supported")
        return JsonResponse({"status": "error", "message": "Language is not supported"})


@require_POST
def remove_item_from_cart(request, order_id, table_id, lang):
    try:

        data = json.loads(request.body)
        item_id = data.get("item_id")
        order_id = data.get("order_id")
        variant_name = data.get("variant")

        if item_id:

            order = get_object_or_404(Order, order_id=order_id)

            menu_item = get_object_or_404(MenuItem, id=item_id)

            variant_instance = None
            if variant_name:
                variant_instance = Variant.objects.filter(
                    name=variant_name, menu_item=menu_item
                ).first()
                if not variant_instance:
                    return JsonResponse(
                        {"status": "error", "message": "Variant not found"},
                        status=404,
                    )

            order_item = get_object_or_404(
                OrderItem,
                order=order,
                menu_item=menu_item,
                variant=variant_instance,
            )
            print(f"OrderItem found: {order_item}")

            if order_item:

                order_item.delete()

                total_amount = sum(
                    item.price * item.quantity for item in order.items.all()
                )

                order.total_amount = float(total_amount)
                order.save()

                return JsonResponse({"status": "success", "total_amount": total_amount})
            else:
                return JsonResponse({"status": "error", "message": "Item not found"})

        return JsonResponse(
            {"status": "error", "message": "Invalid request"}, status=400
        )

    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Order not found"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def payment_ok(request, table_id, lang):

    return render(request, "payments/payment_ok.html")


def payment_nok(request, table_id, lang):

    return render(request, "payments/payment_nok.html")


def payment_notify(request, table_id, lang):
    if request.method == "POST":

        order_id = request.POST.get("OrderID")
        status = request.POST.get(
            "Status"
        )  # Update with actual myPOS response structure

        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.status = status
            payment.save()
        except Payment.DoesNotExist:
            return HttpResponse(status=404)

        return HttpResponse(status=200)

    return HttpResponse(status=400)


def start_payment(request, table_id, lang, order_id):
    # order_id = "1730665302"
    # amount = "129.80"
    # currency = "EUR"

    # Prepare data for the myPOS API
    data = {
        "IPCmethod": "IPCPurchase",
        "IPCVersion": "1.4",
        "IPCLanguage": "EN",
        "SID": "000000000000010",
        "walletnumber": "61938166610",
        "Amount": "23.45",
        "Currency": "EUR",
        "OrderID": "pavelom1730665302",
        "URL_OK": "http://site.ext/paymentOK",
        "URL_Cancel": "http://site.ext/paymentNOK",
        "URL_Notify": "https://site.ext/paymentNotify",
        "CardTokenRequest": "0",
        "KeyIndex": "1",
        "PaymentParametersRequired": "1",
        "customeremail": "name@website.com",
        "customerfirstnames": "John Santamaria",
        "customerfamilyname": "Smith",
        "customerphone": "+23568956958",
        "customercountry": "DEU",
        "customercity": "Hamburg",
        "customerzipcode": "20095",
        "customeraddress": "Kleine Bahnstr. 41",
        "Note": "",
        "CartItems": "2",
        "Article_1": "HP ProBook 6360b sticker",
        "Quantity_1": "2",
        "Price_1": "10",
        "Currency_1": "EUR",
        "Amount_1": "20",
        "Article_2": "Delivery",
        "Quantity_2": "1",
        "Price_2": "3.45",
        "Currency_2": "EUR",
        "Amount_2": "3.45",
    }

    # Concatenate the values and base64 encode them
    conc_data = base64.b64encode(
        "-".join(str(v) for v in data.values()).encode()
    ).decode()

    # Load the RSA private key from the SECRET_KEY string
    private_key_obj = serialization.load_pem_private_key(
        SECRET_KEY.encode(), password=None, backend=default_backend()
    )

    # Sign the concatenated data
    signature = private_key_obj.sign(
        conc_data.encode(), padding.PKCS1v15(), hashes.SHA256()
    )

    # Base64 encode the signature
    signature = base64.b64encode(signature).decode()

    data["Signature"] = signature

    # Print the result
    print("Calculated Signature:", signature)
    print("\nFinal POST request data:")
    for key, value in data.items():
        print(f"{key}: {value}")

    # Send the POST request to myPOS
    response = requests.post("https://www.mypos.com/vmp/checkout-test", data=data)

    if response.status_code == 200:
        # Redirect to myPOS payment page
        return redirect("https://www.mypos.com/vmp/checkout-test")
    else:
        # Handle error
        print("Error:", response.status_code, response.text)
        pass
