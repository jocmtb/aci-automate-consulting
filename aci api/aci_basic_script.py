import requests

APIC_IP = '172.20.116.11'

url = f'https://{APIC_IP}/api/aaaLogin.json'
data_payload = {
    "aaaUser" : {
        "attributes" : {
            "name" : "apic:LOCAL\\cisco",
            "pwd" : "C0nsult1nG2023!"
        }
    }
}

resp = requests.post(url, json = data_payload, verify=False)

#print(resp.json()["imdata"][0]["aaaLogin"]["attributes"])
token = resp.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

get_tenants = requests.get(f'https://{APIC_IP}/api/class/fvTenant.json'
                            , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
tenants = get_tenants.json()["imdata"]
for tn in tenants:
    print('tenant: {0:32} {1:12}'.format(tn["fvTenant"]["attributes"]["name"], tn["fvTenant"]["attributes"]["dn"]))