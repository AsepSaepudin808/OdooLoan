# -*- coding: utf-8 -*-
{
    'name': "Arkana - Base Training",
    'summary': "Arkana - Base Training",
    'description': "Arkana - Base Training",
    'author': "PT. Arkana Solusi Digital",
    "maintainers": ["AsepSaepudin808"],
    'website': "https://arkana.co.id",
    'category': 'Human Resources/Employees',
    "version": "16.0.1.0.0",
    'depends': [
        'base', 
        'mail', 
        'hr', 
        
    ],
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'security/hr_setup_security.xml',
        'views/hr_averange_effective_rate_views.xml',
        'views/hr_family_category_views.xml',
        'views/hr_employee_inherit_views.xml',

    ],
    # 'post_init_hook': 'post_init_hook',
    'application': False,
    'installable': True,
    'auto_install' : False,
    "external_dependencies": {"python": []},
}