# groot-ad-service
A service to trigger the ActiveDirectory script that adds members to the ACM AD group once they have paid membership fees.

Currently has 1 endpoint: /adduser/<netid>, which takes in an auth token through the header, and the netid of the new user through the url