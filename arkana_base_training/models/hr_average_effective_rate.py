from odoo import _, api, fields, models

class HrAverageEffectiveRate(models.Model):
    _name = 'hr.average.effective.rate'
    _description = 'Average Effective Rate'
    
    company_id = fields.Many2one('res.company', string='Company', 
                                index = True, copy = False,
                                default = lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                copy = False, related='company_id.currency_id',
                                store=True)
    name = fields.Char('Name')
    line_ids = fields.One2many('hr.average.effective.rate.line', 'average_effective_rate_id',
                            string='Line IDS')
    line_ids_count = fields.Integer(compute='_compute_line_ids_count', string='Line Count')
    
    @api.depends('line_ids')
    def _compute_line_ids_count(self):
        for rec in self:
            if rec.line_ids:
                rec.line_ids_count = len(rec.line_ids)
            else:
                rec.line_ids_count = 0

class HrAverageEffectiveRateLine(models.Model):
    _name = 'hr.average.effective.rate.line'
    _description = 'Average Effective Rate Line'
    
    average_effective_rate_id = fields.Many2one('hr.average.effective.rate', 
                                string='Average Effective Rate', index = True,
                                copy = False)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                copy = False, related='average_effective_rate_id.currency_id',
                                store=True)
    sequence = fields.Integer(default=10)
    minimal_amount = fields.Monetary(
        string="Min. Amount",
        currency_field='currency_id',
        store=True, readonly=False, required=True)
    maximum_amount = fields.Monetary(
        string="Max. Amount",
        currency_field='currency_id',
        store=True, readonly=False, required=True)
    percentage = fields.Float(
        string="Percentage",
        digits=(2,4),
        store=True, readonly=False, required=True)