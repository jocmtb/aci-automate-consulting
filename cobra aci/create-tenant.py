from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant


TENANT_NAME = 'Example_Brown_tn'
apicUrl = 'https://10.122.189.35'
loginSession = LoginSession(apicUrl, 'admin', 'cisco!123')
moDir = MoDirectory(loginSession)
moDir.login()

# Get the top level Policy Universe Directory
uniMo = moDir.lookupByDn('uni')

# Create Tenant
print("Creating tenant %s.." % (TENANT_NAME))
fvTenantMo = Tenant(uniMo, TENANT_NAME)

# Use the connected moDir queries and configuration...
tenantCfg = ConfigRequest()
tenantCfg.addMo(fvTenantMo)
moDir.commit(tenantCfg)

moDir.logout()