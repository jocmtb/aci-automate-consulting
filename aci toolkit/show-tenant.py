import sys
import acitoolkit.acitoolkit as ACI

# Credentials and information for the DevNet ACI Simulator Always-On Sandbox
APIC_URL = "https://172.20.116.11/"
APIC_USER = "apic:LOCAL\\cisco"
APIC_PASSWORD = "C0nsult1nG2023!"

def main():
    """
    Main execution routine
    :return: None
    """

    # Login to APIC
    session = ACI.Session(APIC_URL, APIC_USER, APIC_PASSWORD)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)

    # Download all of the tenants
    print("TENANT")
    print("------")
    tenants = ACI.Tenant.get(session)
    for tenant in tenants:
        #print(dir(tenant))
        print('{0:36} {1:40} {2:24}'.format(tenant.name, tenant.dn, tenant.descr ))

if __name__ == '__main__':
    main()