from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Order, OrderItem
from products.models import Product
import json
from datetime import datetime, timedelta
from django.utils import timezone

# orders/views.py - Update the place_order function
def place_order(request):
    """Place order view"""
    current_language = request.session.get('ambertek_language') or request.COOKIES.get('ambertek_language', 'en')
    
    if request.method == 'POST':
        try:
            # Get cart items from session
            cart_items = request.session.get('cart', {})
            if not cart_items:
                messages.warning(request, 
                    "Your cart is empty" if current_language != 'sw' else "Carti yako ni tupu"
                )
                return redirect('cart_detail')
            
            # Calculate total
            total_amount = 0
            for product_id, item in cart_items.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    total_amount += product.price * item['quantity']
                except (Product.DoesNotExist, ValueError):
                    pass
            
            # Create order
            order = Order.objects.create(
                customer_name=request.POST.get('customer_name', '').strip(),
                customer_email=request.POST.get('customer_email', '').strip(),
                customer_phone=request.POST.get('customer_phone', '').strip(),
                customer_address=request.POST.get('customer_address', '').strip(),
                customer_city=request.POST.get('customer_city', '').strip(),
                customer_region=request.POST.get('customer_region', '').strip(),
                total_amount=total_amount,
                payment_method=request.POST.get('payment_method', 'cod'),
                notes=request.POST.get('notes', '').strip(),
                estimated_delivery=timezone.now().date() + timezone.timedelta(days=3)
            )
            
            # Create order items
            for product_id, item in cart_items.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    OrderItem.objects.create(
                        order=order,
                        product_id=product.id,
                        product_name=product.name,
                        quantity=item['quantity'],
                        price=product.price
                    )
                except (Product.DoesNotExist, ValueError):
                    pass
            
            # Send SMS/WhatsApp notifications (your existing function)
            send_order_notifications(order, cart_items, current_language)
            
            # Send email notifications
            email_success = False
            admin_email_success = False
            
            try:
                from utils.email_service import email_service
                
                # Send customer confirmation email
                if order.customer_email:
                    email_success = email_service.send_order_confirmation(order)
                    if email_success:
                        order.confirmation_email_sent = True
                        order.confirmation_email_sent_at = timezone.now()
                
                # Send admin notification email
                admin_email_success = email_service.send_admin_notification(order)
                if admin_email_success:
                    order.admin_email_sent = True
                    order.admin_email_sent_at = timezone.now()
                
                # Save email status
                if email_success or admin_email_success:
                    order.save(update_fields=[
                        'confirmation_email_sent', 'confirmation_email_sent_at',
                        'admin_email_sent', 'admin_email_sent_at'
                    ])
                    
            except Exception as e:
                print(f"Email service error: {e}")
            
            # Clear cart
            if 'cart' in request.session:
                del request.session['cart']
            
            # Prepare success message
            success_parts = []
            
            if current_language == 'sw':
                success_parts.append(f"Oda #{order.order_number} imewekwa kikamilifu!")
                
                if order.customer_email and email_success:
                    success_parts.append(f"Uthibitishaji umetumwa kwenye barua pepe: {order.customer_email}")
                elif order.customer_email and not email_success:
                    success_parts.append("Barua pepe haikutumwa, angalia spam folder.")
                
                success_parts.append("Tumetuma ujumbe wa uthibitisho kwa simu yako.")
                
            else:
                success_parts.append(f"Order #{order.order_number} placed successfully!")
                
                if order.customer_email and email_success:
                    success_parts.append(f"Confirmation sent to email: {order.customer_email}")
                elif order.customer_email and not email_success:
                    success_parts.append("Email not sent, please check spam folder.")
                
                success_parts.append("We've sent confirmation message to your phone.")
            
            success_msg = " ".join(success_parts)
            messages.success(request, success_msg)
            
            return render(request, 'orders/order_success.html', {
                'order': order,
                'current_language': current_language,
                'cart_items_count': 0,
                'email_sent': email_success,
                'admin_email_sent': admin_email_success,
            })
            
        except Exception as e:
            print(f"Order placement error: {e}")
            error_msg = (
                f"Error placing order: {str(e)}"
                if current_language != 'sw' else
                f"Hitilafu katika kuweka oda: {str(e)}"
            )
            messages.error(request, error_msg)
            return redirect('checkout')
    
    # GET request - redirect to checkout
    return redirect('checkout')


