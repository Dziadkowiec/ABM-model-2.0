import random

class Company():
    def __init__(self, id, founder):
        self.id = id
        self.founder = founder
        self.workers = [founder]

        self.capital = 25000
        self.current_pay = 2000
        self.payroll = {}

        self.potential_production = 0
        self.product_stockpile = 0

    def produce(self):
        pass

    def debug_hire_specific_worker(self, worker):
        worker.employed = True
        worker.my_company = self
        self.workers.append(worker)
        self.payroll[worker] = self.current_pay
    
    def fire_specific_worker(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
        self.payroll.pop(worker, None)
        worker.employed = False
        worker.my_company = None
        print(f"Company {self.id} fired Worker {worker.id} specifically due to budget cuts.")

    def asses_production(self, model):
        if self.product_stockpile == 0:
            self.price *= 1.01
            self.hire_worker(model)
        else:
            self.price *= 0.99
            self.fire_worker()

    def hire_worker(self, model):
        ppl_willing_to_work_here = [p for p in model.person_list if p.looking_for_job == True and self in p.companies_potential_switch]
        if ppl_willing_to_work_here:
            new_worker = random.choice(ppl_willing_to_work_here)
            if new_worker.employed == False:
                new_worker.employed = True
                self.workers.append(new_worker)
                new_worker.my_company = self
                self.payroll[new_worker] = self.current_pay
                print(f"Company {self.id} hired Person {new_worker.id}.")
            else:
                new_worker.my_company.workers.remove(new_worker)
                new_worker.employed = True
                self.workers.append(new_worker)
                new_worker.my_company = self
                self.payroll[new_worker] = self.current_pay
                print(f"Company {self.id} hired Person {new_worker.id}.")

    def fire_worker(self):
        if len(self.workers) > 1:
            candidates_to_fire = [w for w in self.workers if w != self.founder]
            if candidates_to_fire:
                fired_worker = random.choice(candidates_to_fire)
                fired_worker.employed = False
                self.workers.remove(fired_worker)
                self.payroll.pop(fired_worker, None)
                print(f"Company {self.id} fired Person {fired_worker.id}.")

    def pay_wages(self):
        if self.capital >= self.current_pay:
            self.founder.wealth += self.current_pay
            self.capital -= self.current_pay
            print(f"Company {self.id} paid wage to Founder {self.founder.id}. Remaining capital: {self.capital}.")
        random.shuffle(self.workers)
        if self.payroll:
            for worker, wage in list(self.payroll.items()):
                if self.capital >= wage:
                    worker.wealth += wage
                    self.capital -= wage
                    print(f"Company {self.id} paid wage to Worker {worker.id}. Remaining capital: {self.capital}.")
                else:
                    self.fire_specific_worker(worker)
                    print(f"Company {self.id} cannot pay wage to Worker {worker.id} due to insufficient capital.")

    def check_for_bankruptcy(self, model):
        if self.capital < self.current_pay and len(self.workers) == 1: 
            print(f"Company {self.id} has gone bankrupt!")
            self.workers = []
            self.founder.my_company = None
            self.founder.employed = False
            model.company_list.remove(self)
            
    def adjust_wages(self, model):
        ppl_willing_to_work_here = [p for p in model.person_list if p.looking_for_job == True and self in p.companies_potential_switch]
        if self.product_stockpile == 0 and not ppl_willing_to_work_here:
            print(f"Company {self.id} sold all products and no potential workers. Increasing wages.")
            self.current_pay *= 1.01