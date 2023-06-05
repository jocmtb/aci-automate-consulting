from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession

import sys

apicUrl = 'https://172.27.76.11'
loginSession = LoginSession(apicUrl, 'apic:LOCAL\\cisco', 'C0nsult1nG2023!')
moDir = MoDirectory(loginSession)
moDir.login()

# Use the connected moDir queries and configuration...
tenant1Mo = moDir.lookupByClass(fvTenant, propFilter='and(eq(fvTenant.name, EXITO))')
print('{024} {124} {224} {324}'.format('Name', 'Dn', 'Description', 'Annotation'))
print('{024} {124} {224} {324}'.format(len('Name')'-', len('Dn')'-', len('Description')'-', len('Annotation')'-'))
print('{024} {124} {224} {324}'.format(tenant1Mo[0].name, tenant1Mo[0].dn, tenant1Mo[0].descr, tenant1Mo[0].annotation))

moDir.logout()