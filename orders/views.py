from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from shop.models import Token
import urllib
import json
import httplib2
import datetime
from dateutil.relativedelta import relativedelta


def refreshtoken(token):

    h = httplib2.Http()
    resp, content = h.request("https://api-et.hellocash.net/invoices/",
                    method="GET",
                    headers={'Content-Type':'application/json',
                        'Authorization':'Bearer %s' % token})
    res = json.loads(content)
    try:
        if len(res['error']) > 0:
            data = {'principal': '1481689', 'token': 'laS96x1okyJLt9S9oywGunT54jXv4TZ3SY5mY4GLmWsvxd6pXi1oX1e4M7vBkmilJzkMz-8vdU7jFp3zEWUYhj-rxC3iaQgne7Q8uvIQ9H2u7XXXR6AV9aihWaCM1BUq7x5kinp-6xlw190k29bFh_cO_YaN7YNYPYzGLdH1IYQ', 'system':'lucy'}
            h = httplib2.Http()
            resp, content = h.request("https://api-et.hellocash.net/authenticate", method="POST", body=json.dumps(data), headers={'Content-Type':'application/json'})
            content = json.loads(content)
            token = content['token']
            try:
                t  = get_object_or_404(Token, id='1')
                t.token = token
                t.save()
            except:
                token = Token.objects.create(token=token)
                token.save()
            print("TOKEN REFRESHED")
    except:
        print("Working Token")

def order_create(request):

    try:
        t  = get_object_or_404(Token, id='1')
        token = t.token
    except:
        token = ""

    refreshtoken(token)

    t  = get_object_or_404(Token, id='1')
    token = t.token

    cart = Cart(request)
    description = "Purchase for ["
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                description = description + str(item['product'])  + '-'  + str(item['quantity']) + '|'
            description = description + '] from Robera Super Market.'
            # clear the cart
            print("description: %s" % description)
            print(order.get_total_cost)
            weeks_ahead = datetime.datetime.now() + relativedelta(weeks=1)
            exp_date = weeks_ahead.date().strftime('%Y-%m-%d')
            expiry = exp_date + "T24:00:00.000Z"
            print(expiry)

            if order.phone[0:2] == "09":
                order.phone = order.phone[0:2].replace("09", "+2519")+order.phone[2:]
                order.save()
            data = {
                "amount": float(order.get_total_cost()),
                "description": description,
                "from": order.phone,
                "currency": "ETB",
                "tracenumber": "Nigatu_Invoice_000%s" % order.id,
                "notifyfrom": True,
                "notifyto": True,
                "expires": expiry
            }

            '''
            h = httplib2.Http()
            resp, content = h.request("https://api-et.hellocash.net/invoices",
                        method="POST", body=json.dumps(data),
                        headers={'Content-Type':'application/json',
                            'Authorization':'Bearer %s' % token})
            try:
                content = json.loads(content)
                order.full_name = content['fromname']
                order.hellocash_id = content['id']
                order.tracenumber = content['tracenumber']
                order.expires = content['expires']
                order.status = content['status']
                order.save()

                print(content)
            except:
                print("Error sending invoice")
            '''
            cart.clear()
            # launch asynchronous task
            #order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
