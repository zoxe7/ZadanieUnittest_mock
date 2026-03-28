import requests
def get_user_full_name(user_id):
 
 try:
 response = requests.get(f"https://api.example.com/users/{user_id}")

 
 response.raise_for_status()
 user_data = response.json()
 full_name = f"{user_data.get('first_name')}
{user_data.get('last_name')}"
 return full_name
 except requests.exceptions.HTTPError as http_err:
 if response.status_code == 404:
 return None
 else:
 return "Server error"

 except requests.exceptions.RequestException:
 return "Network error
