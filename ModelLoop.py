import random
import pprint
from unittest import case
import matplotlib.pyplot as plt

class ModelLoopInteractive():
    def __init__(self, person_list: list, company_list: list):
        self.person_list = person_list
        self.company_list = company_list
        self.agents = self.person_list + self.company_list 
        self.id_counter = self._create_id_generator()

    def _create_id_generator(self):
        i = 100
        while True:
            yield i
            i += 1

    def get_next_id(self):
        return next(self.id_counter)
    
    def step(self):
        random.shuffle(self.person_list)
        random.shuffle(self.company_list)
        bakeries = [c for c in self.company_list if c.type == "bakery"]
        farms = [c for c in self.company_list if c.type == "farm"]

        for company in farms:
            company.produce()

        for company in bakeries:
            company.buy_grain(self)
            company.produce()

        for person in self.person_list:
            person.buy_bread(self)
            person.try_finding_better_job(self)

        for company in self.company_list:
            company.pay_wages()
            company.adjust_wages(self)
            company.asses_production(self)
            company.check_for_bankruptcy(self)
        
        for person in self.person_list:
            person.maybe_start_company(self)

    def run(self):
        t = 0
        print("Model interaktywny. komendy Enter, i, addp, addc, q")
        
        while True:
            cmd = input(f"[Tura {t}] > ").strip().lower()
            match cmd:
                case "":
                    print("TURA: ", t)
                    self.step()
                    t += 1
                case "q":
                    print("Koniec symulacji.")
                    break
                case "i":
                    print("Osoby:")
                    for p in self.person_list:
                        print(f"  Person {p.id}: wealth={p.wealth}, employed={p.employed}, company={p.my_company.id if p.my_company else None}, looking_for_job={p.looking_for_job}, companies_potential_switch={[c.id for c in p.companies_potential_switch]}")
                    print("Firmy:")
                    for c in self.company_list:
                        print(f"  Company {c.id}: type={c.type}, capital={c.capital}, price={c.price}, wage={c.current_pay}, stockpile={c.product_stockpile}, workers={[w.id for w in c.workers]}")
                case "addp":
                    input_str = input("Please provide the amount of money: ")
                    try:
                        amount = int(input_str)
                        if amount < 0:
                            print("Warning: Taking money away from people!")
                        
                        for p in self.person_list:
                            p.wealth += amount
                        print(f"Added {amount} wealth to {len(self.person_list)} people.")
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")