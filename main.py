import random


class agent:
    def __init__(self) -> None:
        self.money = 0
        self.state = {}

    def see(self, env_state):
        self.state = env_state

    def action(self):
        p = random.random()

        if p < 10:  # compra
            amount = int(random.random() * 1000)
            price: float = (
                self.env_state["current_price"] + random.random() * 20
            )  # acepta hasta 20 pesos por encima del precio

            while amount > 0:
                min_sell: oferta = self.env_state["sell"][0]
                min_sell_index = 0
                for i, sell in enumerate(self.env_state["sell"]):
                    if sell.price < min_sell.price:
                        min_sell = sell
                        min_sell_index = i

                if min_sell.price <= price:
                    if min_sell.amount >= amount:
                        min_sell.amount -= amount
                        self.env_state["sell"].removeat(
                            min_sell_index
                        )  # ver como eliminar esto en python
                    else:
                        min_sell.amount -= amount
                        amount = 0
                else:
                    break # ver como comprar otro dia
        
        elif p < 50 and self.money > 0:  # compra con 40 %
            amount = random.random() * self.money
            price: float = (
                self.env_state["current_price"] + random.random() * 20
            )  # acepta hasta 20 pesos por debajo del precio

            while amount > 0:
                max_buy: oferta = self.env_state["buy"][0]
                max_buy_index = 0
                for i, buy in enumerate(self.env_state["buy"]):
                    if buy.price > max_buy.price:
                        max_buy = buy
                        max_buy_index = i

                if max_buy.price >= price:
                    if max_buy.amount >= amount:
                        max_buy.amount -= amount 
                        self.env_state["buy"].removeat(
                            max_buy_index
                        )  # ver como eliminar esto en python
                    else:
                        max_buy.amount -= amount
                        amount = 0
                else:
                    break # ver como comprar otro dia
        


class oferta:  # poner en ingles
    def __init__(self, price, amount) -> None:
        self.price = price
        self.amount = amount


class environment:
    def __init__(self, people_count, days) -> None:
        self.agents = [agent() for i in range(people_count)]
        self.state = {"current_price": 0, "sell": [], "buy": []}

        self.run_simulation(days)

    def calc_current_price(self):  # por ahora el precio será solo la media
        mean = 0

        for oferta in self.state["sell"] + self.state["buy"]:
            mean += oferta.price

        return mean / len(self.state["sell"] + self.state["buy"])

    def run_simulation(self, days):
        for i in range(days):
            for agent in self.agents:
                agent.see(self.state)
                agent.action()

            self.state["current_price"] = self.calc_current_price()
