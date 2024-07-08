# Arkana Training
Arkana Training - Internal

## CARA MEMBUAT NEW MODULE ODOO ARKANA_BASE_TRAINING (UBUNTU)

Setelah Odoo dan database odoo16_arkana_training berhasil di buat dan berjalan dengan baik, maka untuk memulainya kita membuat sebuah modul baru. Odoo telah menyiapkan fitur yang bernama SCAFFOLD, yang berfungsi untuk membuat template modul secara instan yang mengandung komponen default pada sebuah modul Odoo.

1. Pertama-tama, Buat Folder modul baru bernama arkana_base_training :
Buka terminal dan navigasikan ke direktori yang sebelumnya kita telah buat. Lalu, buat folder projectnya dengan perintah:
```bash
#masuk ke folder yang sebelumnya telah di buat
cd project
cd arkana_training
# membuat folder modul
mkdir arkana_base_training
```

2. Selanjutnya Scaffold.
Untuk membuat kerangka kerja pada modul yang telah kita buat sebelumnya, maka di perlukan inisialisasi menggunakan scaffold dengan perintah berikut :

```bash
#Inisialisasi Scaffold
scaffold init arkana_base_data
```
Setelah kita mengeksekusi perintah di atas, maka pada folder project arkana_base_data kita akan tercipta sebuah modul baru dengan struktur sebagai berikut :
```bash
arkana_base_training
…. controllers
……… __init__.py
……… controllers.py
…. demo
……… demo.xml
…. models
……… __init__.py
……… models.py
…. security
……… ir.model.access.csv
…. views
……… templates.xml
……… views.xml
…. __init__.py
…. __manifest__.py
```
Pada hirarki diatas, maka struktur MVC (Model View Controller) sudah terbentuk dengan adanya pembagian hirarki berdasarkan folder.

3. Setelah itu konfigurasi file (__manifest__.py) sesuai dengan kebutuhan:

```bash
# Install
# -*- coding: utf-8 -*-
{
    'name': "training_odoo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
 
    'description': """
        Long description of module's purpose
    """,
 
    'author': "My Company",
    'website': "https://www.yourcompany.com",
 
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
 
    # any module necessary for this one to work correctly
    'depends': ['base'],
 
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install' : False,
    "external_dependencies": {"python": []},
}

```
## Membuat Model Di Dalam Module 'Arkana Base Training'

1. Buat 3 models "hr_average_effective_rate.py","hr_employee.py" dan "hr_family_category.py" di dalam folder "models" pada module "Arkana Base Training".

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py
……… hr_family_category.py
```

2. Selanjutnya, sesuaikan "__init__.py" pada folder "models"

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py

#penyesuaian __init__.py
from . import hr_family_category
from . import hr_average_effective_rate
from . import hr_employee
```

 3. Lalu, Menambahkan 2 model "HrAverageEffectiveRate" dan "HrAverageEffectiveRateLine" pada (hr_average_effective_rate.py) 

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py

#hr_average_effective_rate.py

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
```
4. Lalu, Menambahkan model "HrEmployee" dan pada (hr_employee.py) 

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py

#hr_employee.py
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

```
5. Terakhir, Menambahkan model "HrFamilyCategory" dan pada (hr_family_category.py).

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py
……… hr_family_category.py

#hr_family_category.py
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

    #compute for name
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
```
Dari ketiga model yang di buat, kita dapat menyimpulkan bahwa modul ini dirancang untuk memperluas dan memperkaya fitur manajemen pegawai. Berikut adalah beberapa poin utama dari ketiga model tersebut:

 1. HrEmployee Model:

    -Menambahkan bidang family_category_id yang terhubung dengan model 'hr.family.category' untuk mengelola kategori keluarga pegawai.

    -Menambahkan bidang average_effective_rate_id yang terkait dengan 'hr.average.effective.rate' melalui kategori keluarga.

    -Menggunakan metode dan onchange untuk mengatur dan menghitung nilai default untuk kategori keluarga berdasarkan status pernikahan dan daftar kategori keluarga yang tersedia.

 2. HrFamilyCategory Model:

    -Menyediakan model untuk mengelola kategori keluarga pegawai dengan bidang seperti name, family_status, number, ptkp_amount, dan lainnya.

    -Memiliki constrain untuk mencegah duplikasi data kategori keluarga berdasarkan nama, perusahaan, dan ID yang berbeda.

    -Menggunakan metode _compute_name untuk mengisi bidang name berdasarkan status keluarga dan jumlah anggota keluarga.

 3. HrAverageEffectiveRate Model:

    -Menambahkan bidang average_effective_rate_id pada model 'hr.employee' yang terhubung dengan 'hr.average.effective.rate'.

    -Menggunakan metode dan onchange untuk mengelola dan menghitung nilai default untuk bidang family_category_id berdasarkan status pernikahan pegawai dan daftar kategori keluarga yang tersedia.

    -Menyediakan fungsi untuk menghitung jumlah baris terkait dengan tingkat efektif rata-rata pada model 'hr.average.effective.rate'.

## Membuat Views Di Dalam Module 'Arkana Base Training'

1. Buat 3 view "hr_average_effective_rate_views.xml","hr_employee_inherit_views.xml" dan "hr_family_category_views.xml" di dalam folder "views" pada module "Arkana Base Training".

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py
……… hr_family_category.py
…. views
……… hr_average_effective_rate_views.xml
……… hr_employee_inherit_views.xml
……… hr_family_category_views.xml
```

