import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
from django.db.models import Q, F, Max, Min, Count, Case, When, Value, BooleanField
from django.db import connection, reset_queries


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    all_profiles = Profile.objects.prefetch_related('orders').filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not all_profiles.exists():
        return ""

    result = []
    for profile in all_profiles:
        orders_count = len(profile.orders.all())
        result.append(f'Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, orders: {orders_count}')

    return '\n'.join(result)


def get_loyal_profiles():
    all_ordered_profiles = Profile.objects.get_regular_customers()

    if not all_ordered_profiles.exists():
        return ""

    result = []
    for profile in all_ordered_profiles:
        result.append(f"Profile: {profile.full_name}, orders: {profile.orders_count}")

    return '\n'.join(result)


def get_last_sold_products():
    last_order = Order.objects.all().order_by('products__name').last()

    if not last_order:
        return ""

    all_products = [x.name for x in last_order.products.all()]
    result = f"Last sold products: {', '.join(all_products)}"

    return result


def get_top_products():
    query = Product.objects.annotate(
        count_sold=Count('ordered')
        # I filter because i dont want to return product that is not sold at least ONCE IMPORTANT MISTAKE HERE !
    ).filter(
        count_sold__gt=0
    ).order_by('-count_sold', 'name')[:5]

    if not query.exists():
        return ""

    result = ["Top products:"]
    for product in query:
        result.append(f'{product.name}, sold {product.count_sold} times')

    return '\n'.join(result)


def apply_discounts():
    orders_to_update = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False
    ).update(
        total_price=F('total_price') * 0.90
    )

    return f"Discount applied to {orders_to_update} orders."


def complete_order():
    oldest_order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not oldest_order:
        return ""

    # for product in oldest_order.products.all():
    #     product.in_stock -= 1
    #     if product.in_stock == 0:
    #         product.is_available = False
    #
    #     product.save()


    proba = Product.objects.filter(
        ordered=oldest_order
    ).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            # realnto dova e edna zaqvki i in_stock shte bude 0 sled neq i tova che gore ima logica tq oshte ne se e izpulnila
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    # oldest_order.is_completed = True
    # oldest_order.save()

    print(proba)


complete_order()
