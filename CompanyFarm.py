import random
from SuperCompany import Company

class CompanyFarm(Company):
    def __init__(self, id, founder):
        super().__init__(id, founder)
        self.type = "farm"
        self.price = 400 #random.randint(280, 330)
        self.current_pay = 2200 #tymczasowe

    def produce(self):
        self.potential_production = len(self.workers) * 10
        self.product_stockpile = len(self.workers) * 10
        print(f"Company {self.id} produced {self.product_stockpile} grain at price {self.price}.")