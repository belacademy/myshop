from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product, Token, Notification
from orders.models import Order
from django.http import HttpResponse, JsonResponse
import urllib
import json
import httplib2
from django.template import context,loader

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



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def invoice_list(request):
    try:
        t  = get_object_or_404(Token, id='1')
        token = t.token
    except:
        token = ""

    refreshtoken(token)

    t  = get_object_or_404(Token, id='1')
    token = t.token

    orders = Order.objects.all()
    for order in orders:
        h = httplib2.Http()
        resp, content = h.request("https://api-et.hellocash.net/invoices/%s" % order.hellocash_id,
                        method="GET",
                        headers={'Content-Type':'application/json',
                            'Authorization':'Bearer %s' % token})
        try:
            content = json.loads(content)
            order.status = content['status']
            order.save()
        except:
            print("Error updating invoice")
    return render(request,
                  'shop/product/invoice_list.html',
                  {
                   'orders': orders})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

def transfer_list(request):
    try:
        t  = get_object_or_404(Token, id=1)
        token = t.token
    except:
        token = ""

    refreshtoken(token)

    h = httplib2.Http()
    resp, content = h.request("https://api-et.hellocash.net/transfers",
                    method="GET",
                    headers={'Content-Type':'application/json',
                        'Authorization':'Bearer %s' % token})
    try:
        content = json.loads(content)
        print("TRANSFERS: %s" % content)
    except:
        print("Error getting transfers")
    return render(request,
                  'shop/product/transfer_list.html',
                  {
                   'transfers': content})

def notification_list(request):
    flaggeds = Notification.objects.filter(flag=True)
    for flagged in flaggeds:
        flagged.seen = True
        flagged.save()

    unseens = Notification.objects.filter(seen=False)
    for unseen in unseens:
        unseen.flag = True
        unseen.save()
    notifications = Notification.objects.all().order_by('-id')
    return render(request,
                  'shop/product/notification_list.html',
                  {
                   'notifications': notifications})

def retrivenotifications(request):
    count = int(request.GET.get('count'))
    total = Notification.objects.all().count()
    if total > count:
        unseens = Notification.objects.filter(seen=False)
        for unseen in unseens:
            unseen.flag = True
            unseen.save()
            
        notifications = Notification.objects.all().order_by('-id')[0:total-count]

        context = {
                    'notifications': notifications,
                }
        template = loader.get_template('shop/product/notifications.html')
        html = template.render(context)

        return JsonResponse({'html':html,'count':total},
            status=200,content_type="application/json")
    else:
        return HttpResponse(status=204)

def unseencount(request):
    unseen = Notification.objects.filter(seen=False).count()
    return JsonResponse({'unseen':unseen})
