from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Donation
import razorpay
from django.conf import settings
import csv
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as DjangoUser
@api_view(['POST'])
def register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get("password")
    if not name or not email:
        return Response(
            {"error": "Name and email are required"},
            status=400
        )

    try:
        user = User.objects.create(name=name, email=email,password=make_password(password))
        return Response(
            {"message": "Registration successful"},
            status=201
        )
    except IntegrityError:
        return Response(
            {"error": "Email already registered. Please login."},
            status=400
        )


@api_view(['POST'])
def donate(request):
    user_id = request.data.get('user_id')
    amount = request.data.get('amount')

    donation = Donation.objects.create(
        user_id=user_id,
        amount=amount,
        status='PENDING'
    )

    return Response({
        "message": "Donation initiated",
        "donation_id": donation.id,
        "status": "PENDING"
    })
from django.utils import timezone

@api_view(['POST'])
def update_payment(request):
    donation_id = request.data.get('donation_id')
    status = request.data.get('status')

    if status not in ['SUCCESS', 'FAILED']:
        return Response(
            {"error": "Invalid payment status"},
            status=400
        )

    try:
        donation = Donation.objects.get(id=donation_id)
    except Donation.DoesNotExist:
        return Response(
            {"error": "Donation not found"},
            status=404
        )

    donation.status = status

    if status == 'SUCCESS':
        donation.confirmed_at = timezone.now()

    donation.save()

    return Response({
        "message": "Payment status updated",
        "donation_id": donation.id,
        "status": donation.status
    })

@api_view(['POST'])
def common_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    # ADMIN LOGIN
    try:
        admin = DjangoUser.objects.get(username=email)
        if admin.check_password(password) and (admin.is_superuser or admin.is_staff):
            return Response({
                "login": "success",
                "role": "admin"
            })
    except DjangoUser.DoesNotExist:
        pass

    # NORMAL USER LOGIN
    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)
    
    if not (check_password(password, user.password)):
        return Response({"error": "Invalid credentials"}, status=401)

    return Response({
        "login": "success",
        "role": "user",
        "user_id": user.id,
        "name": user.name
    })

@api_view(['GET'])
def donation_history(request, user_id):
    donations = Donation.objects.filter(user_id=user_id).order_by('-attempted_at')

    data = []
    for d in donations:
        data.append({
            "donation_id": d.id,
            "amount": float(d.amount),
            "status": d.status,
            "date": d.attempted_at.strftime("%Y-%m-%d %H:%M")
        })

    return Response({
        "user_id": user_id,
        "donations": data
    })
from django.db.models import Sum

@api_view(['GET'])
def admin_summary(request):
    total_users = User.objects.count()
    total_donations = Donation.objects.count()

    total_amount = Donation.objects.filter(
        status='SUCCESS'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    successful = Donation.objects.filter(status='SUCCESS').count()
    failed = Donation.objects.filter(status='FAILED').count()
    pending = Donation.objects.filter(status='PENDING').count()

    return Response({
        "total_users": total_users,
        "total_donations": total_donations,
        "total_amount_collected": float(total_amount),
        "donations": {
            "success": successful,
            "failed": failed,
            "pending": pending
        }
    })
@api_view(['GET'])
def admin_all_donations(request):
    donations = Donation.objects.select_related('user').all()

    data = []
    for d in donations:
        data.append({
            "donation_id": d.id,
            "user_name": d.user.name,
            "user_id": d.user.id,  
            "user_email": d.user.email,
            "amount": d.amount,
            "status": d.status,
            "date": d.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return Response({
        "donations": data
    })
@api_view(['GET'])
def admin_user_donations(request, email):
    donations = Donation.objects.filter(user__email=email)

    data = [{
        "donation_id": d.id,
        "user_id": d.user.id,         
        "user_name": d.user.name,
        "user_email": d.user.email,
        "amount": d.amount,
        "status": d.status,
        "date": d.created_at.strftime("%Y-%m-%d %H:%M")
    } for d in donations]

    return Response({"donations": data})
@api_view(['GET'])
def admin_users_list(request):
    users = User.objects.all()

    data = []
    for u in users:
        data.append({
            "user_id": u.id,
            "name": u.name,
            "email": u.email
        })

    return Response({
        "total_users": len(data),
        "users": data
    })
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

@api_view(['POST'])
def create_razorpay_order(request):
    donation_id = request.data.get("donation_id")
    amount = request.data.get("amount")

    if not donation_id or not amount:
        return Response({"error": "Invalid data"}, status=400)

    order = client.order.create({
        "amount": int(amount) * 100,   # paise
        "currency": "INR",
        "payment_capture": 1
    })

    return Response({
        "order_id": order["id"],
        "key": settings.RAZORPAY_KEY_ID
    })
def export_users_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="registered_users.csv"'

    writer = csv.writer(response)
    writer.writerow(["User ID", "Name", "Email"])

    for user in User.objects.all():
        writer.writerow([
            user.id,
            user.name,
            user.email
        ])

    return response
def export_donations_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="donations.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Donation ID",
        "User Name",
        "User Email",
        "Amount",
        "Status",
        "Date"
    ])

    for d in Donation.objects.select_related("user").all():
        writer.writerow([
            d.id,
            d.user.name,
            d.user.email,
            d.amount,
            d.status,
            d.created_at if hasattr(d, "created_at") else ""
        ])

    return response

