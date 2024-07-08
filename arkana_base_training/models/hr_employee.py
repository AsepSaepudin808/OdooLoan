from odoo import _, api, fields, models

class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee']
    _description = 'Employee'

    family_category_id = fields.Many2one('hr.family.category', string='Family Category',
                                        index = True, copy = False, tracking = True,
                                        ondelete='restrict')
    average_effective_rate_id = fields.Many2one('hr.average.effective.rate', 
                                        string='Average Effective Rate',
                                        related = 'family_category_id.average_effective_rate_id')

    family_category_ids = fields.Many2many('hr.family.category',
                                            compute='_compute_family_category_ids', 
                                            string='Family Category Domain')
    
    #Fetch Family Category List
    def _get_list_of_family_category_ids(self, marital=False):
            domain = [('company_id', 'in', self.env.company.ids), ('mark_as_married_state', '=', True)] if marital == 'married'\
                else [('company_id', 'in', self.env.company.ids), ('mark_as_married_state', '=', False)] if marital not in ['married',False]\
                    else [('company_id', 'in', self.env.company.ids)]

            family_category_ids = self.env['hr.family.category'].sudo().search(domain, order='id asc')
            return family_category_ids

    #Domain for family category based on marital status
    @api.depends('marital')
    def _compute_family_category_ids(self):
        for rec in self:
            family_category_ids = rec._get_list_of_family_category_ids()
            rec.family_category_ids = family_category_ids if len(family_category_ids)>0 else False

    #choose default family category based on marital status and famely category lists datas
    @api.onchange('marital')
    def _onchange_marital(self):
        for rec in self :
            family_category_ids = rec._get_list_of_family_category_ids()
            rec.family_category_id = family_category_ids[0] if len(family_category_ids)>0 else False
