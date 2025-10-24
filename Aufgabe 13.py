import datetime

tasks = []
task_id_counter = 1


def print_menu():
    print("\n=== Task Manager ===")
    print("1. Neue Aufgabe hinzufügen")
    print("2. Alle Aufgaben anzeigen")
    print("3. Aufgabe Status ändern")
    print("4. Beenden")


def add_task():
    global task_id_counter

    title = input("Aufgabentitel: ").strip()
    if not title:
        print("Fehler: Titel darf nicht leer sein.")
        return

    description = input("Beschreibung (optional): ").strip()

    due_date_input = input("Fälligkeitsdatum ((optional) Format DD-MM-YYYY): ").strip()
    due_date = ""
    if due_date_input:
        try:
            due_date_obj = datetime.datetime.strptime(due_date_input, "%d-%m-%Y")
            due_date = due_date_obj.date().isoformat()
        except ValueError:
            print("Fehler: Das Datum muss im Format DD-MM-YYYY eingegeben werden.")
            return

    priority = input("Priorität ((optional) hoch, mittel, niedrig): ").strip().lower()
    if priority and priority not in ["hoch", "mittel", "niedrig"]:
        print("Fehler: Priorität muss 'hoch', 'mittel' oder 'niedrig' sein.")
        return

    tags = input("Tags (optional): ").strip()
    created_at = datetime.date.today().strftime("%d-%m-%Y")
    status = "offen"

    task = {
        "id": task_id_counter,
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "status": status,
        "tags": [tag.strip() for tag in tags.split(",")] if tags else [],
        "created_at": created_at
    }

    tasks.append(task)
    print(f"Aufgabe #{task_id_counter} wurde hinzugefügt am {created_at}.")
    task_id_counter += 1


def show_tasks():
    if not tasks:
        print("Keine Aufgaben vorhanden.")
        return

    # Spaltenüberschriften
    headers = [
        "ID", "Titel", "Beschreibung", "Fällig am",
        "Priorität", "Status", "Tags", "Erstellt am"
    ]

    # Feste Spaltenbreiten
    column_widths = [5, 20, 30, 12, 10, 15, 25, 12]

    # Kopfzeile
    header_row = ""
    for header, width in zip(headers, column_widths):
        header_row += header.ljust(width)
    print("\n" + header_row)
    print("-" * len(header_row))

    # Aufgabenzeilen
    for task in tasks:
        values = [
            str(task['id']),
            task['title'],
            task['description'],
            task['due_date'] if task['due_date'] else "-",
            task['priority'],
            task['status'],
            ", ".join(task['tags']),
            task['created_at']
        ]

        row = ""
        for value, width in zip(values, column_widths):
            row += value[:width - 1].ljust(width)
        print(row)


def change_task_status():
    if not tasks:
        print("Keine Aufgaben vorhanden.")
        return

    try:
        task_id = int(input("ID der Aufgabe, deren Status geändert werden soll: "))
    except ValueError:
        print("Ungültige Eingabe.")
        return

    for task in tasks:
        if task["id"] == task_id:
            print(f"Aktueller Status: {task['status']}")
            new_status = input("Neuer Status (offen, in Bearbeitung, erledigt, pausiert, abgebrochen): ").strip().lower()
            if new_status in ["offen", "in bearbeitung", "erledigt", "pausiert", "abgebrochen"]:
                task["status"] = new_status
                print("Status aktualisiert.")
            else:
                print("Ungültiger Status.")
            return

    print("Aufgabe mit dieser ID wurde nicht gefunden.")


def main():
    while True:
        print_menu()
        choice = input("Wähle eine Option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            change_task_status()
        elif choice == "4":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte 1-4 wählen.")


if __name__ == "__main__":
    main()
