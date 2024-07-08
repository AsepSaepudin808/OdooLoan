from odoo import _, api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    loan_approver_id = fields.Many2one('res.users', string='Loan Approver',
                            index=True, copy=False, tracking = True, ondelete='set null', 
                            domain="[('company_ids', '=',company_id)]")
    company_currency_id = fields.Many2one(string = 'Company Currancy', 
                                    related = 'company_id.currency_id', readonly = True)
    limit_amount = fields.Monetary('Limit Amount(petty cash)', currency_field = 'company_currency_id')