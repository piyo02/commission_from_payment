{
    'name': 'Commision Management',
    'category': 'sale',
    'version': '10.0',
    'summary': 'Summary the addon.',
    'description': '''Description the addon'''
                   ,
    'depends': ['base', 'sale', 'account'],
    'data': [
        'menu.xml',
        'view/commision_type.xml',
        'view/invoices.xml',
        'view/partner.xml',
        'view/product_template_view.xml',
        'view/report_settlement_temp.xml',
        'view/sale_order.xml',
        'wizard/commision_inv_wizard.xml',
    ],
    'images': [''],
    'auto_install': False,
    'installable': True,
    'application': False,
}
