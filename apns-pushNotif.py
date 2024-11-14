from apns2.client import APNsClient
from apns2.payload import Payload
from apns2.credentials import TokenCredentials

# Replace these with your actual APNs key and app details
KEY_PATH = "/Users/nikhilkvk/Documents/KeysAndCerts/AuthKey_Z7V9BTP7Q7.p8"  # Path to the APNs .p8 key
KEY_ID = "Z7V9BTP7Q7"  # Your APNs key ID
TEAM_ID = "Y86K2MHN8H"  # Your Apple Developer Team ID
BUNDLE_ID = "com.nikhil.LTC-BookUrMeal"  # Your app's bundle ID
DEVICE_TOKEN = ["8b2b12f7b74370ead86bb95d0266d2782f29dfc2831bb13d1c8833025d51d14a",
                "80759ec7b956f5109aa978fb31c5b9f928df5c65cd989e7f9f96096c61e4b3344b5847ff45dfa9a8411d8bd51575b061b6f6ba24ef4d0a66bad7d29be424a300570179cb2bdfbb6dfc6a2023bfa9a18d"]  # The device token to send the notification to

# Initialize APNs client
token_credentials = TokenCredentials(KEY_PATH, KEY_ID, TEAM_ID)
client = APNsClient(credentials=token_credentials, use_sandbox=True)  # Set use_sandbox=False for production

# Create the payload for the push notification
payload = Payload(alert="This is a test notification", badge=1, sound="default")

# Send the push notification
for token in DEVICE_TOKEN:
    client.send_notification(token, payload, topic=BUNDLE_ID)

print("Notification sent successfully!")