def send_order_notifications(order, cart_items, language='en'):
    """Send SMS and WhatsApp notifications"""
    try:
        # Compose messages based on language
        if language == 'sw':
            # Swahili messages
            customer_sms = (
                f"Ahsante {order.customer_name}!\n"
                f"Oda #{order.order_number} imepokelewa.\n"
                f"Jumla: TZS {order.total_amount:,.0f}\n"
                f"Njia ya malipo: {order.get_payment_method_display()}\n"
                f"Tutaungana nawe hivi punde."
            )
            
            customer_whatsapp = (
                f"*AMBERTEK EXPORT*\n\n"
                f"*Oda Mpya Imewekwa!*\n"
                f"-------------------\n"
                f"*Nambari ya Oda:* {order.order_number}\n"
                f"*Mteja:* {order.customer_name}\n"
                f"*Simu:* {order.customer_phone}\n"
                f"*Anwani:* {order.customer_address}\n"
                f"*Jumla:* TZS {order.total_amount:,.0f}\n"
                f"*Njia ya Malipo:* {order.get_payment_method_display()}\n\n"
                f"*Bidhaa:*\n"
            )
            
            admin_sms = (
                f"Oda Mpya!\n"
                f"Nambari: {order.order_number}\n"
                f"Mteja: {order.customer_name}\n"
                f"Simu: {order.customer_phone}\n"
                f"Jumla: TZS {order.total_amount:,.0f}"
            )
            
        else:
            # English messages
            customer_sms = (
                f"Thank you {order.customer_name}!\n"
                f"Order #{order.order_number} received.\n"
                f"Total: TZS {order.total_amount:,.0f}\n"
                f"Payment: {order.get_payment_method_display()}\n"
                f"We'll contact you shortly."
            )
            
            customer_whatsapp = (
                f"*AMBERTEK EXPORT*\n\n"
                f"*New Order Placed!*\n"
                f"-------------------\n"
                f"*Order No:* {order.order_number}\n"
                f"*Customer:* {order.customer_name}\n"
                f"*Phone:* {order.customer_phone}\n"
                f"*Address:* {order.customer_address}\n"
                f"*Total:* TZS {order.total_amount:,.0f}\n"
                f"*Payment Method:* {order.get_payment_method_display()}\n\n"
                f"*Items:*\n"
            )
            
            admin_sms = (
                f"New Order!\n"
                f"Order #: {order.order_number}\n"
                f"Customer: {order.customer_name}\n"
                f"Phone: {order.customer_phone}\n"
                f"Total: TZS {order.total_amount:,.0f}"
            )
        
        # Add items to WhatsApp message
        for product_id, item in cart_items.items():
            try:
                product = Product.objects.get(id=int(product_id))
                if language == 'sw':
                    customer_whatsapp += f"• {product.name} x{item['quantity']} - TZS {product.price * item['quantity']:,.0f}\n"
                else:
                    customer_whatsapp += f"• {product.name} x{item['quantity']} - TZS {product.price * item['quantity']:,.0f}\n"
            except (Product.DoesNotExist, ValueError):
                pass
        
        customer_whatsapp += f"\n*Grand Total: TZS {order.total_amount:,.0f}*"
        
        # In production, you would integrate with SMS/WhatsApp APIs here
        # For now, we'll just print to console and update the model
        
        print("\n" + "="*50)
        print("SMS TO CUSTOMER:")
        print(customer_sms)
        print("\nWHATSAPP TO CUSTOMER:")
        print(customer_whatsapp)
        print("\nSMS TO ADMIN:")
        print(admin_sms)
        print("="*50 + "\n")
        
        # Update notification status
        order.sms_sent = True
        order.whatsapp_sent = True
        order.customer_notified = True
        order.admin_notified = True
        order.save()
        
        return True
        
    except Exception as e:
        print(f"Error sending notifications: {e}")
        return False

def order_success(request, order_id):
    """Order success page"""
    current_language = request.session.get('ambertek_language') or request.COOKIES.get('ambertek_language', 'en')
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
        'current_language': current_language,
        'cart_items_count': 0,
    }
    return render(request, 'orders/order_success.html', context)

    # Add these functions to your existing orders/views.py

def checkout(request):
    """Display checkout form"""
    current_language = request.session.get('ambertek_language') or 'en'
    
    # Get cart from session
    cart_items = request.session.get('cart', {})
    
    if not cart_items:
        messages.warning(request, 
            "Your cart is empty" if current_language != 'sw' else "Carti yako ni tupu"
        )
        return redirect('cart_detail')
    
    # Calculate cart total
    cart_total = 0
    items_list = []
    for product_id, item in cart_items.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * item['quantity']
            cart_total += item_total
            items_list.append({
                'product': product,
                'quantity': item['quantity'],
                'item_total': item_total
            })
        except (Product.DoesNotExist, ValueError):
            pass
    
    context = {
        'current_language': current_language,
        'cart_items': items_list,
        'cart_total': cart_total,
        'cart_items_count': len(cart_items),
    }
    
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_id):
    """Order confirmation page"""
    current_language = request.session.get('ambertek_language') or 'en'
    
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
            'current_language': current_language,
            'cart_items_count': 0,
        }
        
        return render(request, 'orders/confirmation.html', context)
        
    except Order.DoesNotExist:
        messages.error(request, "Order not found")
        return redirect('home')

def order_track(request, order_number):
    """Track order by order number"""
    current_language = request.session.get('ambertek_language') or 'en'
    
    try:
        order = Order.objects.get(order_number=order_number)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
            'current_language': current_language,
            'cart_items_count': 0,
        }
        
        return render(request, 'orders/track.html', context)
        
    except Order.DoesNotExist:
        messages.error(request, 
            f"Order #{order_number} not found" if current_language != 'sw' 
            else f"Oda #{order_number} haipatikani"
        )
        return redirect('home')