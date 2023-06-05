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

        filename = 'mega_apic_aci_tab.xlsx'
        filename = str(filename)
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(filename)
        for x in data.keys():
          worksheet = workbook.add_worksheet(x)
          # Widen the first column to make the text clearer.
          worksheet.set_column(0, 0, 4)
          worksheet.set_column(1, 1, 32)
          worksheet.set_column(2, 2, 32)
          worksheet.set_column(3, 3, 32)
          worksheet.set_column(4, 4, 12)
          worksheet.set_column(5, 5, 10)
          worksheet.set_column(6, 6, 10)
          worksheet.set_column(7, 7, 24)
          worksheet.set_column(8, 8, 12)

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
          worksheet.write('C1', 'Descr',bold)
          worksheet.write('D1', 'Alias', bold)
          worksheet.write('E1', 'Pc Tag', bold)
          worksheet.write('F1', 'FiE', bold)
          worksheet.write('G1', 'Pref Group', bold)
          worksheet.write('H1', 'Bridge Domain', bold)
          worksheet.write('I1', 'Shutdown', bold)

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

def Create_Excel_Table(data,data2):

        filename=f'mega_apic_aci.xlsx'
        filename=str(filename)
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('apic_aci')
        worksheet2 = workbook.add_worksheet('apic_aci2')
        # Widen the first column to make the text clearer.
        for x in [worksheet,worksheet2]:
          x.set_column(0, 0, 4)
          x.set_column(1, 1, 32)
          x.set_column(2, 2, 32)
          x.set_column(3, 3, 32)
          x.set_column(4, 4, 12)
          x.set_column(5, 5, 12)
          x.set_column(6, 6, 12)
        #add border to cells
        border_format=workbook.add_format({
                            'border':1,
                            'align':'left',
                            'font_size':10
                           })
        worksheet.conditional_format( 'A1:N1000' , { 'type' : 'no_blanks' , 'format' : border_format} )
        worksheet2.conditional_format( 'A1:N1000' , { 'type' : 'no_blanks' , 'format' : border_format} )
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True,'bg_color':'#095381','color':'#ffffff','font_size':12})

        # Write some simple text. Text with formatting.
        for ws in [worksheet,worksheet2]:
          ws.write('A1', 'No', bold)
          ws.write('B1', 'EPG Name', bold)
          ws.write('C1', 'Descr', bold)
          ws.write('D1', 'Alias', bold)
          ws.write('E1', 'PC Tag', bold)
          ws.write('F1', 'FiE', bold)
          ws.write('G1', 'Pref Group', bold)
          ws.write('H1', 'Bridge Domain', bold)
          ws.write('I1', 'Shutdown', bold)
        #Create excel file, put data in excel
        ordenar_left = workbook.add_format({'align':'left','font_size':10})
        custom_1 = workbook.add_format({'align':'left','font_size':10,'bg_color':'#66ff66'})
        custom_2 = workbook.add_format({'align':'left','font_size':10,'bg_color':'#ff9999'})
        i=1
        for dat,wks in [(data,worksheet),(data2,worksheet2)]:
                # Write some numbers, with row/column notation.
                for x in dat:
                  wks.write(i, 0, i, ordenar_left)
                  wks.write(i, 1, x['name'], ordenar_left)
                  wks.write(i, 2, x['descr'], ordenar_left)
                  wks.write(i, 3, x['alias'], ordenar_left)
                  wks.write(i, 4, x['pctag'], ordenar_left)
                  if x['fie']=='disabled':
                    wks.write(i, 5, x['fie'], custom_2)
                  else:
                    wks.write(i, 5, x['fie'], custom_1)
                  wks.write(i, 6, x['pg'], ordenar_left)
                  wks.write(i, 7, x['BDName'], ordenar_left)
                  wks.write(i, 8, x['shutdown'], ordenar_left)
                  i+=1
                i=1
        i=1
        workbook.close()
        #os.system('start excel.exe doc2.xlsx')

if __name__=='__main__':
    resp = requests.post(url, json = data_payload, verify=False)

    #print(resp.json()["imdata"][0]["aaaLogin"]["attributes"])
    token = resp.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

    TENANT_NAME = 'REPLICACION_TRI-MEG_EyN'
    tenants_list = ['CAPITAL_SALUD', 'CLARO_IT', 'EXITO', 'ECOPETROL', 'REPLICACION_TRI-MEG_EyN']
    dict_EPG = {}
    for tenant in tenants_list:
        lista_EPG = []
        get_epg_with_faults = requests.get(f'https://{APIC_IP}/api/node/mo/uni/tn-{tenant}/ap-AP_{tenant}.json?query-target=subtree&target-subtree-class=fvAEPg&query-target-filter=eq(fvAEPg.isAttrBasedEPg,"false")&rsp-subtree=children&rsp-subtree-class=fvRsBd&order-by=fvAEPg.name|asc&page=0&page-size=200'
                                    , headers={'Cookie': f'APIC-cookie={token}'}, verify=False)
        epg_list = get_epg_with_faults.json()["imdata"]
        print('{0}'.format('+'*80 ))
        print('{0:10} {1}'.format('Tenant:', tenant))
        for tn in epg_list:
            if "children" in tn["fvAEPg"].keys():
                epg_name = tn["fvAEPg"]["attributes"]["name"]
                epg_descr = tn["fvAEPg"]["attributes"]["descr"]
                epg_fie = tn["fvAEPg"]["attributes"]["floodOnEncap"]
                epg_pg = tn["fvAEPg"]["attributes"]["prefGrMemb"]
                epg_pctag = tn["fvAEPg"]["attributes"]["pcTag"]
                epg_alias = tn["fvAEPg"]["attributes"]["nameAlias"]
                epg_shutdown = tn["fvAEPg"]["attributes"]["shutdown"]
                BD_list = tn["fvAEPg"]["children"]
                for bd in BD_list:
                    print('{0:32} {1:30}  {2:32} {3:12} {4:12} {5:12} {6:12} {7:12}'.format(epg_name
                                                ,epg_descr
                                                ,epg_alias
                                                ,epg_pctag
                                                ,epg_fie
                                                ,epg_pg
                                                ,bd["fvRsBd"]["attributes"]["tnFvBDName"]
                                                ,epg_shutdown
                                                ))
                    lista_EPG.append({'name':epg_name
                                                ,'descr':epg_descr
                                                ,'alias':epg_alias
                                                ,'pctag':epg_pctag
                                                ,'fie':epg_fie
                                                ,'pg':epg_pg
                                                ,'BDName':bd["fvRsBd"]["attributes"]["tnFvBDName"]
                                                ,'shutdown':epg_shutdown})
        dict_EPG[tenant] = lista_EPG
        print('\n{0}'.format('+'*80 ))

    Create_Excel_Table_per_Tab(dict_EPG)

