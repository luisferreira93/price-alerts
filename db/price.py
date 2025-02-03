from datetime import datetime

class Price:
    def __init__(self, id: str, name: str, category: str, price: str, link: str, 
                 last_discount: str, last_update: str, store: str):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.link = link
        self.last_discount = last_discount
        self.last_update = last_update
        self.store = store

    @property
    def last_discount(self):
        return self._last_discount

    @last_discount.setter
    def last_discount(self, value: str):
        if isinstance(value, str):
            self._last_discount = value
        else:
            raise ValueError("last_discount must be a string.")

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, value: str):
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            self._last_update = value
        except ValueError:
            raise ValueError("last_update must be in the format YYYY-MM-DD HH:MM:SS.")
