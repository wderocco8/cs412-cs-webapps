from django.shortcuts import render, redirect
import random
from datetime import datetime, timedelta

# Create your views here.

def main(request):
    '''Show the main page.'''

    template_name = "restaurants/main.html"
    return render(request, template_name)

def order(request):
    '''
    Handle the form submission.
    Read the form data from the request,
    and send it back to a template.
    '''

    # Randomly choose a daily special from a list
    daily_specials = ['Pizza Margherita', 'Pasta Carbonara', 'Grilled Salmon', 'Caesar Salad']
    daily_special = random.choice(daily_specials)


    # Pass the daily special to the order template
    return render(request, 'restaurants/order.html', {'daily_special': daily_special})

    
def confirmation(request):
    '''Show the confrimation page.'''

    # check that we have a POST request
    if request.POST:

        # read the form data into python variables
        # Read form data from request
        ordered_items = request.POST.getlist('items')
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')

        #  Calculate total price based on item prices
        item_prices = {'Pizza': 12.99, 'Pasta': 10.99, 'Salad': 8.99, 'Special': 14.99}
        total_price = sum(item_prices[item] for item in ordered_items if item in item_prices)

        # Calculate a random ready time (between 30-60 minutes)
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        # Pass order data to confirmation template
        context = {
            'ordered_items': ordered_items,
            'customer_name': customer_name,
            'total_price': total_price,
            'ready_time': ready_time.strftime("%H:%M"),
            'customer_phone': customer_phone,
            'customer_email': customer_email
        }

        return render(request, 'restaurants/confirmation.html', context)

    # if GET request, redirect to order page
    return redirect("rest_order")