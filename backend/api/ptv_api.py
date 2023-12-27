# We got access to the api (⌐■_■)
# •ᴥ•

import requests

user_Id= "3002643"
API_key= "8ad3d125-2509-4055-bab7-a7d75bffd0b7"

response = requests.get("https://timetableapi.ptv.vic.gov.au/v3/routes?devid=3002643&signature=7FEA36B28AB297DE8D929259C53D655C3055211F")
print(response.status_code)
