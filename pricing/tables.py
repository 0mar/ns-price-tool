import django_tables2 as tables
import pricing.subscriptions as sub

class SubscriptionTable(tables.Table):
    name = tables.Column()
    base_price = tables.Column()
    trip_prices = tables.Column()
    total_price = tables.Column()
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        # fields = map(lambda x: x.name, sub.all_subs)
        # fields = ('name', 'base_price', 'trip_prices', 'total')
