from PersonClass import Person
from BakeryClass import CompanyBakery
from CompanyFarm import CompanyFarm
from ModelLoop import ModelLoopInteractive

#Founder, c1
p1 = Person(1, True, True, None)
c1 = CompanyBakery(10, p1)
p1.my_company = c1
p2 = Person(2, True, False, None)
p3 = Person(3, True, False, None)
c1.debug_hire_specific_worker(p2)
c1.debug_hire_specific_worker(p3)
p4 = Person(4, True, False, None)
p5 = Person(5, True, False, None)

#Founder, c2
p6 = Person(6, True, True, None)
c2 = CompanyFarm(11, p6)
p6.my_company = c2
c2.debug_hire_specific_worker(p4)
c2.debug_hire_specific_worker(p5)
p7 = Person(7, False, False, None)
p8 = Person(8, False, False, None)
p9 = Person(9, False, False, None)
p10 = Person(10, False, False, None)
ModelLoopInteractive([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10], [c1, c2]).run()