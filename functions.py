def menu():
    print("*" * 100)
    print("WYBIERZ AKCJE:")
    print("Saldo: 1")
    print("Sprzedaż: 2")
    print("Zakup: 3")
    print("Konto: 4")
    print("Lista: 5")
    print("Magazyn: 6")
    print("Przeglad: 7")
    print("Korekty w magazynie: 8")
    print("Koniec: 9")
    print("*" * 100)


def account_balance_note(account_balance):
    print(f"Obecny stan konta: {round(account_balance,2)} PLN")


def bad_response():
    print("*" * 10)
    print("Blad.")
    print("Sprobuj ponownie.")
    print("*" * 10)


def confirm(user_input):
    user_confirm = True
    while user_confirm:
        print(f"Czy podana wartosc: \"{user_input}\" jest poprawna?")
        print("Tak: Y")
        print("Nie: N")
        confirm_input = (input(": ")).upper()
        if confirm_input == "Y":
            user_confirm = False
            return True
        elif confirm_input == "N":
            user_confirm = True
            return False
        else:
            bad_response()
            user_confirm = True


def history_overview(history):
    if len(history) == 0:
        print("Nie wykonano żadnych operacji.")
    else:
        start = None
        while not isinstance(start, int):
            try:
                print("Podaj początkowy krok przeglądu.")
                print("Wprowadz 0 aby wyswietlić od początku.")
                start = int(input(": "))
                if start < 0:
                    bad_response()
                    start = None
                elif start > len(history):
                    print(
                        f"Bład. Dotychczasowa liczba wykonanych kroków: {len(history)}")
                    start = None
            except ValueError:
                bad_response()
                start = None
        stop = None
        while not isinstance(stop, int):
            try:
                print("Podaj końcowy krok przeglądu.")
                print("Wprowadz 0 aby wyswietlić do końca.")
                stop = int(input(": "))
                if stop < 0:
                    bad_response()
                    stop = None
                elif stop == 0:
                    stop = len(history)
                elif stop < start:
                    print(
                        "Błąd. Krok końcowy nie może być mniejszy niż krok początkowy.")
                    stop = None
                elif stop > len(history):
                    print(
                        f"Bład. Dotychczasowa liczba wykonanych kroków: {len(history)}")
                    stop = None
            except ValueError:
                bad_response()
        if start >= 1:
            start -= 1
        if stop == 0:
            stop = None
        print("*" * 10 + " HISTORIA " + "*" * 10)
        for step, message in enumerate(history[start:stop]):
            print(f"{step + start + 1}.: {message}")
        print("*" * 30)


def decimal_count_check(number, message):
    decimal_count = 3
    while decimal_count > 2:
        number = float(
            input(message).replace(",", "."))
        decimal_count = len(str(number).split(".")[1])
        if decimal_count > 2:
            bad_response()
        else:
            return number


def check_if_number_positive(confirmation_status, number, message):
    if confirmation_status == False:
        return None
    else:
        if number <= 0:
            print(message)
            return None
        else:
            return number


def item_not_in_inventory():
    print("Nie ma takiego przedmiotu w magazynie.")
    print("Czy spróbować ponownie?")
    print("Tak: Y")
    print("Nie: N")
    user_confirm = str(input(": ")).upper()
    if user_confirm == "N":
        return False
    elif user_confirm == "Y":
        return True
    else:
        bad_response()


def continue_request():
    print("Czy chcesz kontynuować edycje przedmiotów?")
    print("Tak: Y")
    print("Nie: N")
    user_confirm = str(input(": ")).upper()
    if user_confirm == "N":
        return False
    elif user_confirm == "Y":
        return True
    else:
        bad_response()


def break_point():
    print("Czy chcesz przerwać?")
    print("Tak: Y")
    print("Nie: N")
    user_confirm = str(input(": ")).upper()
    if user_confirm == "N":
        return False
    elif user_confirm == "Y":
        return True
    else:
        bad_response()


def buy(account_balance, history, inventory, product, price, quantity, selling_price, db):
    from app import HistoryEntry, InventoryItem
    item_name = product
    item_quantity = quantity
    cost_price = price
    list_price = selling_price
    purchase_price = item_quantity * cost_price
    if purchase_price > account_balance:
        return 0
    history_message = f"Zakupiono przedmiot: \"{item_name}\", w ilości: {item_quantity}. Cena za sztuke: {round(cost_price, 2)} PLN. Łączna cena za zamówienie: {round(purchase_price, 2)} PLN."
    history.append(history_message)

    history_entry = HistoryEntry(message=history_message)
    db.session.add(history_entry)

    if item_name.upper() not in inventory:
        inventory[item_name.upper()] = {
            "item_name": item_name,
            "quantity": item_quantity,
            "list_price": list_price
        }

        item_entry = InventoryItem(name=item_name.upper(
        ), quantity=item_quantity, list_price=list_price)
        db.session.add(item_entry)

    else:
        inventory[item_name.upper()]["quantity"] += item_quantity
        inventory[item_name.upper()]["list_price"] = list_price
        item_name_upper = item_name.upper()
        db_item = db.session.query(InventoryItem).filter_by(
            name=item_name_upper).first()
        db_item.quantity += item_quantity
        db_item.list_price = list_price

    db.session.commit()
    return purchase_price


def balance(history, new_balance, account_balance, db):
    from app import HistoryEntry
    if account_balance + new_balance < 0:
        return 0
    amount = new_balance
    if amount > 0:
        history_message = f"Do konta dodano: {amount} PLN."
        history.append(history_message)

        history_entry = HistoryEntry(message=history_message)
        db.session.add(history_entry)
        db.session.commit()

    elif amount < 0:
        history_message = f"Z konta odjęto: {amount} PLN."
        history.append(history_message)

        history_entry = HistoryEntry(message=history_message)
        db.session.add(history_entry)
        db.session.commit()

    return amount


