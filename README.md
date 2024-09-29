# CheckBox
Project

## Development setup


Clone this repository:

```
git clone https://github.com/OldSem/checkbox_test.git
cd checkbox_test
```
Create .env file
```
make create_env
```
Start project:

```
make up
```




## Instructions

For start project use  

```
make up
```

Create migrations
```
alembic revision --autogenerate -m "Initial migration"
```

Variables:
```
{{base_url}}=0.0.0.0:8000

```
Test
```
make test

```


### Auth
Add user:
```
POST {{base_url}}/users/
BODY:
{"username": "username",
"role": "Admin",
"email": "username@gmail.com",
"password": "password"}
```
Get token:
```
POST {{base_url}}/token
BODY:
{
    "password": "password",
    "username": "username"
}
```

### Tasks

Create Receipt
```
POST {{base_url}}/receipts/
BODY:
{
  "products": [
    {
      "name": "Good name",
      "price": 20.00,
      "quantity": 3
    },
    ...
  ],
  "payment": {
    "type": "card"/"cash",
    "amount": 200
  }
}

```
Get Receipts
```
GET {{base_url}}/receipts/

```
View Receipt
```
GET {{base_url}}/receipts/{{nn}}/show/
```
