{
    'name': "Arkana - Partner",
    'summary': "Arkana - Partner",
    'description': "Arkana - Partner",
    'author': "PT. Arkana Solusi Digital",
    "maintainers": ["nrkholid"],
    'website': "https://arkana.co.id",
    'category': 'Human Resources/Employees',
    "version": "16.0.1.0.0",
    'depends': [
        'arkana_base_training'
    ],
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'wizard/partner_wizard.xml',
        # 'views/arkana_partner_menu.xml',
    ],
    # 'post_init_hook': '_create_tax_components_setup',
    'application': True,
    'installable': True,
    'auto_install' : True,
    "external_dependencies": {"python": []},
}