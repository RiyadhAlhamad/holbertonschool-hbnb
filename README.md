# HBnB RESTful API (Part 2)

This project is a modular and extensible RESTful API backend built in Python, following clean architecture principles. It includes well-organized layers for models, services, persistence, and routing.

---

## 📁 Project Structure

```
📁 part2
└── hbnb
    ├── auto_test.py
    ├── config.py
    ├── requirements.txt
    ├── run.py
    ├── app
    │   ├── __init__.py
    │   ├── api
    │   │   ├── __init__.py
    │   │   └── v1
    │   │       ├── amenities.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       ├── users.py
    │   │       └── __init__.py
    │   ├── models
    │   │   ├── amenity.py
    │   │   ├── BaseModel.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── user.py
    │   │   └── __init__.py
    │   ├── persistence
    │   │   ├── repository.py
    │   │   └── __init__.py
    │   └── services
    │       ├── facade.py
    │       └── __init__.py
    └── README.md
```


---

## 🚀 Features

- ✅ Modular and layered architecture
- ✅ RESTful API endpoints:
  - `/api/v1/amenities`
  - `/api/v1/places`
  - `/api/v1/reviews`
  - `/api/v1/users`
- ✅ Service layer abstraction
- ✅ Repository pattern for data persistence
- ✅ Easy configuration using `config.py`
- ✅ Automated testing with `auto_test.py`

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/hbnb-api.git
cd hbnb-api/part2/hbnb
```

2. **Create and activate a virtual environment**:

```
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```
pip install -r requirements.txt

```

## ▶️ Running the API

python run.py
```
The server will start on the configured host and port (default is http://127.0.0.1:5000/).
```

## ✅ Running Tests

python auto_test.py
```
This runs predefined automated tests to validate the API functionality.
```


## 🧠 Technologies Used

Python 3

Flask

RESTful API