def list_overview(inventory):
    print("*" * 30)
    print("PEŁEN WYKAZ MAGAZYNU")
    print("*" * 10)
    for item_name in inventory:
        name = inventory.get(item_name, {}).get("item_name")
        quantity = inventory.get(item_name, {}).get("quantity")
        list_price = inventory.get(item_name, {}).get("list_price")
        print("*" * 10)
        print(f"Przedmiot: {name}")
        print(f"Liczba dostępnych sztuk: {quantity}")
        print(f"Cena: {round(list_price, 2)} PLN")
    print("*" * 30)


def inventory_overview(inventory):
    item = None
    while not item:
        item = str(input("Podaj nazwe przedmiotu: ")).upper()
        if item not in inventory:
            user_confirm = item_not_in_inventory()
            if not user_confirm:
                break
            else:
                item = None
        else:
            quantity = inventory[item]["quantity"]
            name = inventory.get(item, {}).get("item_name")
            print(f"Stan magazynu dla przedmiotu \"{name}\": {quantity}.")


def sell(history, inventory, item, sell_quantity, db):
    from app import HistoryEntry, InventoryItem
    item_to_sell = item.upper()
    if item_to_sell not in inventory:
        return 0
    else:
        item_name = inventory.get(item_to_sell, {}).get("item_name")
        list_price = inventory.get(item_to_sell, {}).get("list_price")
        quantity = inventory.get(item_to_sell, {}).get("quantity")
        selling_quantity = sell_quantity
        available_quantity_left = quantity - selling_quantity
        if available_quantity_left < 0:
            return 0
        else:
            selling_price = selling_quantity * list_price
            inventory[item_to_sell]["quantity"] = available_quantity_left
            history_message = f"Sprzedano \"{item_name}\" w ilość sztuk: {selling_quantity}. Cena sprzedaży: {round(selling_price, 2)} PLN."
            history.append(history_message)

            history_entry = HistoryEntry(message=history_message)
            db.session.add(history_entry)

            item_name_upper = item_to_sell
            db_item = db.session.query(InventoryItem).filter_by(
                name=item_name_upper).first()
            db_item.quantity -= sell_quantity

            db.session.commit()

            return selling_price


def inventory_correction(history, inventory):
    item = str(input("Wprowadź nazwę przedmiotu: "))
    if item.upper() not in inventory:
        print(f"W magazynie nie ma przedmiotu o nazwie: \"{item}\"")
    else:
        old_item_name = inventory.get(item.upper(), {}).get("item_name")
        old_list_price = inventory.get(item.upper(), {}).get("list_price")
        old_quantity = inventory.get(item.upper(), {}).get("quantity")
        print("*" * 10)
        print(
            f"Przedmiot: {old_item_name}, Cena: {round(old_list_price, 2)} PLN, Liczba dostępnych sztuk: {old_quantity}")
        print("*" * 10)
        history_message = f"Rozpoczeto edycje przedmiotu \"{item}\"."
        history.append(history_message)
        user_confirm = True
        while user_confirm:
            print("wprowadz komende do edycji")
            print("Zmiana nazwy przedmiotu: NAZWA")
            print("Zmiana ceny: CENA")
            print("Zmiana ilości dostępnych sztuk: LICZBA")
            print("Wyjdź: EXIT")
            command = str(input(": ")).upper()
            if command == "NAZWA":
                new_item_name = str(input("Wprowadź nową nazwę: "))
                item_data = inventory.pop(item.upper())
                item_data["item_name"] = new_item_name
                inventory[new_item_name.upper()] = item_data
                history_message = f"Ustawiono nową nazwę przedmiotu: \"{new_item_name}\"."
                history.append(history_message)
                print("Zmiana nazwy przedmiotu. Edycja zostaje zamknięta.")
                user_confirm = False
            elif command == "CENA":
                new_list_price = None
                while not isinstance(new_list_price, float):
                    try:
                        list_message = "Podaj nową cene sprzedaży 1 sztuki towaru: "
                        new_list_price = decimal_count_check(
                            new_list_price, list_message)
                        list_price_confirm = confirm(new_list_price)
                        new_list_price = check_if_number_positive(
                            list_price_confirm, new_list_price, "Bład. Cena sprzedaży nie może być mniejsza lub równa 0.")
                    except ValueError:
                        bad_response()
                inventory[item.upper()]["list_price"] = new_list_price
                history_message = f"Ustawiono nową cenę przedmiotu: {round(new_list_price, 2)} PLN."
                history.append(history_message)
                user_confirm = continue_request()
            elif command == "LICZBA":
                new_quantity = None
                while not isinstance(new_quantity, int):
                    try:
                        new_quantity = int(
                            input("Podaj liczbe dostępnych przedmiotów: "))
                        item_quantity_confirm = confirm(new_quantity)
                        new_quantity = check_if_number_positive(
                            item_quantity_confirm, new_quantity, "Bład. Liczba dostępnych sztuk nie może być mniejsza lub równa 0.")
                    except ValueError:
                        bad_response()
                inventory[item.upper()]["quantity"] = new_quantity
                history_message = f"Zmieniono liczbę dostepnych sztuk przedmiotu: {new_quantity}"
                history.append(history_message)
                user_confirm = continue_request()
            elif command == "EXIT":
                user_confirm = False
            else:
                bad_response()
        history_message = f"Zakończono edycje przedmiotu: \"{item}\""
        history.append(history_message)
