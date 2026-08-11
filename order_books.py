class OrderBook:
    def __init__(self):
        self.bids=[]
        self.asks=[]

    def __str__(self):
        return f'bids: {self.bids}, asks: {self.asks}'

    def add_order(self, side, price, quantity):
        if side == "bids":
            self.bids.append({"price": price, "quantity": quantity})
        elif side == "asks":
            self.asks.append({"price": price, "quantity": quantity})
        else:
            raise ValueError("side must be 'bids' or 'asks'")
        
    def sort_book(self):
        self.bids.sort(reverse=True, key=lambda x: x['price'])
        self.asks.sort(reverse=False, key=lambda x: x['price'])

    def get_spread(self):
        self.sort_book()
        return (self.asks[0]['price']-self.bids[0]['price'])

    def execute_market_order(self, side, quantity):

        self.sort_book()

        if side == 'buy':
         choice = self.asks
        elif side == 'sell':
         choice = self.bids

        price = 0

        for i in range(quantity):
            choice[0]['quantity'] -= 1
            price += choice[0]['price']
            if choice[0]['quantity'] == 0:
                choice.pop(0)
            if choice == []:
                return f'ran out of orders to {side}, price: {price}'
            
        return price

    def add_limit_order(self, side, price, quantity):

        self.sort_book()

        if side == 'buy':
            choice = self.asks
            leftovers = 'bids'
        elif side == 'sell':
            choice = self.bids
            leftovers = 'asks'

        cost = 0
        leftover = 0 

        for i in range(quantity):

            if not choice:
                leftover = quantity - i
                break

            if choice[0]['price'] <= price and side == 'buy' or choice[0]['price'] >= price and side == 'sell':
                choice[0]['quantity'] -= 1
                cost += choice[0]['price']
                if choice[0]['quantity'] == 0:
                    choice.pop(0)
                if choice == []:
                    leftover = quantity - i-1
                    break
            else:
                leftover = quantity - i
                break

        if leftover > 0:
            self.add_order(leftovers, price, leftover) 

        self.sort_book() 

        return cost     

class MarketMaker:

    def __init__(self):
        self.cash = 1000
        self.inventory = 0

    def quote(self, book, fair_value, spread, quote_quantity=1):

        skew = 0.5 * self.inventory

        bid_price = fair_value - spread/2 - skew
        ask_price = fair_value + spread/2 - skew

        book.add_limit_order('buy', bid_price, quote_quantity)
        book.add_limit_order('sell', ask_price, quote_quantity)

    def on_fill(self, side, price, quantity):
        if side == 'buy':
            self.inventory += quantity 
            self.cash -= price*quantity
        elif side == 'sell':
            self.inventory -= quantity 
            self.cash += price*quantity
        
