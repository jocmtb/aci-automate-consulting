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

TENANT_NAME = 'REPLICACION_TRI-MEG_EyN'
tenants_list = ['CAPITAL_SALUD', 'CLARO_IT', 'EXITO', 'ECOPETROL', 'REPLICACION_TRI-MEG_EyN']
for tenant in tenants_list:
    get_epg_with_faults = requests.get(f'https://{APIC_IP}/api/mo/uni/tn-{tenant}.json?query-target=subtree&target-subtree-class=fvAEPg&rsp-subtree-include=faults'
                                , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
    epg_list = get_epg_with_faults.json()["imdata"]
    print('{0}'.format('+'*80 ))
    print('{0:10} {1}'.format('Tenant:', tenant))
    for tn in epg_list:
        if "children" in tn["fvAEPg"].keys():
            epg_name = tn["fvAEPg"]["attributes"]["name"]
            fault_list = tn["fvAEPg"]["children"]
            for fault in fault_list:
                print('{0:10} {1:30}\n  decsr: {2:32}\n  cause: {3:12}\n  rule: {4:12}\n  severity: {5:12}\n  type: {6:12}\n  date: {7:12}'.format('EPG:'
                                            ,epg_name
                                            ,fault["faultDelegate"]["attributes"]["descr"]
                                            ,fault["faultDelegate"]["attributes"]["cause"]
                                            ,fault["faultDelegate"]["attributes"]["rule"]
                                            ,fault["faultDelegate"]["attributes"]["severity"]
                                            ,fault["faultDelegate"]["attributes"]["type"]
                                            ,fault["faultDelegate"]["attributes"]["lastTransition"]))
    print('\n{0}'.format('+'*80 ))