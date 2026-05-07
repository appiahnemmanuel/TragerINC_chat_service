import os
from huggingface_hub import InferenceClient
import requests
from decouple import config, RepositoryEnv

#config = config(RepositoryEnv(os.path.join(os.getcwd(), '.env')))

api_key = config('HF_API_KEY')
FASTAPI_BASE_URL = 'http://127.0.0.1:8000'

client = InferenceClient(api_key=api_key)

#FASTAPI_BASE_URL = FASTAPI_BASE_URL

def get_customer_info(customer_id: str):
	try:
		response = requests.get(f'{FASTAPI_BASE_URL}/customers/{customer_id}')
		response.raise_for_status()
		return response.json()
	except requests.exceptions.RequestException as e:
		print(f"Error fetching customer info: {e}")
		return None
	
def get_energy_usage(customer_id: str):
    try:
        response = requests.get(f'{FASTAPI_BASE_URL}/energy_usage/{customer_id}')
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching energy usage: {e}")
        return None
    

def get_support_tickets(customer_id: str):
    try:
        response = requests.get(f'{FASTAPI_BASE_URL}/support_tickets/{customer_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching support tickets: {e}")
        return None


def generate_chatbot_response(user_input: str, customer_id: str):
    customer_info = get_customer_info(customer_id)

    energy_usage = get_energy_usage(customer_id)

    support_tickets = get_support_tickets(customer_id)

    context = (
        f'Customer Info:\n'
        f'Name: {customer_info.get("first_name")} {customer_info.get("last_name")}\n'
        f'Email: {customer_info.get("email")}\n'
        f'Account Status: {customer_info.get("account_status")}\n'

        f"Energy Usage:\n"
        f"Last month's usage: {energy_usage[0]['usage_kwh']} kWh\n"
        f"Peak demand: {energy_usage[0]['peak_demand_kwh']} kWh\n"
        f"Total charge: ${energy_usage[0]['total_charge']}\n\n"

        f'Support Tickets:\n'
        f"{'No support tickets found.' if not support_tickets else ''}" +
        "\n".join([f"- [{ticket['issue_type']}] {ticket['ticket_status']}" for ticket in support_tickets]) + "\n\n"

        f"User Query: {user_input}\n\n"
    )

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[
                {
                    "role": "user",
                    "content": context
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error generating chatbot response: {e}")
        return "Sorry, I couldn't generate a response at this time."