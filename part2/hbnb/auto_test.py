import requests

base_url = "http://127.0.0.1:5000/api/v1/users/"

d_user = [
    {"first_name":"riyadh", "last_name": "alhamad", "email": "mail@mail.com"},
    {"first_name":"mhamad", "last_name": "alhamad", "email": "mmmmail@mail.com"},
    {"first_name":"badr", "last_name": "alhamad", "email": "mail@mail.com"} 
]

#POST
for user in d_user:
    get_users = requests.post(base_url, json=user)
    print("POST: ",get_users.status_code, get_users.json())

#GET
get_all = requests.get(base_url)
print("\n GET All Users: ", get_all.status_code)
users = get_all.json()
print(users)

if len(users) > 1:
    #print(users)
    user_id = users[1]["id"]
    update = {"first_name": "mmmmmmmm", "last_name": "Alllllllllil", "email": "mmmmmmm@mmmm.com"}
    get_users = requests.put(base_url + user_id, json=update)
    print("\n PUT:", get_users.status_code, get_users.json())
    