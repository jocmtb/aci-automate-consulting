import requests

APIC_IP = '172.20.116.11'

url = f'https://{APIC_IP}/api/aaaLogin.json'
data_payload = {
    "aaaUser" : {
        "attributes" : {
            "name" : "apic:LOCAL\\cisco",
            "pwd" : "C0nsult1nG2023#"
        }
    }
}

resp = requests.post(url, json = data_payload, verify=False)
token = resp.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

get_nodes = requests.get(f'https://{APIC_IP}/api/class/eqptcapacityFSPartition.json?query-target-filter=eq(eqptcapacityFSPartition.path,"/bootflash")'
                            , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
nodes = get_nodes.json()["imdata"]
print('{0:12} {1:16} {2:12} {3:14} {4:12} {5:12}'.format('Node', 'Partition', 'Free mem', 'Used mem', 'Total', 'Utilization'))
print(len('{0:12} {1:16} {2:12} {3:14} {4:12} {5:12}'.format('node', 'partition', 'free_mem', 'used_mem', 'Total','utilization'))*'-')
for node in nodes:
    nodeId = node["eqptcapacityFSPartition"]["attributes"]["dn"].split('/')[2]
    partition = node["eqptcapacityFSPartition"]["attributes"]["path"].rstrip()
    free_mem = int(node["eqptcapacityFSPartition"]["attributes"]["avail"]) 
    used_mem = int(node["eqptcapacityFSPartition"]["attributes"]["used"])
    total_mem = free_mem + used_mem
    utilization = f'{round( (used_mem / (used_mem  + free_mem))*100, 2)}%'
    print('{0:12} {1:16} {2:<12} {3:<14} {4:<12} {5:12}'.format(nodeId, partition, free_mem, used_mem, total_mem, utilization))