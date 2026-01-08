import os
from azure.communication.phonenumbers import (
    PhoneNumbersClient, 
    PhoneNumberCapabilities, 
    PhoneNumberCapabilityType, 
    PhoneNumberType, 
    PhoneNumberAssignmentType
)
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("COMMUNICATION_SERVICE_CONNECTION_STRING")

phone_numbers_client = PhoneNumbersClient.from_connection_string(connection_string)

capabilities = PhoneNumberCapabilities(
        calling = PhoneNumberCapabilityType.INBOUND,
        sms = PhoneNumberCapabilityType.NONE
    )

poller = phone_numbers_client.begin_search_available_phone_numbers(
    "US",
    PhoneNumberType.TOLL_FREE,
    PhoneNumberAssignmentType.APPLICATION,
    capabilities,
    polling = True
)

search_result = poller.result()
print("Search Result:", search_result)
print("Phone Numbers to Purchase:", search_result.phone_numbers)

purchase_poller = phone_numbers_client.begin_purchase_phone_numbers(
    search_result.search_id,
    polling=True
)
purchase_result = purchase_poller.result()

# begin_purchase_phone_numbers returns None on success - this is expected behavior
if purchase_result is None:
    print("Purchase completed successfully!")
    print(f"Purchased Phone Numbers: {search_result.phone_numbers[0]}")
else:
    print(f"Purchase result: {purchase_result}")
