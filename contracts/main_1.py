from docxtpl import DocxTemplate

doc = DocxTemplate('template.docx')

context = {
    'company_name': 'test',
    'contract_date': '2025-06-05',
    'full_name': 'Dummy User',
    'address_1': 'long address',
    'primary_number': '1232567890',
    'secondary_number': '9876532103',
    'abn_number': '12345678',
    'distance_covered': '25',
    'standard_inspection': '120',
    'suburbs_list': 'a,b,c,d,e,f,g,h',
    'bsb': '1233',
    'account_number': '1234567890',

}

doc.render(context)
doc.save(f'{context['full_name']}.docx')