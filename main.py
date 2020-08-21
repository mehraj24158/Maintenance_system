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

