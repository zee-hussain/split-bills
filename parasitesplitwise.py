from distutils import errors
from os import access
from splitwise import Splitwise
from splitwise.expense import Expense

sObj = Splitwise("","",api_key="")

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
    expense, error = sObj.createExpense(expense)
