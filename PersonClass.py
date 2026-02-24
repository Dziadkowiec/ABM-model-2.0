import numpy as np
import random
from BakeryClass import CompanyBakery
from CompanyFarm import CompanyFarm
class Person:
    def __init__(self, id: int, employed, is_founder, my_company):
        self.id = id
        self.wealth = 40000
        self.employed = employed
        self.is_founder = is_founder
        self.my_company = my_company
        self.bread_needs = 7
        self.looking_for_job = False
        self.companies_potential_switch = []

    def buy_bread(self, model):
        bakeries = [c for c in model.company_list if c.type == "bakery"]
        companies_sorted = sorted(bakeries, key=lambda c: c.price)
        total_bought = 0
        
        for company in companies_sorted:
            if total_bought >= self.bread_needs:
                break
            bought_here = 0
            for _ in range(self.bread_needs - total_bought):
                if self.wealth >= company.price and company.product_stockpile > 0:
                    self.wealth -= company.price
                    company.capital += company.price
                    company.product_stockpile -= 1
                    bought_here += 1
                    total_bought += 1
                else:
                    break
            if bought_here > 0:
                print(f"Person {self.id} bought {bought_here} bread from Company {company.id}. Remaining wealth: {self.wealth}.")

    def try_finding_better_job(self, model):
        self.companies_potential_switch = []
        if self.employed and not self.is_founder:
            companies_by_wage = sorted(model.company_list, key=lambda c: c.current_pay, reverse=True)
            for company in companies_by_wage:
                if company.current_pay > self.my_company.payroll.get(self, 0) and company is not self.my_company:
                    self.companies_potential_switch.append(company)
                    self.looking_for_job = True
        elif not self.employed:
            self.looking_for_job = True
            self.companies_potential_switch = model.company_list.copy()
        else:
            self.looking_for_job = False
            self.companies_potential_switch = []

    def maybe_start_company(self, model):
        if not self.employed and self.wealth > 25000 and np.random.random() < 0.05:
            company_id = model.get_next_id()
            bakeries = [c for c in model.company_list if c.type == "bakery"]
            farms = [c for c in model.company_list if c.type == "farm"]
            if len(bakeries) < len(farms):
                new_company = CompanyBakery(company_id, founder=self)
            else:
                new_company = CompanyFarm(company_id, founder=self)
            self.is_founder = True
            self.employed = True
            self.my_company = new_company
            self.wealth -= 25000
            model.company_list.append(new_company)
            model.agents.append(new_company)

