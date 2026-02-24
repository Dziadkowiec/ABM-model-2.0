import random
from SuperCompany import Company

class CompanyBakery(Company):
    def __init__(self, id, founder):
        super().__init__(id, founder)
        self.type = "bakery"
        self.price = 1000 #random.randint(500, 600)
        self.grains_stockpile = 0

    def calculate_potential_production(self):
        return len(self.workers) * 10
    
    def buy_grain(self, model):
        farms = [c for c in model.company_list if c.type == "farm"]
        farms_sorted = sorted(farms, key=lambda c: c.price)
        total_bought = 0
        self.potential_production = self.calculate_potential_production()
        print(f"Company {self.id} is demanding {self.potential_production} grain.")
        
        for farm in farms_sorted:
            if total_bought >= self.potential_production:
                break
            bought_here = 0
            for _ in range(self.potential_production - total_bought):
                if self.capital >= farm.price and farm.product_stockpile > 0:
                    self.capital -= farm.price
                    self.grains_stockpile += 1
                    farm.capital += farm.price
                    farm.product_stockpile -= 1
                    bought_here += 1
                    total_bought += 1
                else:
                    break
            if bought_here > 0:
                print(f"Company {self.id} bought {bought_here} grain from Company {farm.id}. Remaining capital: {self.capital}.")

    def produce(self):
        if self.grains_stockpile != 0:
            grain_used = min(self.grains_stockpile, self.potential_production)
            self.grains_stockpile -= grain_used
            self.product_stockpile = min(len(self.workers) * 10, grain_used)
            self.potential_production = len(self.workers) * 10
            print(f"Company {self.id} produced {self.product_stockpile} bread at price {self.price}.")
        else:
            print(f"Company {self.id} has no grain to produce bread.")

    def asses_production(self, model):
        if self.product_stockpile == 0:
            self.price *= 1.01
            self.hire_worker(model)
        elif self.product_stockpile > 0 and self.grains_stockpile == 0:
             self.fire_worker()
        else:
            self.price *= 0.99
            self.fire_worker()