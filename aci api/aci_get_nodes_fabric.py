import requests

#MEGA 172.20.116.11
#TRIARA 172.27.76.11
APIC_IP = '172.27.76.11'

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

print(resp.json()["imdata"][0]["aaaLogin"]["attributes"])
token = resp.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

get_tenants = requests.get(f'https://{APIC_IP}/api/node/class/fabricNode.json?query-target-filter=and(ne(fabricNode.role, %22controller%22), ge(fabricNode.id,%22101%22),le(fabricNode.id,%22315%22))'
                            , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
tenants = get_tenants.json()["imdata"]
for tn in tenants:
    print('{0:20} {1:8} {2:20} {3:12} {4:12} {5:12} {6:12} {7:12}'.format(tn["fabricNode"]["attributes"]["name"]
                                         , tn["fabricNode"]["attributes"]["id"]
                                         , tn["fabricNode"]["attributes"]["model"]
                                         , tn["fabricNode"]["attributes"]["role"]
                                         , tn["fabricNode"]["attributes"]["address"]
                                         , tn["fabricNode"]["attributes"]["serial"]
                                         , tn["fabricNode"]["attributes"]["version"]
                                         , tn["fabricNode"]["attributes"]["dn"]
                                         ))