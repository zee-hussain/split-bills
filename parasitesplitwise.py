import os
from distutils import errors
from splitwise import Splitwise
from splitwise.expense import Expense

sObj = Splitwise(os.environ['SW_CONSUMER_KEY'],os.environ['SW_CONSUMER_SECRET'],api_key=os.environ['SW_API_KEY'])

def getParasiteExpenses():
    parasiteExpenses = []
    allExpenses = sObj.getExpenses()
    for i in range(0, len(allExpenses)):
        groupId = allExpenses[i].getGroupId()
        if groupId == 19337393:
            parasiteExpenses.append(allExpenses[i].getDetails())
    return parasiteExpenses

def createParasiteExpense(cost: str, name: str, notes: str):
    expense = Expense()
    expense.setCost(cost)
    expense.setGroupId(19337393)
    expense.setDescription(name)
    expense.setSplitEqually()
    expense.setDetails(notes)
    expense, errors = sObj.createExpense(expense)
