# This script is used for storing Twitter's App Credentials
# Please don't forget to call obtain_access_token.py afterwards

import pickle

credentials = {}

credentials['APP_KEY'] = input("What is your APP Key? ")
credentials['APP_SECRET'] = input("What is your APP Secret? ")

output = open('credentials.pkl', 'wb')

pickle.dump(credentials, output)

output.close()

print("Credentials have been stored ... don't forget to invoke obtain_access_token.py ...")