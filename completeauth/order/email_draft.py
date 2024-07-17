
def email_draft_create(id, items, amt):
    body = f'''
Dear Sir/Ma'am,

Thank you for choosing our online store! 🎉 We’ve received your order, and our team is already hard at work preparing it for shipment. Here’s a quick summary:
    
Order Details:

1) Order Person name: {id}
2) Items: {items}  
3) Total Amount: {amt}

What’s Next?

Order Processing: Our elves (well, not really, but close!) are carefully picking and packing your items.
Quality Check: We’ll ensure that everything meets our high standards.
Shipping: Soon, your order will be on its way to your doorstep.
Delivery: Keep an eye on your inbox for tracking updates. Your goodies are coming!
Estimated Delivery Date: [Provide an estimated delivery timeframe based on your shipping policies.]

If you have any questions or need assistance, feel free to reply to this email or contact our friendly customer support team at [Customer Support Email or Phone Number].

Once again, thank you for shopping with us! We appreciate your trust in our products and services. 🙏

Happy shopping, and stay excited for your upcoming delivery! 🚚✨

Warm regards,

Product-Pulse Customer Support Team
'''

    return body

def email_draft_delete(id, name, amt):
    body = f'''
Dear Sir/Ma'am,

Your Order of following details has been deleted please verify
    
Order Details:

1) Order Person name: {id}
2) Items: {name}  
3) Total Amount: {amt}

If it has not been deleted by you then kindly change the password and report it to us.

Warm regards,

Product-Pulse Customer Support Team
'''

    return body