2. Setelah itu tambahkan ke 3 views yang telah kita buat ke dalam (__manifest__.py) pada bagian 'data':

```bash
#__manifest__.py
'data': [
        'views/hr_family_category_views.xml',
        'views/hr_averange_effective_rate_views.xml',
        'views/hr_employee_inherit_views.xml',
        ]
```

3. Lalu, selanjutnya kita buat Beberapa elemen utama dalam views ini melibatkan tampilan daftar (tree view) dan tampilan formulir (form view) serta menuitem untuk entitas "hr.average.effective.rate".

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py
……… hr_family_category.py
…. views
……… hr_average_effective_rate_views.xml

#tree view & form view dari hr_average_effective_rate.xml
 <!-- viewstree rate   -->
    <record id="hr_average_effective_rate_view_tree" model="ir.ui.view">
        <field name="name">hr.average.effective.rate.view.tree</field>
        <field name="model">hr.average.effective.rate</field>
        <field name="arch" type="xml">
            <tree string="TER Information">
                <field name="name"/>
                <field name="line_ids_count"/>
                <field name="company_id"/> 

            </tree>
        </field>
    </record>

    <!-- views form rate -->
    <record id="hr_average_effective_rate_view_form" model="ir.ui.view">
        <field name="name">hr.average.effective.rate.view.form</field>
        <field name="model">hr.average.effective.rate</field>
        <field name="arch" type="xml">
            <form string="TER Detail Info">
                <sheet>

                    <div class="oe_title">
                        <label for="name" />
                        <h1><field
                            name="name"
                            required="1"
                            placeholder="e.g. A"
                        /></h1>
                    </div>

                    <group name="line_ids_count" string="General/ Information"> 
                        <field name="line_ids_count"/>
                        <field name="company_id" readonly="1" 
                            options="{'no_create' : True, 'no_open' : True}"/> 
                        <field name="currency_id" readonly="1" options="{'no_create' : True, 'no_open' : True}"/>
                    </group>

                    <notebook>
                        <page string="TER Rules Detail" name="ter_rules_detail">
                            <field name="line_ids" class="mx-1">
                                <tree editable="bottom">
                                    <field name="average_effective_rate_id" readonly="1" invisible="1" 
                                        options="{'no_create' : True, 'no_open' : True}" />
                                    <field name="currency_id" readonly="1" invisible="1" 
                                        options="{'no_create' : True, 'no_open' : True}" />
                                    <field name="sequence" readonly="1" invisible="1" />
                                    <field name="minimal_amount" widget="monetary" 
                                        options="{'currency_field': 'currency_id'}"/>
                                    <field name="maximum_amount" widget="monetary" 
                                        options="{'currency_field': 'currency_id'}"/>
                                    <field name="percentage"/>
                                </tree>
                                <form>
                                    <group>
                                    <field name="minimal_amount" widget="monetary" 
                                        options="{'currency_field' : 'currancy_id'}" />
                                    <field name="maximum_amount" widget="monetary" 
                                        options="{'currency_field' : 'currancy_id'" />
                                    <field name="percentage" readonly="1" invisible="1"
                                        options="{'currency_field': 'currency_id'}"/>
                                    </group>
                                </form>
                            </field>
                        </page>
                    </notebook>

                </sheet>
            </form>
        </field>
    </record>

    <record id="hr_average_effective_rate_action" model="ir.actions.act_window">
        <field name="name">TER Information</field>
        <field name="type">ir.actions.act_window</field>
        <field name="res_model">hr.average.effective.rate</field>
        <field name="view_mode">tree,form</field>
        <field name="domain">[]</field>
        <field name="context">{}</field>
        <field name="help" type="html">
            <p/>
        </field>
    </record>

    <record id="hr_average_effective_rate_action_tree" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">tree</field>
        <field name="act_window_id" ref="hr_average_effective_rate_action"/>
        <field name="view_id" ref="hr_average_effective_rate_view_tree"/>
    </record>

    <record id="hr_average_effective_rate_action_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">form</field>
        <field name="act_window_id" ref="hr_average_effective_rate_action"/>
        <field name="view_id" ref="hr_average_effective_rate_view_form"/>
    </record>

#menuitem
<menuitem id="menu_action_average_effective_rate" 
        name="TER Information" 
        action="hr_average_effective_rate_action" 
        parent="hr.menu_config_employee" sequence="99" groups="hr.group_hr_manager" />
