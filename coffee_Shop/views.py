from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
import os
from django.conf import settings

from coffee_Shop.forms import MenuItemForm
from .models import MenuItem, Order
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from datetime import datetime
from django.db.models import Sum, F


def home(request):
    return render(request, 'home.html')


def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {'items': items})



def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()
            
            # Store item ID in session
            request.session.setdefault('menu_item_ids', [])
            menu_item_ids = request.session['menu_item_ids']
            menu_item_ids.append(new_item.id)
            request.session['menu_item_ids'] = list(set(menu_item_ids))  # Avoid duplicates

            return redirect('coffee_app:menu')
    else:
        form = MenuItemForm()
    return render(request, 'add_item.html', {'form': form})


def add_to_order(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)
        order = request.session.get('order', [])
        order.append(item_id)
        request.session['order'] = order
    return redirect('coffee_Shop:menu')



# def remove_item(request, item_id):
#     menu_item_ids = request.session.get('menu_item_ids', [])
#     if item_id in menu_item_ids:
#         menu_item_ids.remove(item_id)
#         request.session['menu_item_ids'] = menu_item_ids
#     return redirect('coffee_app:order')


def order_view(request):
    order_ids = request.session.get('order', [])
    print(order_ids)
    items = MenuItem.objects.filter(id__in=order_ids)
    print("items", items)

    # Count quantity for each item
    item_counts = {}
    for item_id in order_ids:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
    
    print(item_counts)
    items_with_quantity = []
    for item in items:
        items_with_quantity.append({
            'item': item,
            'price': item.price,
            'item_image': item.image,
            'quantity': item_counts[item.id],
            'subtotal': item_counts[item.id] * item.price
        })

    print("items_with_quantity", items_with_quantity)
    total = sum(i['subtotal'] for i in items_with_quantity)
    print("total", total)

    return render(request, 'order.html', {'items': items_with_quantity, 'total': total})



def confirm_order(request):
    if request.method == 'POST':
        order_ids = request.session.get('order', [])
        if not order_ids:
            return redirect('coffee_Shop:order')

        items = MenuItem.objects.filter(id__in=order_ids)
        total_price = 0

        # Count total price considering quantity
        for item in items:
            total_price += order_ids.count(item.id) * item.price

        order = Order.objects.create(total_price=total_price)
        order.items.set(items)
        order.save()

        # Clear session after confirming
        request.session['order'] = []

        return render(request, 'order_summary.html', {'order': order})

    return redirect('coffee_Shop:order')


def delete_item(request, item_id):
    order = request.session.get('order', [])

    if item_id in order:
        order.remove(item_id)  # Removes one occurrence of the item_id
        request.session['order'] = order

    return redirect('coffee_Shop:order')

def remove_item(request, item_id):
    order = request.session.get('order', [])
    order = [id for id in order if id != item_id]
    request.session['order'] = order
    return redirect('coffee_Shop:order')

def add_item(request):
    return render(request, 'add_item.html')

def order(request):
    order_ids = request.session.get('order', [])
    items = MenuItem.objects.filter(id__in=order_ids)
    
    if not items.exists():
         
         pass
    
    return render(request, 'order.html', {'items': items})

