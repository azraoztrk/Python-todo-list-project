import sqlite3

deleted_duty_stack = []

def connect_db():
    return sqlite3.connect("duties.db")

def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS duties(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duty TEXT NOT NULL,
        done TEXT NOT NULL                     
)
""")

def show_menu():
    print('1-Add Duty')
    print('2-List Duty')
    print('3-Delete Duty')
    print("4-Mark Duty Done")
    print(f'5-Undelete The Last Deleted Duty. ({len(deleted_duty_stack)} available)')
    print("6-Exit")

def add_duty(cursor, conn):
    get_text = input('Enter a duty: ')
    cursor.execute("""INSERT INTO duties (duty, done) VALUES (?, ?)""", (get_text, "Not Done"))
    conn.commit()
    print('Duty Added Successfuly!\n')

def list_duty(cursor):
    cursor.execute("SELECT id, duty, done FROM duties")
    duties = cursor.fetchall()

    if not duties:
        print("Please add a duty first!\n")
    else:
        for duty in duties:
            print(f"{duty[0]}: {duty[1]} - {duty[2]}\n")
        print("\n")

def delete_duty(cursor, conn):
    try:
        deleteInput = int(input('Enter a duty number to delete: '))
        
        cursor.execute("SELECT duty, done FROM duties WHERE id = ?", (deleteInput,))
        duty = cursor.fetchone()

        if duty is None:
            print("Duty not found.\n")
            return
        
        deleted_duty_stack.append(duty)

        cursor.execute("DELETE FROM duties WHERE id = ?", (deleteInput,))
        conn.commit()
        print('Duty deleted successfuly!\n') 
    except ValueError:
        print("Please enter a valid number!\n")

def undelete_duty(cursor, conn):
    #stack’te tutulan son silinen görevi geri almak için yazıldı.
    if not deleted_duty_stack:
        print("Nothing to undelete.")
        return
    
    duty = deleted_duty_stack.pop()

    cursor.execute("INSERT INTO duties (duty, done) VALUES (?, ?)", (duty[0], duty[1]))
    conn.commit()

    print(f"Restored duty: '{duty[0]}'\n")

def mark_duty_done(cursor, conn):
    try:
        markDoneInput = int(input("Enter the task number to mark as done: "))
        cursor.execute("UPDATE duties SET done = 'Done ✅' WHERE id = ?", (markDoneInput,))
        conn.commit()
        print("Task marked as done!\n")
    except:
        print("Please enter a valid number!\n")

def main():
    conn = connect_db()
    cursor = conn.cursor()
    create_table(cursor)

    while True:
        show_menu()
        try:
            userInput = int(input('Choose one of them(1-6): '))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if userInput == 1:
            add_duty(cursor, conn)

        elif userInput == 2:
            list_duty(cursor)

        elif userInput == 3:
            delete_duty(cursor, conn)

        elif userInput == 4:
            mark_duty_done(cursor, conn)

        elif userInput == 5:
            undelete_duty(cursor, conn)

        elif userInput == 6:
            conn.close()
            print("Goodbye 👋")
            break
        else:
            print("Please choose a valid option!\n")
        
if __name__ == "__main__":
    main()
#Kodumu import edilebilir ve test edilebilir yazmak için if __name__ == "__main__" kullanıyorum.