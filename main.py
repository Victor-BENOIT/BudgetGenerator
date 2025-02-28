# Objectif : Créer un budget mensuel et pouvoir y ajouter des investissements en fonction du % de ce qui reste
# Lien du Sankey Diagram : https://sankeymatic.com/build/


import string
from enum import Enum

class BudgetTypeEnum(Enum):
    INCOME = 1
    EXPENSE = 2
    INVESTMENT = 3


class Budget:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self.investments = 0
        self.balance = 0
        self.register = {}
        self.register_name = "mon_budget.txt"
        self.colors = {
            "Loyer": "#d94", "Electricité": "#d94", "Courses": "#137",
            "Cantine": "#137", "Box Wifi": "#959", "Abo Spotify": "#959",
            "Abo Téléphone": "#959", "Argent de poche": "#d44", "Salaire": "#d44",
            "Budget": "#d64", "Matelas de sécurité": "#197", "ETF S&P 500": "#197", "ETF Nasdaq 100": "#197",
            "Bitcoin": "#197", "Ethereum": "#197"
        }

    def __str__(self):
        return f"Revenus: {self.income}€\nDépenses: {self.expenses}€\nInvestissements: {self.investments}€"

    def update_balance(self):
        self.balance = self.income - self.expenses

    def add_income(self, name: string, value: int):
        self.income += value
        self.add_in_register(name, value, BudgetTypeEnum.INCOME)
        self.update_balance()

    def add_expense(self, name: string, value: int):
        self.expenses += value
        self.add_in_register(name, value, BudgetTypeEnum.EXPENSE)
        self.update_balance()


    def add_investment(self, name: string, value: int = 0, percentage: int = 0):
        if self.balance <= 0:
            no_more_money = f"Vous n'avez plus d'argent à investir : votre balance est de {self.balance}€."
            raise Exception(no_more_money)
        elif value and percentage:
            wrong_call = f"Choisissez soit une somme soit un pourcentage à investir parmi votre balance."
            raise Exception(wrong_call)
        else:
            if value:
                self.investments += value
                self.add_in_register(name, value, BudgetTypeEnum.INVESTMENT)
            elif percentage:
                self.investments += int(percentage / 100 * self.balance)
                self.add_in_register(name, int(percentage / 100 * self.balance), BudgetTypeEnum.INVESTMENT)


    def add_in_register(self, name: string, value: int, type: BudgetTypeEnum):
        if name in self.register:
            self.register[name].append((type.name, value))
        else:
            self.register[name] = [(type.name, value)]

    def export_to_file(self):
        with open(self.register_name, "w", encoding="utf-8") as file:
            # Écriture des revenus
            file.write(f"// Revenus : {self.income}€\n")
            for name, transactions in self.register.items():
                for t_type, value in transactions:
                    if t_type == "INCOME":
                        file.write(f"{name} [{value}] Budget\n")
            file.write("\n")

            # Écriture des dépenses
            file.write(f"// Dépenses : {self.expenses}€\n")
            for name, transactions in self.register.items():
                for t_type, value in transactions:
                    if t_type == "EXPENSE":
                        file.write(f"Budget [{value}] {name}\n")
            file.write("\n")

            # Écriture des investissements
            file.write(f"// Investissements : {self.investments}€\n")
            for name, transactions in self.register.items():
                for t_type, value in transactions:
                    if t_type == "INVESTMENT":
                        file.write(f"Budget [{value}] {name}\n")
            file.write("\n")

            # Définition des couleurs


            # Écriture des couleurs
            for name in self.colors:
                file.write(f":{name} {self.colors[name]}\n")


if __name__ == "__main__":
    bdg = Budget()

    # MES REVENUS
    bdg.add_income("Salaire", 1500)
    bdg.add_income("Argent de poche", 215)

    # MES DEPENSES
    bdg.add_expense("Loyer", 540)
    bdg.add_expense("Electricité", 70)
    bdg.add_expense("Courses", 150)
    bdg.add_expense("Cantine", 90)
    bdg.add_expense("Box Wifi", 23)
    bdg.add_expense("Abo Spotify", 7)
    bdg.add_expense("Abo Téléphone", 7)
    bdg.add_expense("Achats non essentiels", 200)

    # MES INVESTISSEMENTS
    bdg.add_investment(name="ETF S&P 500", percentage=45)
    bdg.add_investment(name="ETF Nasdaq 100", percentage=30)
    bdg.add_investment(name="Bitcoin", percentage=13)
    bdg.add_investment(name="Ethereum", percentage=2)
    bdg.add_investment(name="Matelas de sécurité", percentage=10)

    bdg.export_to_file()
    print(bdg)


