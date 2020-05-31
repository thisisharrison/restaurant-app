from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from .models import Topping, Size, Category, Crust, MenuItem, OrderItem, Order

# Create your views here.


def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, "orders/login.html", {"message": "Please Login"})
    # else:
    context = {
        "user": request.user,
        "menuItem": MenuItem.objects.all()
    }
    return render(request, "orders/orders.html", context)


def login_view(request):
    if request.method == "GET":
        return render(request, "orders/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def register_view(request):
    if request.method == "GET":
        return render(request, "orders/register.html", {"message": None})
    else:
        first_name = request.POST["first"]
        last_name = request.POST["last"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "orders/register.html", {"message": "Passwords do not match."})
        if not username:
            return render(request, "orders/register.html", {"message": "Missing username."})
        try:
            user = User.objects .get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return render(request, "orders/login.html")
        return render(request, "orders/register.html", {"message": "Username is in use."})


# @login_required
# def order(request):
#     # TO DO

def item_view(request, menuitem_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": "Please Login"})
    try:
        menuitem = MenuItem.objects.get(pk=menuitem_id)
    except MenuItem.DoesNotExist:
        raise Http404("Item does not exist")
    toppings = Topping.objects.exclude(pk=21)
    subtoppings = Topping.objects.filter(pk__in=[3, 10, 4, 21])
    context = {
        "menuitem_id": menuitem.id,
        "name": menuitem.name,
        "category": str(menuitem.category),
        "size": menuitem.size,
        "toppings": toppings,
        "subtoppings": subtoppings}
    return render(request, "orders/items.html", context)


def add_to_cart(request, menuitem_id):
    try:
        menuitem = MenuItem.objects.get(pk=menuitem_id)
    except MenuItem.DoesNotExist:
        raise Http404("Item does not exist")

    chosen = request.POST.getlist("toppings")
    alltops = Topping.objects.all()

    chosenids = []

    for a in alltops:
        for c in chosen:
            if c == a.name:
                chosenids.append(a.id)

    print(chosenids)

    if '1' in menuitem.name and len(chosenids) != 1 or '2' in menuitem.name and len(chosenids) != 2 or '3' in menuitem.name and len(chosenids) != 3 or 'Special' in menuitem.name and len(chosenids) != 6:
        raise Http404("Wrong Topping Amount")
    print(menuitem.category_id)
    if menuitem.category_id == 2:
        price = float(menuitem.price) + 0.5*int(len(chosenids))
    else:
        price = float(menuitem.price)
    newitem = OrderItem.objects.create(
        name=menuitem, amount=len(chosenids), price=price)
    newitem.topping.set(chosenids)
    newitem.save()

    username = request.user
    order = Order.objects.create(username=username, item_order=newitem)
    # order.item_order.add(newitem.id)

    return HttpResponseRedirect(reverse("index"))


def cart_view(request, user):
    # Return view of Orders query by username and unship status
    # get objects of unshipped items from user
    # for each objects, append data to a dict
    # pass dict to context

    if request.method == "GET":
        cartview = []

        history = Order.objects.filter(username=request.user).all()
        cartitems = history.filter(status="PEND")
        olditems = history.exclude(status="PEND").order_by('-ordered_date')

        totalsum = 0
        for item in cartitems:
            customid = item.item_order_id
            nameid = OrderItem.objects.get(pk=customid).name_id
            price = float(OrderItem.objects.get(pk=customid).price)
            name = MenuItem.objects.get(pk=nameid).name
            size = MenuItem.objects.get(pk=nameid).size
            categoryid = MenuItem.objects.get(pk=nameid).category_id
            category = Category.objects.get(pk=categoryid).name
            quantity = int(MenuItem.objects.get(pk=nameid).quantity)
            toppings = OrderItem.objects.get(pk=customid).topping.all()
            a = []
            for topping in toppings:
                a.append(topping.name)
            cartview.append({'customid': customid, 'name': name, 'category': category,
                             'toppings': a, 'quantity': quantity, 'size': size, 'price': price})

            totalsum += price

        totalsum = round(float(totalsum), 2)

        orderhistory = []

        for item in olditems:
            customid = item.item_order_id
            status = item.status
            date = item.ordered_date
            nameid = OrderItem.objects.get(pk=customid).name_id
            name = MenuItem.objects.get(pk=nameid).name
            categoryid = MenuItem.objects.get(pk=nameid).category_id
            category = Category.objects.get(pk=categoryid).name
            size = MenuItem.objects.get(pk=nameid).size
            price = float(OrderItem.objects.get(pk=customid).price)
            quantity = int(MenuItem.objects.get(pk=nameid).quantity)
            toppings = OrderItem.objects.get(pk=customid).topping.all()
            a = []
            for topping in toppings:
                a.append(topping.name)
            orderhistory.append({'date': date, 'customid': customid, 'status': status, 'name': name, 'category': category, 'size': size,
                                 'toppings': a, 'quantity': quantity, 'price': price})

        context = {
            "cartviews": cartview,
            "totalsum": totalsum,
            "user": request.user,
            "orderhistory": orderhistory
        }
        return render(request, "orders/mycart.html", context)
    else:
        if request.POST:
            history = Order.objects.filter(username=request.user).all()
            cartitems = history.filter(status="PEND")
            customids = []
            for item in cartitems:
                customid = item.item_order_id
                customids.append(customid)

            removeid = request.POST

            for ids in customids:
                if str(ids) in removeid:
                    OrderItem.objects.filter(id=ids).delete()
            return HttpResponseRedirect(reverse("mycart", args=[request.user]))


def checkout(request, user):
    # requests method
    # remove object from orderitem db
    # change status on order db
    # chosen = request.POST.getlist("toppings")
    if request.method == "POST":
        history = Order.objects.filter(username=request.user).all()
        cartitems = history.filter(status="PEND").all()
        for item in cartitems:
            item.status = "CONF"
            item.save()
        confitems = history.filter(status="CONF").all()
        totalsum = 0
        cartview = []
        for item in confitems:
            customid = item.item_order_id
            nameid = OrderItem.objects.get(pk=customid).name_id
            name = MenuItem.objects.get(pk=nameid).name
            categoryid = MenuItem.objects.get(pk=nameid).category_id
            category = Category.objects.get(pk=categoryid).name
            price = float(MenuItem.objects.get(pk=nameid).price)
            quantity = int(MenuItem.objects.get(pk=nameid).quantity)
            toppings = OrderItem.objects.get(pk=customid).topping.all()
            a = []
            for topping in toppings:
                a.append(topping.name)
            cartview.append({'customid': customid, 'name': name, 'category': category,
                             'toppings': a, 'quantity': quantity, 'price': price})

            totalsum += price

        name = User.objects.get(username=request.user)
        full_name = name.first_name + ' ' + name.last_name
        email = name.email

        totalsum = round(float(totalsum), 2)

        context = {
            "cartviews": cartview,
            "totalsum": totalsum,
            "user": request.user,
            "full_name": full_name,
            "email": email
        }
        return render(request, "orders/checkout.html", context)


def order(request, user):
    if request.method == "POST":
        history = Order.objects.filter(username=request.user).all()
        confitems = history.filter(status="CONF").all()
        for item in confitems:
            item.status = "PREP"
            item.save()
    return HttpResponseRedirect(reverse("index"))


def manager_view(request):
    # pass all order objects
    # categorized by shipped and unshipped
    if request.method == "GET":
        confirmed = Order.objects.exclude(status="SHIP").exclude(
            status="PEND").order_by('-ordered_date')
        conf_orders = []
        shipped = Order.objects.filter(status="SHIP").order_by('-ordered_date')
        ship_orders = []
        for order in confirmed:
            timestamp = order.ordered_date
            orderid = order.id
            status = order.status
            userid = order.username_id
            user = User.objects.get(pk=userid).first_name + ' ' + \
                User.objects.get(pk=userid).last_name
            mealid = OrderItem.objects.get(pk=order.item_order_id).name_id
            topquery = OrderItem.objects.get(
                pk=order.item_order_id).topping.all()
            toppings = []
            for topping in topquery:
                toppings.append(topping.name)
            meal = MenuItem.objects.get(pk=mealid).name
            price = MenuItem.objects.get(pk=mealid).price
            category = MenuItem.objects.get(pk=mealid).category.name
            order = {'id': orderid, 'status': status, 'time': timestamp, 'user': user, 'meal': meal, 'topping': toppings,
                     'price': price, 'category': category}
            conf_orders.append(order)
        for order in shipped:
            timestamp = order.ordered_date
            orderid = order.id
            status = order.status
            userid = order.username_id
            user = User.objects.get(pk=userid).first_name + ' ' + \
                User.objects.get(pk=userid).last_name
            mealid = OrderItem.objects.get(pk=order.item_order_id).name_id
            topquery = OrderItem.objects.get(
                pk=order.item_order_id).topping.all()
            toppings = []
            for topping in topquery:
                toppings.append(topping.name)
            meal = MenuItem.objects.get(pk=mealid).name
            price = MenuItem.objects.get(pk=mealid).price
            category = MenuItem.objects.get(pk=mealid).category.name
            order = {'id': orderid, 'status': status, 'time': timestamp, 'user': user, 'meal': meal, 'topping': toppings,
                     'price': price, 'category': category}
            ship_orders.append(order)
        status = [
            'preparing',
            'ready',
            'shipped'
        ]
        context = {
            "orders": conf_orders,
            "shipped": ship_orders,
            "statuses": status
        }
        return render(request, "orders/manager.html", context)
    elif request.method == "POST":
        changeid_str = request.POST
        for i in changeid_str:
            changeid_int = i.replace(
                'csrfmiddlewaretokenstatus', '')
        status = request.POST.get("status")
        print(status)
        print(changeid_int)
        # status = request.post["status"]

        order = Order.objects.get(pk=changeid_int)

        if status == "preparing":
            order.status = "PREP"
            order.save()
        elif status == "ready":
            order.status = "READ"
            order.save()
        elif status == "shipped":
            order.status = "SHIP"
            order.save()

        return HttpResponseRedirect("manager")
