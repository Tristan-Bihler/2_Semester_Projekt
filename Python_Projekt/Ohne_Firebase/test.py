import requests

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMDA5MTg5MzgxZWNlMWI0YmVhYmYzMTEwNjhlNzNhZiIsIm5iZiI6MTc0OTgwMjE2Ny4yNiwic3ViIjoiNjg0YmRjYjdmN2Q3Njc2NTA4NWM3MzIzIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9._QsNJ-SUmLVsvPO9YE8cshUgZCns4o1mlxZfH48bFuQ"
}

response = requests.get(url, headers=headers)

print(response.text)