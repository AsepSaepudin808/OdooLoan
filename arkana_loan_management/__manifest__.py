# -*- coding: utf-8 -*-
{
    'name': "Arkana - Loan Management",
    'summary': "Arkana - Loan Managemant",
    'description': "Arkana - Loan Management",
    'author': "PT. Arkana Solusi Digital",
    'mainteners':["AsepSaepudin808"],
    'website': "https://arkana.co.id",
    'category': 'Human Resources/Employees',
    'version': '16.0.1.0.0',

    #any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'hr',
                'arkana_base_training',
    ],
    'license': 'OPL-1',

    # always loaded
    'data': [
        'security/hr_loan_role.xml',
        'security/ir.model.access.csv',
        'security/hr_loan_security.xml',
        'data/hr_loan_seq_data.xml',
        'data/hr_loan_cron.xml',
        'report/hr_loan_report_view.xml',
        'views/hr_loan_line_views.xml',
        'views/hr_loan_line_analysis_view.xml',
        'views/hr_employee_inherit_views.xml',
        'views/hr_loan_kasbon_views.xml',
        'views/hr_loan_loan_views.xml',
        'views/hr_loan_menu_views.xml',
        'wizard/hr_loan_report_wizard_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install' : False,
    "external_dependencies": {"python": []},
}
