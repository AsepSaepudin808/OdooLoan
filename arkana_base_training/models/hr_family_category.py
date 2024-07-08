from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrFamilyCategory(models.Model):
    _name = 'hr.family.category'
    _description = 'HrFamilyCategory'
    _rec_name = 'name'
    _order = 'name asc, ptkp_amount asc'

    active = fields.Boolean('Active', default = True)
    company_id = fields.Many2one('res.company', string='Company',
                                
                                default = lambda self:self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                copy =False, related='company_id.currency_id',
                                store=True)
    name = fields.Char(compute='_compute_name', string='name',
                        store=True, index='trigram')
    family_status = fields.Selection([
        ('k', 'K'),
        ('tk', 'TK')
    ], string='Family Status', default='tk')
    number = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ], string='Number', default='0')
    ptkp_amount = fields.Monetary('PTKP Amount', currency_field='currency_id')
    mark_as_married_state = fields.Boolean('Mark As Married State', default = False)
    average_effective_rate_id = fields.Many2one('hr.average.effective.rate', 
                                                domain="[('company_id', '=', company_id)]",
                                                string='Average Effective ID', index = True,
                                                ondelete='restrict')

    #compute untuk name
    @api.depends('family_status', 'number')
    def _compute_name(self):
        for rec in self:
            if rec.family_status and rec.number:
                family_status = dict(self.env[rec._name].fields_get(allfields=['family_status'])['family_status']['selection'])[rec.family_status]
                number = dict(self.env[rec._name].fields_get(allfields=['number'])['number']['selection'])[rec.number]
                rec.name = "{}/{}".format(family_status, number)
            else:
                rec.name = '/'
    #privent for duplicated data
    @api.constrains('name')
    def _constrains_name(self):
        for rec in self:
            family_category_id = self.search([('name', 'm', rec.name),
                                            ('id', '!=', rec.id),
                                            ('company_id', '=', rec.company_id)])
            if family_category_id:
                raise ValidationError('Data Exist for this name')