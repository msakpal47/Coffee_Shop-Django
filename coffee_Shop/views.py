from django.shortcuts import render, redirect

from coffee_Shop.forms import MenuItemForm
from .models import MenuItem, Order
from django.shortcuts import get_object_or_404


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
        order.append(item_id)  # Allowing multiple quantities
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
         #Optionally, add a message or handle empty order
         pass
    
    return render(request, 'order.html', {'items': items})

