import datetime

tasks = []
task_id_counter = 1


def print_menu():
    print("\n=== Task Manager ===")
    print("1. Neue Aufgabe hinzufügen")
    print("2. Alle Aufgaben anzeigen")   
    print("3. Aufgabe Status ändern")
    print("4. Beenden")



def _parse_due_date(iso_string):
    """Erwartet YYYY-MM-DD (oder ''/None) und liefert datetime.date oder None."""
    if not iso_string:
        return None
    try:
        return datetime.date.fromisoformat(iso_string)
    except Exception:
        return None


def _priority_rank(p):
    """Kleinere Zahl = höhere Priorität (hoch < mittel < niedrig)."""
    mapping = {"hoch": 0, "mittel": 1, "niedrig": 2}
    return mapping.get(p, 3)


def _sorted_tasks(choice):
    """Gibt eine neue, sortierte Liste der Aufgaben zurück (ändert tasks nicht)."""
    items = list(tasks)

    if choice == "1":  
        items.sort(key=lambda t: (
            _parse_due_date(t["due_date"]) is None,
            _parse_due_date(t["due_date"]) or datetime.date.max,
            t["id"]
        ))
    elif choice == "2":  
        items.sort(key=lambda t: (
            _parse_due_date(t["due_date"]) is None,
            -(_parse_due_date(t["due_date"]) or datetime.date.min).toordinal(),
            t["id"]
        ))
    elif choice == "3":  
        items.sort(key=lambda t: (_priority_rank(t["priority"]), t["id"]))
   
    return items




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


def show_tasks(task_list=None):
    data = task_list if task_list is not None else tasks

    if not data:
        print("Keine Aufgaben vorhanden.")
        return

    headers = [
        "ID", "Titel", "Beschreibung", "Fällig am",
        "Priorität", "Status", "Tags", "Erstellt am"
    ]
    column_widths = [5, 20, 30, 12, 10, 15, 25, 12]

    header_row = "".join(h.ljust(w) for h, w in zip(headers, column_widths))
    print("\n" + header_row)
    print("-" * len(header_row))

    for task in data:
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
        row = "".join((v[:w - 1]).ljust(w) for v, w in zip(values, column_widths))
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
        choice = input("Wähle eine Option: ").strip()

        if choice == "1":
            add_task()

        elif choice == "2":
            if not tasks:
                print("Keine Aufgaben vorhanden.")
                continue

            print("\nSortieren? [Enter = keine]")
            print("1 = Fälligkeitsdatum aufsteigend   |  2 = Fälligkeitsdatum absteigend")
            print("3 = Priorität (hoch → niedrig)")
            sort_choice = input("Auswahl: ").strip()

            if sort_choice in {"1", "2", "3"}:
                sorted_list = _sorted_tasks(sort_choice)
                show_tasks(sorted_list)
            else:
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