@csrf_exempt
def menu_api(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        data = []
        for item in items:
            image_url = ''
            if item.image:
                try:
                    image_url = request.build_absolute_uri(item.image.url)
                except Exception:
                    image_url = ''
            data.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'image_url': image_url,
            })
        return JsonResponse({'items': data})
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            image_url = ''
            if item.image:
                try:
                    image_url = request.build_absolute_uri(item.image.url)
                except Exception:
                    image_url = ''
            return JsonResponse({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'image_url': image_url,
            }, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_exempt
def add_to_order_api(request, item_id):
    if request.method == 'POST':
        get_object_or_404(MenuItem, id=item_id)
        order = request.session.get('order', [])
        order.append(item_id)
        request.session['order'] = order
        return JsonResponse({'ok': True})
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

def order_api(request):
    if request.method == 'GET':
        order_ids = request.session.get('order', [])
        items = MenuItem.objects.filter(id__in=order_ids)
        counts = {}
        for iid in order_ids:
            counts[iid] = counts.get(iid, 0) + 1
        payload = []
        total = 0.0
        for item in items:
            qty = counts.get(item.id, 0)
            subtotal = float(item.price) * qty
            total += subtotal
            img = ''
            if item.image:
                try:
                    img = request.build_absolute_uri(item.image.url)
                except Exception:
                    img = ''
            payload.append({
                'id': item.id,
                'name': item.name,
                'price': float(item.price),
                'quantity': qty,
                'subtotal': subtotal,
                'image_url': img,
            })
        return JsonResponse({'items': payload, 'total': total})
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_item_api(request, item_id):
    if request.method == 'POST':
        order = request.session.get('order', [])
        if item_id in order:
            order.remove(item_id)
            request.session['order'] = order
        return JsonResponse({'ok': True})
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_exempt
def remove_item_api(request, item_id):
    if request.method == 'POST':
        order = request.session.get('order', [])
        order = [id for id in order if id != item_id]
        request.session['order'] = order
        return JsonResponse({'ok': True})
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_exempt
def confirm_order_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_name = data.get('name', 'Guest')
            customer_email = data.get('email', '')
            customer_phone = data.get('phone', '')
        except json.JSONDecodeError:
            customer_name = 'Guest'
            customer_email = ''
            customer_phone = ''

        order_ids = request.session.get('order', [])
        if not order_ids:
             return JsonResponse({'error': 'No items in order'}, status=400)

        items = MenuItem.objects.filter(id__in=order_ids)
        total_price = 0.0
        
        # Calculate details for CSV and Total
        item_details = []
        for item in items:
            count = order_ids.count(item.id)
            total_price += count * float(item.price)
            item_details.append(f"{item.name} (x{count})")
        
        order = Order.objects.create(
            total_price=total_price,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone
        )
        order.items.set(items)
        order.save()
        
        # Save to CSV
        orders_dir = os.path.join(settings.BASE_DIR, 'orders')
        os.makedirs(orders_dir, exist_ok=True)
        csv_file = os.path.join(orders_dir, 'orders.csv')
        
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Order ID', 'Customer Name', 'Email', 'Phone', 'Items', 'Total Price', 'Date'])
            
            writer.writerow([
                order.id,
                customer_name,
                customer_email,
                customer_phone,
                "; ".join(item_details),
                f"{total_price:.2f}",
                order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        request.session['order'] = []
        return JsonResponse({'order_id': order.id, 'total_price': float(order.total_price)})
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_exempt
def order_history_api(request):
    if request.method == 'GET':
        date_str = request.GET.get('date', '').strip()
        orders_dir = os.path.join(settings.BASE_DIR, 'orders')
        csv_file = os.path.join(orders_dir, 'orders.csv')
        if not os.path.isfile(csv_file):
            return JsonResponse({'orders': [], 'total_for_date': 0.0, 'daily_totals': []})
        orders = []
        daily_totals_map = {}
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    dt = datetime.strptime(row.get('Date', ''), '%Y-%m-%d %H:%M:%S')
                except Exception:
                    continue
                dkey = dt.strftime('%Y-%m-%d')
                try:
                    amt = float(row.get('Total Price', '0') or 0)
                except Exception:
                    amt = 0.0
                daily_totals_map[dkey] = daily_totals_map.get(dkey, 0.0) + amt
                if date_str:
                    dsel = parse_date(date_str)
                    if dsel and dkey == dsel.strftime('%Y-%m-%d'):
                        orders.append({
                            'order_id': int(row.get('Order ID', '0') or 0),
                            'time': dt.strftime('%H:%M:%S'),
                            'customer_name': row.get('Customer Name', ''),
                            'total_price': amt,
                            'items': row.get('Items', '')
                        })
        daily_totals = [{'date': k, 'total': v} for k, v in sorted(daily_totals_map.items(), reverse=True)]
        total_for_date = 0.0
        if date_str:
            total_for_date = sum(o['total_price'] for o in orders)
        return JsonResponse({'orders': orders, 'total_for_date': total_for_date, 'daily_totals': daily_totals})
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

