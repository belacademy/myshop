from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order
from shop.models import Notification
def webhook(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        print("BODY %s" % body)
        try:
            tracenumber = body['tracenumber']
            order = get_object_or_404(Order, tracenumber=tracenumber)

            if body['status'] == 'PROCESSED':
                subject = 'Payment Confirmation'
                message = ' A purchase by tracenumber of  ' + tracenumber + ' by ' + \
                order.full_name + ' is Processed Successfully. \nID: ' + body['id'] + \
                ' \nThe description for payment: ' + body['description'] + '\nPayment Date: ' + \
                    body['processdate'] + '\n\n THANK YOU FOR USING OUR SERVICE!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['nigatutesfaye2008@gmail.com',]
                send_mail( subject, message, email_from, recipient_list )

                notif = Notification.objects.create(text=message, date=body['processdate'])
                notif.save()

                subject = 'Payment Confirmation'
                message = 'Dear ' + order.full_name + ' A purchase by tracenumber of  ' + tracenumber + \
                ' is Processed Successfully. \nID: ' + body['id'] + \
                ' \nThe description for payment: ' + body['description'] + '\nPayment Date: ' + \
                    body['processdate'] + '\n\n THANK YOU FOR USING OUR SERVICE!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [order.email,]
                send_mail( subject, message, email_from, recipient_list )



            if body['status'] == 'DENIED':
                subject = 'Payment Denied'
                message = ' A purchase by tracenumber of  ' + tracenumber + ' by ' + \
                order.full_name + ' is Denied. The description for payment is ' + body['description']
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['nigatutesfaye2008@gmail.com',]
                send_mail( subject, message, email_from, recipient_list )

                notif = Notification.objects.create(text=message, date=body['processdate'])
                notif.save()
        except:
            if body['status'] == 'PROCESSED':
                subject = 'Transfer Confirmation'
                message = ' A transfer to ' + body['toname'] + '(' +body['to']+')' + ' With Account number ' + body['toaccount'] + \
                ' is Processed Successfully. \nThe description of transfer: ' + body['description'] + \
                '\nThe Amount of Transfer: ' + str(body['amount']) + '\nTransfer fee: ' + str(body['fee']) + '\nTransfer Date: ' + \
                body['processdate'] + '\n\n THANK YOU FOR BANKING WITH US!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['nigatutesfaye2008@gmail.com',]
                send_mail( subject, message, email_from, recipient_list )

                notif = Notification.objects.create(text=message, date=body['processdate'])
                notif.save()
    return HttpResponse()
