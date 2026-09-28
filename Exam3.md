# ТЗ — Banking System на Django MVT

Разработать банковскую систему на **Django MVT** с использованием **Models, Forms, Views, Templates и ORM**.

## 1. Authentication

Пользователь может:

* зарегистрироваться по `phone_number` и `password`;
* войти и выйти из системы.

После регистрации пользователь создаёт `Account`:

* `first_name`
* `last_name`
* `address`
* `passport_id`
* `balance`

При создании:

```text
balance = 1000
```

---

## 2. Cards

Авторизованный пользователь может создавать несколько карт.

Поля:

* `card_number`
* `cvv`
* `date`
* `type`
* `PIN`
* `balance`

При создании карты:

```text
balance = 500
```

Пользователь может:

* смотреть свои карты;
* смотреть детали карты;
* изменять и удалять свои карты.

`card_number` и `passport_id` должны быть уникальными.

---

## 3. Transactions

Пользователь может отправлять деньги:

* по `phone_number`;
* по `card_number`.

Перед переводом выбирается источник:

```text
Account
Card
```

Поддержать переводы:

```text
Account → Account
Account → Card
Card → Account
Card → Card
```

Перед переводом проверить:

* получателя;
* принадлежность источника пользователю;
* `amount > 0`;
* достаточность баланса.

При успешном переводе:

```text
source.balance -= amount
destination.balance += amount
```

И создаётся запись в `Transaction`.

---

## 4. Transaction History

Пользователь видит историю своих транзакций.

Фильтры:

```text
All
Sent
Received
```

Для каждой карты также должна быть отдельная история её транзакций с такими же фильтрами.

---

## 5. Check User / Card

### Check Phone

Пользователь вводит номер телефона.

Если найден:

```text
First name
Last name
```

Иначе:

```text
User not found
```

### Check Card

Пользователь вводит номер карты.

Если найдена:

```text
First name
Last name
```

Иначе:

```text
Card not found
```

Нельзя показывать `password`, `PIN`, `CVV`, `balance`, `passport_id` и другие приватные данные.

---

## 6. Access Control

Пользователь может работать только со своими:

* Account;
* Cards;
* Transactions.

Нельзя использовать чужой Account/Card как источник перевода или изменять чужие данные.

---

## 7. Models

Минимальные модели:

```text
User
Account
Card
Transaction
```

Связи между ними реализовать через Django ORM.

---

## 8. Forms / Views / Templates

Создать Forms для:

* Registration/Login;
* Account;
* Card;
* Transfer;
* Check Phone/Card.

Создать Views и Templates для:

* Authentication;
* Account;
* Cards CRUD;
* Transfers;
* Transaction History;
* Check Phone/Card.

Все операции с базой выполнять через **Django ORM**.
