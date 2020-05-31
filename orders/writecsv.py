# complete in shell


f = open('orders/pizzamenu.csv')
reader = csv.reader(f)
next(reader)
for row in reader:
    item = MenuItem.objects.create(
        name=row[0], price=row[1], category_id=row[2], size_id=row[3], quantity=row[4], crust_id=row[5])


# delete
w = MenuItem.objects.filter(id__gte=32).all()
for item in w:
    w.delete()
