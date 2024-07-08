from odoo import Command, api, models, _
import json, os

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    @api.model_create_multi
    def create(self, values):
        company = super().create(values)
        company._create_tax_components_setup()
        return company

    def _create_tax_components_setup(self):
        aer_type_id = self.env['hr.average.effective.rate']
        family_category_id = self.env['hr.family.category']
        for rec in self:
            datas, result, values = {}, [], []
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open('{}/../data/personal_income_tax_setup.json'.format(dir_path)) as f:
                datas = json.load(f)
                
            for data in datas['average_effective_rate_type']:
                lines = []
                for record in data['lines']:
                    lines.append((0, 0, {
                    
                    "minimal_amount": record['minimal_amount'],
                    "maximum_amount": record['maximum_amount'],
                    "percentage": record['percentage']}))
                res = aer_type_id.sudo().create({'company_id' : rec.id, 'name' : data['name'], 'line_ids' : lines})
                result.append({'average_effective_rate_id' : res.id, 'name' : res.name})
            
            for data in datas['family_category']:
                aer_type = next((res for res in result if res['name'] == data['average_effective_rate_id']), False)
                data['average_effective_rate_id'] = aer_type['average_effective_rate_id']
                data['company_id'] = rec.id
                values.append(data)
            
            family_category_id.sudo().create(values)
        return True
