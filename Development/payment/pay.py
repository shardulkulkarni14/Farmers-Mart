### Create a new Payment Request


# pip install instamojo-wrapper
from instamojo_wrapper import Instamojo

API_KEY = '3200b0a8745e5566455b40363dba2aa6'
AUTH_TOKEN = '4e327bece751601e5a0e5b3d63a15990'
api = Instamojo(api_key=API_KEY,
                auth_token=AUTH_TOKEN)

# Create a new Payment Request
response = api.payment_request_create(
	#buyer_name = 'Shardul',
    amount='10',
    purpose='FIFA 16',
    send_email=True,
    email="foo@example.com",
    redirect_url="http://www.example.com/handle_redirect.py",
    phone = "+919491655317"
    )
# print the long URL of the payment request.
print(response['payment_request']['longurl'])
# print the unique ID(or payment request ID)
print(response['payment_request']['id'])