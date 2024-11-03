from argparse import ArgumentParser, Namespace
import database
from datetime import datetime


def add_expense(args: Namespace) -> None:
    try:
        expense_id = database.add_entry(
            {
                "description": args.description,
                "amount": args.amount,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "updated": None,
            }
        )
        print(f"Expense added successfully (ID: {expense_id})")
    except Exception as e:
        print(f"Failed to add expense: {e}")


def update_expense(args: Namespace) -> None:
    expenses = database.load_database()

    for expense in expenses["expenses"]:
        if expense["expense_id"] == args.id:
            if not args.description and not args.amount:
                print("Please pass either --description or --amount or both")
                return

            if args.description:
                expense["description"] = args.description
            if args.amount:
                expense["amount"] = args.amount

            expense["updated"] = datetime.now().strftime("%Y-%m-%d")

    database.update_database(expenses)
    print(f"Expense updated successfully (ID: {args.id})")


def delete_expense(args: Namespace) -> None:
    try:
        database.delete_entry(args.id)
        print(f"Expense deleted successfully (ID: {args.id})")
    except IndexError:
        print(f"(ID: {args.id}) does not exist")


def list_expenses(args: Namespace) -> None:
    expenses = database.load_database()

    print("ID Date Updated Description Amount")
    for expense in expenses["expenses"]:
        print(
            f"{expense["expense_id"]} {expense["date"]} {expense["updated"]} {expense["description"]} {expense["amount"]}"
        )


def summarize_expenses(args: Namespace) -> None:
    expenses = database.load_database()["expenses"]
    total_expenses = 0

    if args.month:
        for expense in expenses:
            if int(expense["date"].split("-")[1]) == args.month:
                total_expenses += expense["amount"]
    else:
        for expense in expenses:
            total_expenses += expense["amount"]

    print(f"Total expenses: ${total_expenses:,.2f}")


parser = ArgumentParser(
    prog="ExpenseTracker",
    description="Tracks expenses",
    epilog="meow idk",
)
subparsers = parser.add_subparsers(
    title="Commands", description="Available commands", dest="command"
)

# add
parser_add = subparsers.add_parser("add", help="Add a new expense")
parser_add.add_argument(
    "-d", "--description", help="Description of the expense", type=str, required=True
)
parser_add.add_argument(
    "-a", "--amount", help="How much the expense costs", type=float, required=True
)
parser_add.set_defaults(function=add_expense)


# update
parser_update = subparsers.add_parser("update", help="Update an expense")
parser_update.add_argument(
    "-i", "--id", help="ID of the expense", type=int, required=True
)
parser_update.add_argument(
    "-d", "--description", help="Description of the expense", type=str
)
parser_update.add_argument(
    "-a", "--amount", help="How much the expense costs", type=float
)
parser_update.set_defaults(function=update_expense)

# delete
parser_delete = subparsers.add_parser("delete", help="Delete an expense")
parser_delete.add_argument(
    "-i", "--id", help="ID of the expense", type=int, required=True
)
parser_delete.set_defaults(function=delete_expense)


# list
parser_list = subparsers.add_parser("list", help="List all expenses")
parser_list.set_defaults(function=list_expenses)

# summary
parser_summary = subparsers.add_parser("summary", help="Show total expenses")
parser_summary.add_argument("-m", "--month", help="Month of the expenses", type=int)
parser_summary.set_defaults(function=summarize_expenses)

args: Namespace = parser.parse_args()

if args.command:
    args.function(args)
else:
    parser.print_help()
