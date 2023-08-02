from . models import *

customers = Customer.object.all()

firstCustomer = Customer.objects.first()

lastCustomer = Customer.objects.last()

order = Order.objects