import requests
from odoo import models, fields, api
from odoo.exceptions import UserError

class PartnerWizard(models.TransientModel):
    _name = 'arkana.partner.wizard'
    _description = 'Wizard untuk memilih Kategori dan Produk'

    wizard_selection = fields.Selection([
        ('category', 'Category'),
        ('product', 'Product')
    ], string='Wizard')

    def apply_wizard(self):
        for wizard in self:
            data = False
            if wizard.wizard_selection == 'category':
                # Jika yang dipilih adalah Kategori
                # Mengambil data produk dari API eksternal
                response = requests.get('https://dummyjson.com/products/categories')
                response.raise_for_status()  # Memunculkan error untuk respons yang buruk
                data = response.json()

                # Menyiapkan nilai untuk membuat kategori produk baru
                category_values = []
                for product in data:
                    # print(product)
                    category = self.env['product.category'].search([('name', '=', product)], limit=1)

                    # Jika kategori ada, gunakan ID-nya; jika tidak, atur ke False
                    category_id = True if category else False

                    if not category_id:
                        category_values.append({
                            'name': product,
                        })

                # Membuat kategori produk baru di Odoo
                self.env['product.category'].create(category_values)
                

            elif wizard.wizard_selection == 'product':
                # Jika yang dipilih adalah Produk
                # Mengambil data produk dari API eksternal
                response = requests.get('https://dummyjson.com/products')
                response.raise_for_status()  # Memunculkan error untuk respons yang buruk
                products_data = response.json()
                products_data = products_data['products']
            # print(products_data,'EEEEEEEEEEEEEEEE')

                # Memproses setiap produk dan membuat/memperbarui rekaman Produk di Odoo
                product_obj = self.env['product.product']
                category_obj = self.env['product.category']

                product_values = []
                for product in products_data:
                    product_name = product['title']

                    # Mencari kategori produk di Odoo
                    # Jika kategori ada, gunakan ID-nya; jika tidak, atur ke False
                    category_id = category_obj.search([('name', '=', product['category'])], limit=1)
                    category_id = category_id if category_id else False

                    # Mencari produk di Odoo
                    produk = product_obj.search([('name', '=', product['title'])], limit=1)
                    produk = True if produk else False

                    # Menyiapkan nilai untuk membuat/memperbarui produk
                    if not produk:
                        product_values.append({
                            'name': product_name,
                            'description': product.get('description', ''),
                            'categ_id': category_id.id,
                        })

                # Membuat atau memperbarui produk di Odoo
                self.env['product.product'].create(product_values)

        # except requests.RequestException as e:
        #     raise UserError(f"Gagal mengambil data produk: {str(e)}")