from abc import ABC, abstractmethod

class User(ABC):
    """
    Base Class for Technicians, Residents, and Admins:

    Name: First and last name separated by a space
    ID: Numerical number, 8 digits long
    History: Stores history of associated ticket ID's
    """
    def __init__(self, name, id, phone_number, email):
        self.name = name
        self.id = id
        self.phone_number = phone_number
        self.email = email

class person(User):
    def __init__():
        super(person, self).__init__()

        




class Technician:
    """
        Technician Class:

        Name: Technician first and last name separated by a space
        ID: Numerical employment number, 8 digits long
        Credentials: List of degrees or certifications
        History: Stores ticket ID's of previous assignments
        Salary: Monthly pay in USD
        Bonus: Monthly bonus in USd
    """
    def __init__(self, name, tech_id, credentials=None, salary=None):
        self.name = name
        self.id = tech_id
        self.phone_number = phone_number
        self.email = email


        self.credentials = credentials
        self.history = []
        self.salary = salary
        self.bonus = None



    def bonus(self, bonus):
        self.bonus = bonus

    def (self, ):


class Customer:
    """
        Customer Class
    """
    def __init__(self, customer_id, status=None):
        self.id = customer_id
        self.status = status


class Ticket:
    """
        Ticket Class holds customer id, ticket id,  and assigned technician id.
    """

    def __init__(self, customer_id, ticket_id, location, tech_id=None, status=None):
        self.customer_id = customer_id
        self.ticket_id = ticket_id
        self.location = location
        self.tech_id = tech_id
        self.status = status