```

4. Lalu, kita buat sebuah penyesuaian (inheritance) dari tampilan formulir (form view) untuk model "hr.employee"


```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py
……… hr_family_category.py
…. views
……… hr_average_effective_rate_views.xml
……… hr_employee_inherit_views.xml

#hr_employee_inherit_views.xml
<record id="view_employee_form_inherit_customization" model="ir.ui.view">
        <field name="name">hr.employee.view.form.inherit.customization</field>
        <field name="model">hr.employee</field>
        <field name="inherit_id" ref="hr.view_employee_form"/>
        <field name="arch" type="xml">

            <xpath expr="//notebook/page[@name='personal_information']/group[1]/group[2]/field[@name='children']" position="after">
                <field name="family_category_ids" invisible="1"/>
                <field name="family_category_id" options="{'no_create' : True, 'no_open' : True}"
                        domain ="[('id', 'in', family_category_ids)]"/>
                <field name="average_effective_rate_id" string="TER" force_save="1" readonly="1"
                        options="{'no_create' : True, 'no_open' :True}" />
            </xpath>
            
        </field>
    </record>
```

5. Lalu, selanjutnya kita buat Beberapa elemen utama dalam views ini melibatkan tampilan daftar (tree view) dan action (action view) serta menuitem untuk entitas "hr.family.category".

```bash
#Struktur Direktori
arkana_base_training
…. models
……… __init__.py
……… hr_average_effective_rate.py
……… hr_employee.py
……… hr_family_category.py
…. views
……… hr_average_effective_rate_views.xml
……… hr_employee_inherit_views.xml
……… hr_family_category_views.xml

#hr_employee_inherit_views.xml
<record id="hr_family_category_view_tree" model="ir.ui.view">
        <field name="name">hr.family.category.view.tree</field>
        <field name="model">hr.family.category</field>
        <field name="arch" type="xml">
                    <tree string="Family Category" default_order="company_id asc, name asc" edit="1" editable="bottom" multi_edit="1">
                        <field name="name"/>
                        <field name="family_status" required="1"/>
                        <field name="number" required="1"/>
                        <field name="average_effective_rate_id" required="1" options="{'no_create' : True,'no_open' : True}"/>
                        <field name="ptkp_amount" options="{'currancy_field' : True,'curancy_id' : True}"/>
                        <field name="mark_as_married_state"/>
                        <field name="active" optional="hide" force_save="1" readonly="1"/>
                        <field name="company_id" optional="hide" force_save="1" readonly="1"/>
                        <field name="currency_id" optional="hide" force_save="1" readonly="1"
                                options="{'no_create' : True,'no_open' : True}"/>
                    </tree>
        </field>
    </record>   
    
    <record id="hr_family_category_action" model="ir.actions.act_window">
        <field name="name">Family Category</field>
        <field name="res_model">hr.family.category</field>
        <field name="view_mode">tree</field>
        <field name="domain">[]</field>
        <field name="context">{}</field>
        <field name="help" type="html">
            <p/>
        </field>
    </record>
    <record id="hr_family_category_action_tree" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">tree</field>
        <field name="act_window_id" ref="hr_family_category_action"/>
        <field name="view_id" ref="hr_family_category_view_tree"/>
    </record>

#menuitem
<menuitem id="menu_hr_family_category" 
    name="Family Category" 
    action="hr_family_category_action" 
    parent="hr.menu_config_employee"  
    sequence="99" 
    groups="hr.group_hr_manager"/>
```
Kesimpulan singkat dari ketiga code view yang telah kita buat tersebut adalah sebagai berikut:

1. HrFamilyCategory Model:

    -Merepresentasikan model "hr.family.category" dengan beberapa bidang seperti "active", "company_id", "currency_id", "name", "family_status", "number", "ptkp_amount", "mark_as_married_state", dan "average_effective_rate_id".

    -Melibatkan komputasi otomatis untuk bidang "name" dan validasi untuk mencegah data dengan nama yang sama.

    -Terdapat relasi dengan model lain, yaitu "hr.average.effective.rate".

2. HrFamilyCategory Tree View (hr_family_category_view_tree):

    -Menyediakan tampilan daftar (tree view) untuk model "hr.family.category" dengan beberapa kolom yang dapat diubah dan diurutkan secara default berdasarkan "company_id" dan "name".

    -Beberapa kolom memiliki aturan wajib diisi, opsi untuk menyembunyikan, atau hanya-baca.

    -Terdapat opsi untuk mencegah pembuatan dan pembukaan baru untuk beberapa kolom.

3. HrFamilyCategory Action and Menu (hr_family_category_action, hr_family_category_action_tree, menu_hr_family_category):

    -Membuat aksi window dan tampilan terkait untuk menampilkan tampilan daftar "hr_family_category_view_tree".

    -Menambahkan item menu "Family Category" yang akan membuka aksi window tersebut.

    -Menetapkan urutan dan pengaturan akses untuk item menu, sehingga hanya dapat diakses oleh grup pengguna tertentu.

## Selanjutnya mengatur security dari module 'Arkana Base Training'