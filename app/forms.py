from bitcoinaddress import validate

class RequestForm():

    def __init__(self, destination, amount, multiple=None):
        self.errors = {}
        if destination is None:
            self.errors['destination'] = "Please enter a valid Bitcoin Address"
            
        elif len(destination) > 35 or len(destination) < 26:
            self.errors['destination'] = "Please enter a valid Bitcoin Address"
            
        else:
            try:
                if not validate(destination):
                    self.errors['destination'] = "Please enter a valid Bitcoin Address"
            except Exception as error:
                print(error)
                self.errors['destination'] = "Please enter a valid Bitcoin address"

        try:
            self.amount = float(amount)
        except:
            self.errors['amount'] = "Please enter a number!"
            self.amount = 0

        if self.amount > 1 or self.amount < 0.01:
            self.errors['amount'] = "Please enter a valid amount!"
        
        self.destination = destination
        self.amount = amount
        self.multiple = multiple

        
                          
