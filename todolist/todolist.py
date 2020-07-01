# potrzebne do stworzenia engine
from sqlalchemy import create_engine

# potrzebne do tworzenia tabeli
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

# tworzenie obiektów daty
from datetime import datetime, timedelta

# potrzebne do tworzenia sesji (łączenia sie z bazą)
from sqlalchemy.orm import sessionmaker

# Write your code here

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# spawnowanie modelu bazy
Base = declarative_base()


# tworzenie tabeli dziedziczącej z modelu bazy
class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    # debug klasy
    def __repr__(self):
        return self.task


# tworzenie tabeli w bazie
Base.metadata.create_all(engine)

# tworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()


def show_tasks(ilosc_dni=1):
    # Legenda:
    # -1 = przegapione zadania
    #  0 = wszystkie zadania
    #  1 = dzisiejsze zadania
    # >1 = dłuższy okres

    today = datetime.today().date()

    if ilosc_dni == 0:
        rows = session.query(Table).order_by(Table.deadline.asc()).all()
        print("All tasks:")
        for i in range(len(rows)):
            data = rows[i].deadline
            print(str(i + 1) + ".", str(rows[i]) + ".", data.strftime('%d %b'))
    elif ilosc_dni == 1:
        rows = session.query(Table).filter(Table.deadline == today).all()
        print("Today", today.day, today.strftime('%b'), ":")
        if len(rows) > 0:
            for i in range(len(rows)):
                print(str(i + 1) + ".", rows[i])
        else:
            print("Nothing to do!")
    elif ilosc_dni == -1:
        print("Missed tasks:")
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline.asc()).all()
        for i in range(len(rows)):
            data = rows[i].deadline
            print(str(i + 1) + ".", str(rows[i]) + ".", data.strftime('%d %b'))
    else:
        for i in range(ilosc_dni):
            current_day = today + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == current_day).all()
            print(current_day.strftime('%A'), current_day.day, current_day.strftime('%b') + ":")
            if len(rows) > 0:
                for j in range(len(rows)):
                    print(str(j + 1) + ".", rows[j])
            else:
                print("Nothing to do!")
            print()
    # for i in range(len(tasks)):
    #     print(str(i + 1) + ")", tasks[i])


def add_task():
    print("Enter task")
    zadanie = input()
    print("Enter deadline")
    koniec = datetime.strptime(input(), '%Y-%m-%d').date()
    session.add(Table(task=zadanie, deadline=koniec))
    session.commit()
    print("The task has been added!")


def delete_task():
    rows = session.query(Table).order_by(Table.deadline.asc()).all()
    print("Chose the number of the task you want to delete:")
    for i in range(len(rows)):
        data = rows[i].deadline
        print(str(i + 1) + ".", str(rows[i]) + ".", data.strftime('%d %b'))
    row_to_delete = int(input()) - 1
    session.delete(rows[row_to_delete])
    session.commit()
    print("The task has been deleted!")


prompt = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
"""
wybrana_opcja = input(prompt)

while wybrana_opcja != "0":
    print()
    if wybrana_opcja == "1":
        show_tasks()
    elif wybrana_opcja == "2":
        show_tasks(7)
    elif wybrana_opcja == "3":
        show_tasks(0)
    elif wybrana_opcja == "4":
        show_tasks(-1)
    elif wybrana_opcja == "5":
        add_task()
    elif wybrana_opcja == "6":
        delete_task()

    wybrana_opcja = input(prompt)

print()
print("Bye!")
