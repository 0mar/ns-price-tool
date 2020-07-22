import json
from datetime import datetime, time


class TripInfo:
    def __init__(self, form, raw_price_info):
        self.raw_trip_data = form
        self.departure = self.arrival = self.date = self.time = None
        for attr in ['departure', 'arrival', 'date', 'time']:
            self.__setattr__(attr, self.raw_trip_data[attr])
        self.datetime = datetime.combine(self.date, self.time)
        self.price_info = json.loads(raw_price_info)

    def summary(self):
        return "%s to %s at %s" % (self.departure, self.arrival, self.datetime.strftime("%d-%m-%Y %H:%M"))

    def get(self, class_type, discount_type, product_type):
        if discount_type == 'FREE':  # Not in API but custom added for this engine
            return {'classType': class_type, "discountType": discount_type, "ProductType": product_type,
                    'price': '0'}
        for entry in self.price_info['priceOptions'][1]['totalPrices']:
            if entry['classType'] == class_type \
                    and entry['discountType'] == discount_type \
                    and entry['productType'] == product_type:
                return entry
        raise AttributeError("No price options with class %s, discount %s and product type %s" % (
            class_type, discount_type, product_type))


class BaseSubscriptor:
    name = 'Base'

    def __init__(self):
        self.trips = []
        self._mp_list = []

    def __str__(self):
        """
        Printable representation of the total price
        :return:
        """
        string = "Subscription: %s\nTrips:\n" % self.name
        string += "\n".join([trip.summary() for trip in self.trips])
        string += "\nTotal: %s" % self.euro_repr(self.total_price())
        return string

    def __repr__(self):
        return "%s (%d trips)" % (self.name, len(self.trips))

    def add(self, trip):
        self.trips.append(trip)

    def _duration(self, in_months=False):
        min_date = self.trips[0].datetime
        max_date = self.trips[0].datetime
        for trip in self.trips[1:]:
            if trip.datetime < min_date:
                min_date = trip.datetime
            if trip.datetime > max_date:
                max_date = trip.datetime
        delta = max_date - min_date
        if in_months:
            return int(delta.days / 30) + 1
        else:
            return delta

    def marginal_price(self):
        total = 0
        self._mp_list.clear()
        for trip in self.trips:
            for rule, discount in self.rules.items():
                if rule(trip.datetime):
                    entry = trip.get("SECOND", discount, "SINGLE_FARE")
                    break
            else:
                raise AttributeError("No rule for trip %s" % trip)
            price = float(entry['price']) / 100
            self._mp_list.append(price)
            total += price
        return total

    def marginal_prices(self):
        self.marginal_price()
        return self._mp_list

    def base_price(self):
        return self._duration(in_months=True) * self.base_price_unit

    def total_price(self):
        return self.base_price() + self.marginal_price()

    @staticmethod
    def euro_repr(value):
        return "€%.2f" % value


def is_weekend(trip_dt):
    return trip_dt.weekday() in [5, 6]


def is_dal(trip_dt, weekend_is_dal=True):
    in_morning_jam = time(6, 30) < trip_dt.time() < time(9, 0)
    in_evening_jam = time(16, 0) < trip_dt.time() < time(18, 30)
    return is_weekend(trip_dt) and weekend_is_dal or not (in_morning_jam or in_evening_jam)


def default(_):
    return True


class Basis(BaseSubscriptor):
    name = 'Geen abbonnement'
    base_price_unit = 0
    rules = {default: "NONE"}


class DalVoordeel(BaseSubscriptor):
    name = "Dal Voordeel"
    base_price_unit = 5
    rules = {is_dal: "FORTY_PERCENT", default: "NONE"}


class WeekendVoordeel(BaseSubscriptor):
    name = "Weekend Voordeel"
    base_price_unit = 2
    rules = {is_weekend: "FORTY_PERCENT", default: "NONE"}


class AltijdVoordeel(BaseSubscriptor):
    name = "Altijd Voordeel"
    base_price_unit = 23
    rules = {is_dal: 'FORTY_PERCENT', default: 'TWENTY_PERCENT'}


class DalVrij(BaseSubscriptor):
    name = "Dal vrij"
    base_price_unit = 105
    rules = {is_dal: "FREE", default: "NONE"}


class WeekendVrij(BaseSubscriptor):  # Todo: Add other weekend vrij
    name = "Weekend vrij"
    base_price_unit = 34
    rules = {is_weekend: 'FREE', is_dal: 'FORTY_PERCENT', default: "NONE"}


class AltijdVrij(BaseSubscriptor):
    name = "Altijd Vrij"
    base_price_unit = 351
    rules = {default: 'FREE'}


all_subs = [Basis, DalVoordeel, WeekendVrij, AltijdVoordeel, DalVrij, WeekendVrij, AltijdVrij]
