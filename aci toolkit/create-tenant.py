import acitoolkit.acitoolkit as aci

# Define static values to pass (edit these if you wish to set differently)
DEFAULT_TENANT_NAME = 'Yellow_test_tenant3'

def main():
    """
    Main create tenant routine
    :return: None
    """
    # Get all the arguments
    description = 'It logs in to the APIC and will create the tenant.'
    creds = aci.Credentials('apic', description)
    creds.add_argument('-t', '--tenant', help='The name of tenant'
                     #,username='admin', password='cisco!123', URL='https://10.122.189.35'
                       ,default=DEFAULT_TENANT_NAME)

    args = creds.get()

    # Login to the APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    # Create the Tenant
    tenant = aci.Tenant(args.tenant)

    # Push the tenant to the APIC
    resp = session.push_to_apic(tenant.get_url(),
                                tenant.get_json())
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)
    else:
        print('Tenant Created {0}'.format(DEFAULT_TENANT_NAME))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass