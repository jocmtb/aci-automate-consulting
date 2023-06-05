import requests
import xlsxwriter

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

def Create_Excel_Table_per_Tab(data):

        filename = 'mega_apic_aci_endpoints.xlsx'
        filename = str(filename)
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(filename)
        for x in data.keys():
          worksheet = workbook.add_worksheet(x[:31])
          # Widen the first column to make the text clearer.
          worksheet.set_column(0, 0, 4)
          worksheet.set_column(1, 1, 32)
          worksheet.set_column(2, 2, 16)
          worksheet.set_column(3, 3, 12)
          worksheet.set_column(4, 4, 12)
          worksheet.set_column(5, 5, 10)
          worksheet.set_column(6, 6, 10)
          worksheet.set_column(7, 7, 48)
          worksheet.set_column(8, 8, 32)

          #add border to cells
          border_format=workbook.add_format({
                            'border':1,
                            'align':'left',
                            'font_size':10
                           })
          worksheet.conditional_format( 'A1:N1000' , { 'type' : 'no_blanks' , 'format' : border_format} )
          # Add a bold format to use to highlight cells.
          bold = workbook.add_format({'bold': True,'bg_color':'#095381','color':'#ffffff','font_size':12})

        # Write some simple text. Text with formatting.
          worksheet.write('A1', 'No',bold)
          worksheet.write('B1', 'EPG Name',bold)
          worksheet.write('C1', 'MAC',bold)
          worksheet.write('D1', 'IP', bold)
          worksheet.write('E1', 'Encap', bold)
          worksheet.write('F1', 'Source', bold)
          worksheet.write('G1', 'LC Own', bold)
          worksheet.write('H1', 'tDn', bold)
          worksheet.write('I1', 'Modified Timestamp', bold)

          #Create excel file, put data in excel
          ordenar_left = workbook.add_format({'align':'left','font_size':10})
          custom_1 = workbook.add_format({'align':'left','font_size':10,'bg_color':'#66ff66'}) 
          custom_2 = workbook.add_format({'align':'left','font_size':10,'bg_color':'#ff9999'}) 
          i=1
          for datax in data[x]:
                # Write some numbers, with row/column notation.
                worksheet.write(i, 0, i, ordenar_left)
                worksheet.write(i, 1, datax['name'], ordenar_left)
                worksheet.write(i, 2, datax['descr'], ordenar_left)
                worksheet.write(i, 3, datax['alias'], ordenar_left)
                worksheet.write(i, 4, datax['pctag'], ordenar_left)
                worksheet.write(i, 5, datax['fie'], ordenar_left)
                worksheet.write(i, 6, datax['pg'], ordenar_left)
                worksheet.write(i, 7, datax['BDName'], ordenar_left)
                worksheet.write(i, 8, datax['shutdown'], ordenar_left)
                i+=1
          i=1
          print("Excel Done")
        workbook.close()
        #os.system('start excel.exe doc2.xlsx')

if __name__=='__main__':
    resp = requests.post(url, json = data_payload, verify=False)

    #print(resp.json()["imdata"][0]["aaaLogin"]["attributes"])
    token = resp.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

    TENANT_NAME = 'EXITO'
    epgs_list = []
    dict_EPG = {}
    get_all_list_epgs = requests.get(f'https://{APIC_IP}/api/node/mo/uni/tn-{TENANT_NAME}/ap-AP_{TENANT_NAME}.json?query-target=subtree&target-subtree-class=fvAEPg&query-target-filter=eq(fvAEPg.isAttrBasedEPg,"false")&rsp-subtree=children&rsp-subtree-class=fvRsBd&order-by=fvAEPg.name|asc&page=0&page-size=200'
                                    , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
    epg_list = get_all_list_epgs.json()["imdata"]
    for tn in epg_list:
      if "children" in tn["fvAEPg"].keys():
        epg_name = tn["fvAEPg"]["attributes"]["name"]
        epgs_list.append(epg_name)

    for epg_name in epgs_list:
        lista_EPG = []
        get_epg_with_faults = requests.get(f'https://{APIC_IP}/api/node/mo/uni/tn-{TENANT_NAME}/ap-AP_{TENANT_NAME}/epg-{epg_name}.json?query-target=children&target-subtree-class=fvCEp&rsp-subtree=children&rsp-subtree-class=fvRsToVm,fvRsVm,fvRsHyper,fvRsCEpToPathEp,fvIp,fvPrimaryEncap&order-by=fvCEp.dn|asc&page=0&page-size=1000'
                                    , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
        epg_list = get_epg_with_faults.json()["imdata"]
        print('{0}'.format('+'*80 ))
        print('{0:10} {1}'.format('EPG:', epg_name))
        for tn in epg_list:
            if "children" in tn["fvCEp"].keys():
                ep_name = tn["fvCEp"]["attributes"]["name"]
                ep_mac = tn["fvCEp"]["attributes"]["mac"]
                ep_ip = tn["fvCEp"]["attributes"]["ip"]
                ep_encap = tn["fvCEp"]["attributes"]["encap"]
                ep_lcc = tn["fvCEp"]["attributes"]["lcC"]
                ep_lco = tn["fvCEp"]["attributes"]["lcOwn"]
                ep_modts = tn["fvCEp"]["attributes"]["modTs"]
                BD_list = tn["fvCEp"]["children"]
                for bd in BD_list:
                    if "fvRsCEpToPathEp" in bd.keys():
                      print('{0:32} {1:30}  {2:32} {3:12} {4:12} {5:12} {6:12} {7:12}'.format(ep_name
                                                ,ep_mac
                                                ,ep_ip
                                                ,ep_encap
                                                ,ep_lcc
                                                ,ep_lco
                                                ,bd["fvRsCEpToPathEp"]["attributes"]["tDn"]
                                                ,ep_modts
                                                ))
                      lista_EPG.append({'name':epg_name
                                                ,'descr':ep_mac
                                                ,'alias':ep_ip
                                                ,'pctag':ep_encap
                                                ,'fie':ep_lcc
                                                ,'pg':ep_lco
                                                ,'BDName':bd["fvRsCEpToPathEp"]["attributes"]["tDn"]
                                                ,'shutdown':ep_modts})
        dict_EPG[epg_name] = lista_EPG
        print('\n{0}'.format('+'*80 ))

    Create_Excel_Table_per_Tab(dict_EPG)

