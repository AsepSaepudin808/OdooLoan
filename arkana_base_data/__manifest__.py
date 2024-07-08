{
    'name': "Arkana - Base Data",
    'summary': "Arkana - Base Data",
    'description': "Arkana - Base Data",
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
    ],
    'post_init_hook': '_create_tax_components_setup',
    'application': False,
    'installable': True,
    'auto_install' : True,
    "external_dependencies": {"python": []},
}