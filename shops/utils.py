from django.core.mail import send_mail

def send_order_notification(order,email_from = '',email_to = []):
    order_notification = "Order details\n"
    order_notification += f'Date: {order.date_ordered.date()} {order.date_ordered.time()}\n'
    order_notification += f'Name: {order.first_name} {order.last_name}\n'
    order_notification += f'Phone number: {order.phone_number}\n'
    order_notification += f'Delivery Option: {order.delivery_option}\n'
    order_notification += 'Items Ordered:\n'

    for item in order.cart_items:
        order_item = f'{item.quantity} {item.product.product_name}(s) at {item.get_total} Ksh \n'
        order_notification+=order_item

    order_notification += f'Order total:{order.get_cart_total} Ksh\n'

    send_mail(
        subject='Order notification',
        message = order_notification,
        from_email = email_from,
        recipient_list = email_to,
        fail_silently = False,
    )