from odoo import models, fields, api

class CustomResPartner(models.Model):
    _inherit = 'res.partner'
    
    ref = fields.Char('Reference')

    @api.model
    def create(self, vals):
        # Memanggil fungsi create dari superclass untuk membuat partner
        res = super(CustomResPartner, self).create(vals)

        # Melakukan override pada field 'Ref' berdasarkan kondisi is_company
        if res and res.id:
            if res.is_company:
                res.ref = 'CMPY-%04d' % res.id
            else:
                res.ref = 'IDVD-%04d' % res.id

        return res

    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        # Inisialisasi args jika tidak ada
        args: args or []

        # Membuat domain untuk pencarian berdasarkan 'name' dan 'ref'
        domain=['|',('name', operator, name), ('ref', operator, name)]

        # Melakukan pencarian berdasarkan domain dan argumen, dengan batasan hasil pencarian
        partners = self._search(domain, limit=limit)
        return partners

    def name_get(self):
        result = []
        for record in self:
            if record.ref:  # Jika 'Ref' terisi, tambahkan 'Ref' ke dalam nama partner
                result.append((record.id, f"{record.ref} - {record.name}"))
            else:
                # Jika 'Ref' tidak terisi, gunakan nama partner default dari Odoo
                result.append((record.id, record.name))
        return result
