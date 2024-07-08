# Arkana Training
Arkana Training - Internal

## NEW MODULE ODOO ARKANA LOAN MANAGEMENT PADA PROJECT 'ARKANA TRAINING' 

Setelah Odoo berjalan dengan baik, maka untuk membuatnya kita harus membuat sebuah folder baru. Odoo telah menyiapkan fitur yang bernama SCAFFOLD, yang berfungsi untuk membuat template modul secara instan yang mengandung komponen default pada sebuah modul Odoo.

1. Pertama-tama, Buat Folder modul baru bernama arkana_loan_management :
```bash
# Masuk ke Folder yang sebelumnya telah di buat
cd project
cd arkana-training
# membuat folder modul
mkdir arkana_loan_management
```

2. Selanjutnya Scaffold.
Untuk membuat kerangka kerja pada folder modul arkana_loan_management yang telah kita buat sebelumnya, maka di perlukan inisialisasi menggunakan scaffold dengan perintah berikut :

```bash
#Inisialisasi Scaffold
scaffold init arkana_loan_management
```
Setelah kita mengeksekusi perintah di atas, maka pada folder project arkana_loan_management kita akan tercipta sebuah struktur modul sebagai berikut :
```bash
arkana_loan_management
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
Pada hirarki diatas, struktur MVC (Model View Controller) sudah terlihat dengan adanya pembagian hirarki berdasarkan folder. Sama halnya seperti konsep MVC yang lain, masing-masing folder memiliki fungsi tersendiri, penjelasan ringkasnya sebagai berikut :

    A. Controllers = Berisi file python yang mengandung perintah untuk komunikasi model & view (untuk website/front-end)

    B. Demo = Berisi file xml yang mengandung data untuk demo (saat create database centang “Demo Data”)

    C. Models = Berisi file python yang mengandung perintah untuk menggunakan ORM seperti membuat model, inherit, dll

    D. Security = Berisi file csv yang mengandung akses right pada setiap model (tabel) dan file xml untuk membuat group sesuai kebutuhan akses right

    E. Views = Berisi file xml yang mengandung syntax untuk membuat berbagai tampilan view seperti list, form, kanban, calendar, pivot, graph, dll

    Nantinya kita juga bisa menambahkan beberapa folder lagi sesuai kebutuhan seperti report, wizard, i18n, static, dll. Seperti berikut :

    F. Report = Berisi file python sebagai parsing datanya dan xml sebagai file action dan template reportnya

    G. Wizard = Berisi file python dan xml untuk membuat model & view dari suatu wizard (model on the fly)

    H. i18n = Berisi file translator

    I. Static = Berisi file pendukung seperti javascript, css, image, dll

    Disamping folder diatas, modul yang telah kita buat juga mengandung 2 file yaitu : __init__.py dan __manifest__.py yang memiliki fungsi seperti berikut ini :

    J. __init__.py

    File ini berfungsi untuk menjadikan folder biasa menjadi modul python. Karna Odoo dikembangkan dengan python, maka modul odoo harus dikenali oleh python. File ini juga berfungsi sebagai constructor sebagaimana pada file python, Odoo akan membaca file ini pertama kali saat diinstal. Pada file ini kita harus mengimport semua folder yang mengandung file python dan mengimport file python yang sejajar dengan file __init__ ini jika ada

    K. __manifest__.py

    File ini berfungsi untuk menjadikan folder biasa menjadi modul Odoo. Fungsinya sama seperti file __openerp__.py pada versi odoo sebelumnya. File ini berisi sebuah dictionary python yang memiliki beberapa key dan mengandung informasi bagi user saat ingin menginstall modul terkait.

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
}

```
Penjelasan untuk masing-masing key dictionary ringkasnya sebagai berikut :

    name (string) : Nama modul

    summary (string) : Ringkasan fungsi modul

    description (string) : Penjelasan fungsi modul

    author (string) : Pembuat modul

    website (string) : Informasi website modul

    category (string) : Category modul

    version (string) : Versi modul

    depends (list) : Nama modul yang diisi akan otomatis terinstall saat modul ini diinstal

    data (list) : Daftar file xml & csv dari semua folder yang ingin di eksekusi

    demo (list) : Daftar file xml dari folder demo

    qweb (list) : Akan meload file xml (Isinya file dari folder static)

    installable (boolean) : Jika diisi True, maka modul dapat diinstal

    application (boolean) : Jika diisi True, modul akan terfilter sebagai Apps

    auto_install (boolean) : Jika diisi True, modul akan otomatis terinstall saat pembuatan database


## Membuat Model di dalam Module 'Arkana Loan Management'

1. Buat 2 models "hr_employee.py" dan "hr_loan.py" di dalam folder "models" pada module "Arkana Loan Management".

```bash
#Struktur Direktori
arkana_loan_management
…. models
……… __init__.py
……… hr_employee.py
……… hr_loan.py
```
2. Selanjutnya, sesuaikan "__init__.py" pada folder "models".

```bash
from . import hr_employee
from . import hr_loan

```
3. Lalu, Membuat Models 'HrEmployee' pada (hr_employee.py)

```python
#Struktur Direktori
arkana_base_management
…. models
……… __init__.py
……… hr_employee.py

#hr_employee.py

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    loan_approver_id = fields.Many2one('res.users', string='Loan Approver',
                            index=True, 
                            copy=False, 
                            tracking = True, 
                            ondelete='restrict', 
                            domain="[('company_ids', '=',company_id)]")
    company_currency_id = fields.Many2one(string = 'Company Currancy', 
                                    related = 'company_id.currency_id', readonly = True)
    limit_amount = fields.Monetary('Limit Amount(petty cash)', currancy_field = 'company_currency_id')
```
Penjelasan :
  1.  _inherit = 'hr.employee': Mendeklarasikan bahwa model ini mengambil warisan dari model Odoo yang sudah ada, yaitu 'hr.employee'. Dengan ini, model HrEmployee akan memiliki semua kolom dan perilaku yang sudah didefinisikan dalam model 'hr.employee', dan kita dapat menambahkan atau memodifikasi perilaku tersebut.
  2.  _description = 'Employee':memberikan informasi singkat tentang tujuan atau fungsi dari model tersebut.
  3. fields loan_approver_id = sebagai relasi Many2one ke model 'res.users' (model pengguna dalam Odoo). ada Beberapa parameter yang di gunakan :
        *string='Loan Approver': Memberikan label untuk kolom ini.
        *index=True: Menyatakan bahwa indeks akan dibuat di database untuk kolom ini, mempercepat pencarian dan pengurutan.
        *copy=False: Menyatakan bahwa nilai kolom ini tidak boleh disalin saat mereplikasi rekaman.
        *tracking=True: Menandakan bahwa kolom ini akan dilacak untuk digunakan dalam sistem pelacakan perubahan.
        *ondelete='restrict': Menetapkan perilaku saat rekaman yang terkait dengan rekaman ini dihapus. Dalam hal ini, aksi hapus dibatasi ('restrict').
        *domain="[('company_ids', '=', company_id)]": Menyertakan domain untuk membatasi pilihan yang dapat dipilih dalam loan_approver_id berdasarkan kondisi tertentu, yaitu hanya pengguna dengan company_ids yang sama dengan company_id yang dapat dipilih.
    4. company_currency_id = Mendefinisikan kolom company_currency_id sebagai relasi Many2one ke model 'res.currency' yang terkait dengan company (company_id). Kolom ini bersifat hanya membaca (readonly). Ini berarti nilai untuk kolom ini akan diambil dari kolom currency_id pada  record company yang terkait.
    5. fields limit_amount = Mendefinisikan kolom limit_amount sebagai kolom Monetary (mata uang) dengan label 'Limit Amount(petty cash)'. Kolom ini juga menyertakan parameter currancy_field, yang menghubungkannya dengan kolom company_currency_id. Hal ini menunjukkan bahwa nilai untuk limit_amount akan disajikan dalam mata uang yang terkait dengan company.
    
4. Lalu, Membuat 2 Model 'HrLoan' dan 'HrLoanLine' pada (hr_loan.py).


```python
#Struktur Direktori
arkana_loan_management
…. models
……… __init__.py
……… hr_loan.py

#hr_loan.py

class HrLoan(models.Model):
    _name = 'hr.loan'
    _description = 'Loan'
    _inherit = ['mail.thread','mail.activity.mixin']

    def _get_default_employee_id(self):
        employee_ids = self.env.user.employee_ids.filtered(lambda r : r.company_id.id == self.env.company.id)
        return employee_ids[0] if len(employee_ids) > 0 else False

    loan_type = fields.Selection([
        ('petty_cash', 'Kasbon'),
        ('loan', 'Loan')
    ], string='Loan Type', tracking = True, copy = False, index = True)
    company_id = fields.Many2one('res.company', string ='Company',
                                                index =True, copy =False,
                                                default =lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string ='Currency',
                                copy =False, related ='company_id.currency_id',
                                store =True)
    name =fields.Char("Name", default ='New')
    state =fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
    ], string = 'State', default = 'draft', copy = False, tracking = True, index = True)
    start_date = fields.Date('Start Date', tracking = True, default=lambda self: fields.Date.to_string(date.today().replace(day=1)), index = True)
    end_date = fields.Date('End Date', tracking = True, compute = "_compute_end_date", readonly = False, store=True, index = True)
    employee_id = fields.Many2one('hr.employee', string = 'Employee', index = True, copy = False,
                                                    tracking = True, ondelete = 'restrict', default = '_get_default_employee_id')
    department_id = fields.Many2one('hr.department', string = 'Department', index = True,
                                                    store = True, compute = '_compute_employee_id', tracking = True, ondelete='set null')
    manager_id = fields.Many2one('hr.employee', compute='_compute_employee_id', string='Manager', store = True,
                                                    index=True, tracking=True, ondelete='set null')
    loan_approver_id = fields.Many2one('res.users', compute='_compute_employee_id', string='Approver', store = True,
                                                    index=True, tracking=True, ondelete='set null',
                                                    domain="[('company_ids', '=', company_id)]")
    limit_amount = fields.Monetary('Limit Amount', currency_field='currency_id', compute='_compute_employee_id', store=True, tracking=True)
    line_ids = fields.One2many('hr.loan.line', 'loan_id', string='Loan Line')
    total_amount= fields.Monetary(compute='_compute_total_amount', string='Total Amount', currency_field='currency_id', store=True)
    loan_line_count = fields.Integer(compute='_compute_loan_line_count', string='Loan Line Count')
    is_approver = fields.Boolean(compute='_compute_is_approver', string='Is Approver?')
    is_authorized_user = fields.Boolean(compute='_compute_is_authorized_user', string='Is Authorized User')

    residual_amount = fields.Monetary(compute='_compute_residual_amount', string='Residual Amount', store=True,
                                        currency_field='currency_id')
    residual_amount_percentage = fields.Float('Residual Amount Percentage',
                                        compute='_compute_residual_amount_percentage',
                                        digits=(3,2))

    @api.depends('limit_amount', 'total_amount')
    def _compute_residual_amount(self):
        for  rec in self:
            # residual_amount = rec.limit_amount.rec.total_amount
            residual_amount = rec.limit_amount - rec.total_amount
            rec.residual_amount = residual_amount
            # rec.residual_amount_percentage = residual_amount / rec.limit_amount

    @api.depends('residual_amount', 'limit_amount')
    def _compute_residual_amount_percentage(self):
        for  rec in self:
            limit_amount = rec.limit_amount if rec.limit_amount > 0 else 1
            rec.residual_amount_percentage = rec.residual_amount / limit_amount
    
    #Check Authorized User
    def _compute_is_authorized_user(self):
        for rec in self:
            rec.is_authorized_user = bool(rec.employee_id.user_id.id == self.env.user.id)\
                or bool(self.env.user.has_group('arkana_loan_management.group_loan_management_finance'))
    
    #Compute Is Approver User
    def _compute_is_approver(self):
        for rec in self:
            rec.is_approver = bool(rec.loan_approver_id.id == self.env.user.id)\
                or bool(self.env.user.has_group('arkana_loan_management.group_loan_management_administrator'))

    #Compute Loan Line Count
    @api.depends('line_ids', 'line_ids.state')
    def _compute_loan_line_count(self):
        for rec in self:
            rec.loan_line_count = len(rec.line_ids)

    #Compute End Date
    @api.depends('start_date')
    def _compute_end_date(self):
        next_month = relativedelta(month=+1, day=1, days=-1)
        for rec in self:
            rec.end_date = rec.start_date and rec.start_date + next_month

    #Compute Total Amount
    @api.depends('line_ids.amount', 'line_ids', 'line_ids.state')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.filtered(lambda x : x.state == 'confirm').mapped('amount'))

    #Compute Employee Data
    @api.depends('employee_id')
    def _compute_employee_id(self):
        for rec in self:
            if rec.employee_id:
                rec.department_id = rec.employee_id.department_id.id if rec.employee_id.department_id else False
                rec.loan_approver_id = rec.employee_id.loan_approver_id.id if rec.employee_id.loan_approver_id else\
                    rec.employee_id.parent_id.id if rec.employee_id.parent_id else False
                rec.manager_id = rec.employee_id.parent_id.id if rec.employee_id.parent_id else False
                rec.limit_amount = rec.employee_id.limit_amount if rec.employee_id.limit_amount else False
            
    #action to draft
    def action_set_to_draft(self):
        self.write({'state' : 'draft'})
        return True

    #Action to Confirm
    def action_confirm(self):
        values = {'state' : 'confirm'}
        for rec in(self):
            if rec.name == 'New':
                values['name'] = rec._generate_name_by_seq()
            rec.write(values)
            rec._send_message_to_partner(type="to_approve")
        return True

    #Action De
    def _get_default_message(self, type, line = False, line_name = False):
        if type == 'to_approve':
            return """ Dear <b> {} </b>,
                <br/>
                Please Approve the Request for Loan with
                Loan Number : <b> {} </b>
                <br/>
                Requested by: <b> {} </b>
                <br/>
                Created by: <b> {} </b>
                <br/>
                For Company: <b> {} </b>
                <br/>
            """.format(self.loan_approver_id.partner_id.name, self.name, 
                    self.employee_id.user_id.partner_id.name, 
                    self.env.user.partner_id.name, self.company_id.name)
        else:
            request = "Your Request" if not line else "Your Loan Line Request with Name : <b>{}</b>".format(line_name)
            action = 'Approved' if type in['approved', 'confirm'] else 'rejected'
            return """ 
                Dear <b> {} </b>,
                <br/>
                {} has been <b> {} </b> for Loan with
                Loan Number : <b> {} </b>
                <br/>
                <b> {} </b> by: <b> {} </b>
                <br/>
            """.format(self.employee_id.user_id.partner_id.name, request, action, self.name,
                action, self.loan_approver_id.partner_id.name)
    
    #Send Massage to Approver
    def _send_message_to_partner(self, type='to_approve', line = False, line_name = False):
        partner_ids = self.loan_approver_id.partner_id + \
            self.employee_id.user_id.partner_id + self.env.user.partner_id
        display_msg = self._get_default_message(type, line, line_name)
        self.message_post(body=display_msg, 
                    partner_ids=partner_ids.ids)
        return True

    #Generate Name by Sequence
    def _generate_name_by_seq(self):
        try:
            name = self.env['ir.sequence'].next_by_code('hr.loan.sequence')
            return name
        except Exception as err:
            raise ValidationError('Squence not found! %s'.err)

    #action to approve
    def action_approve(self):
        self.write({'state' : 'approved'})
        self._send_message_to_partner(type="approved")
        return True

    #action to rejected
    def action_rejected(self):
        self.write({'state' : 'rejected'})
        self._send_message_to_partner(type = 'rejected')
        return True

    def _get_loan_details_action(self):
        list_view_id = self.env.ref('').id
        form_view_id = self.env.ref('').id
        search_view_id = self.env.ref('').id
        return {
            'name': _('Loan Details'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.loan.line',
            'view_id': list_view_id,
            'search_view_id' : search_view_id,
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'domain' : [],
            'context' : {},
        }

    def _check_authorized_user(self):
        is_authorized = bool(self.employee_id.user_id.id == self.env.user.id) \
                or bool(self.env.user.has_group('arkana_loan_management.group_loan_management_finance'))
        return is_authorized

    #Action to Load Loan Details
    def action_load_loan_details(self):
        action = self.env.ref('arkana_loan_management.hr_loan_line_action').sudo().read()[0]
        action ['domain'] = [('loan_id', '=', self.id)]
        action ['context'] = {'default_loan_id' : self.id} if self.is_authorized_user else\
            {'default_loan_id' : self.id, 'create':0, 'edit':0, 'delete':0}
        return action


    def unlink(self):
        for rec in self:
            if rec.state != 'draft' or len(rec.line.ids.filtered(lambda x : x.state == 'confirm')) > 0:
                raise UserError("You can't Delete the Data because not in Draft State or has Confimed Lines")
        return super(HrLoan, self).unlink()

class HrLoanLine(models.Model):
    _name = 'hr.loan.line'
    _description = 'Loan Line'

    loan_id = fields.Many2one('hr.loan', string ='Loan ID', ondelete='cascade',
                                        index = True, copy=False)
    name = fields.Char(string='name', compute='_compute_name', store=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True,
                                store = True, related = 'loan_id.employee_id')
    loan_type = fields.Selection(string = 'Loan Type', related = 'loan_id.loan_type', store=True, index=True)
    company_id = fields.Many2one('res.company', string ='Company',
                                index = True, copy = False, 
                                related='loan_id.company_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                copy = False, related ='company_id.currency_id',
                                store = True)
    date = fields.Date('Date', default=fields.Date.context_today, index=True)
    amount = fields.Monetary('Amount', currency_field='currency_id')
    remarks = fields.Char(string ='Remarks')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('rejected', 'Rejected'),

    ], string='State', default='draft', copy=False, index=True)

    @api.model
    def create(self, vals):
        res = super(HrLoanLine, self).create(vals)
        res._check_authorized_user('Create')
        return res
    
    def write(self, vals):
        res = super(HrLoanLine, self).write(vals)
        self._check_authorized_user('Edit')
        return res

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("You can't Delete the Posted Data")
        return super(HrLoanLine, self).unlink()

    def _check_authorized_user(self, params):
        if not self.loan_id._check_authorized_user():
            raise ValidationError("You can't Access for {} this Data".format(params))

    @api.depends('date', 'loan_id')
    def _compute_name(self):
        for rec in self:
            name= '/'
            if rec.date and rec.loan_id:
                name = "{} - {}".format(rec.loan_id.name, rec.date.strftime('%d %m %y'))
            rec.name = name

    def action_set_state(self):
        state = self._context.get('state', False)
        datas = self.filtered(lambda x : x.state not in ['confirm', 'rejected'])
        line_name = ", ".join([data.name for data in datas]) if len(datas) > 1 else datas.name
        datas.write({'state' : state})
        datas.loan_id._send_message_to_partner(state, True, line_name)
        return True

    def action_confirm(self):
        state = self._contex.get('state', False)
        line_name = ",".join([data.name for data in self]) if len(self.ids) > 1 else self.name
        self.write({'state' : state})
        self.loan_id._send_message_to_partner(state, True, line_name)
        return False
```

5. Lalu, Membuat Model 'hr_employee.py' pada (hr_loan.py).

```bash
#Struktur Direktori
arkana_loan_training
…. models
……… __init__.py
……… hr_employee.py
……… hr_loan.py

#hr_employee.py
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
```

## Setting Security Pada Modul 'Arkana Loan Management'

1. Buat 'hr_loan_role.xml', 'hr_loan_security.xml' dan 'ir.model.access.csv' di folder 'arkana_loan_management/security'
```bash
#Struktur Direktori
arkana_loan_training
…. models
……… __init__.py
……… hr_employee.py
……… hr_loan.py
…. security
……… hr_loan_role.xml
……… hr_loan_security.xml
……… ir.model.access.csv

```
2. Impor file Security baru dengan menambahkan nama file security ke dalam data di 'manifest.py' seperti ini:

```bash
#Struktur Direktori
arkana_loan_training
…. models
……… __init__.py
……… hr_employee.py
……… hr_loan.py
…. security
……… hr_loan_role.xml
……… hr_loan_security.xml
……… ir.model.access.csv
....
……… __manifest__.py

#__manifest__.py
'data': [
    'security\hr_loan_role.xml',
    'security\ir.model.access.csv',
    'security\hr_loan_security.xml',
],
```
3. Buat rule User, Approver, Manager, Finance, dan Administrator pada 'hr_loan_role' dengan menggunakan code ini:
```xml
#Struktur Direktori
arkana_loan_management
…. models
……… __init__.py
……… hr_employee.py
……… hr_loan.py
…. security
……… hr_loan_role.xml

#hr_loan_role.xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="module_category_loan_management" model="ir.module.category">
        <field name="name">Loan Management</field>
        <field name="name"/>
        <field name="sequence">10</field>
    </record>
    <record id="group_loan_management_user" model="res.groups">
        <field name="name">User</field>
        <field name="category_id" ref="module_category_loan_management"/>
        <field name="implied_ids" eval="[(6, 0, [ref('base.group_user')])]"/>
    </record>
    <record id="group_loan_management_approver" model="res.groups">
        <field name="name">Approver</field>
        <field name="category_id" ref="module_category_loan_management"/>
        <field name="implied_ids" eval="[(6, 0, [ref('group_loan_management_user')])]"/>
    </record>
    <record id="group_loan_management_finance" model="res.groups">
        <field name="name">Finance</field>
        <field name="category_id" ref="module_category_loan_management"/>
        <field name="implied_ids" eval="[(4, ref('group_loan_management_finance'))]"/>
    </record>
    <record id="group_loan_management_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="category_id" ref="module_category_loan_management"/>
        <field name="implied_ids" eval="[(4, ref('group_loan_management_approver'))]"/>
    </record>
    <record id="group_loan_management_administrator" model="res.groups">
        <field name="name">Administrator</field>
        <field name="category_id" ref="module_category_loan_management"/>
        <field name="implied_ids" eval="[(6, 0, [ref('group_loan_management_manager')])]"/>
        <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
    </record>
</odoo>

```
4. Selanjutnya, buat data akses (permissions) yang digunakan untuk mengelola hak akses (permissions) pada 'ir.model.access.csv' dengan menggunakan code ini:

```bash
#Struktur Direktori
arkana_loan_management
….v models
……… __init__.py
……… hr_employee.py
……… hr_loan.py
….v security
……… hr_loan_role.xml
……… ir.model.access.csv

#ir.model.access.csv

id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hr_loan_user,access_hr_loan_user,arkana_loan_management.model_hr_loan,arkana_loan_management.group_loan_management_user,1,1,1,1
access_hr_loan_line_user,access_hr_loan_line_user,arkana_loan_management.model_hr_loan_line,arkana_loan_management.group_loan_management_user,1,1,1,1

access_hr_loan_approver,access_hr_loan_approver,arkana_loan_management.model_hr_loan,arkana_loan_management.group_loan_management_approver,1,1,1,1
access_hr_loan_line_approver,access_hr_loan_line_approver,arkana_loan_management.model_hr_loan_line,arkana_loan_management.group_loan_management_approver,1,0,0,0

access_hr_loan_manager,access_hr_loan_manager,arkana_loan_management.model_hr_loan,arkana_loan_management.group_loan_management_manager,1,1,1,1
access_hr_loan_line_manager,access_hr_loan_line_manager,arkana_loan_management.model_hr_loan_line,arkana_loan_management.group_loan_management_manager,1,0,0,0

access_hr_loan_finance,access_hr_loan_finance,arkana_loan_management.model_hr_loan,arkana_loan_management.group_loan_management_finance,1,1,1,1
access_hr_loan_line_finance,access_hr_loan_line_finance,arkana_loan_management.model_hr_loan_line,arkana_loan_management.group_loan_management_finance,1,1,1,1

access_hr_loan_report_,access_hr_loan_report_,arkana_loan_management.model_hr_loan,arkana_loan_management.group_loan_management_administrator,1,1,1,1
access_hr_loan_line_administrator,access_hr_loan_line_administrator,arkana_loan_management.model_hr_loan_line,arkana_loan_management.group_loan_management_administrator,1,1,1,1

access_hr_loan_report_wizard_user,access_hr_loan_report_wizard_user,arkana_loan_management.model_hr_loan_report_wizard,arkana_loan_management.group_loan_management_user,1,1,1,1
```

## Membuat View pada Modul 'Arkana Loan Management'

1. Membuat Icon Module
    1. Klik website : https://spilymp.github.io/ibo/
    2. Isilah field-field yang disediakan :

        a. Odoo Version : Odoo 15 (Pilih Odoo versi anda)

        b.  Icon Set : Font Awesome 5 Solid & Reguler 
            Pilih salah satu dari 8 website penyedia icon > Lalu klik icon bola dunia di sebelahnya  > Pilih salah satu icon yang diinginkan lalu copy nama classnya untuk point c.

        c.  Icon Class : fas fa-user-graduate
            Paste nama class dari point b tanpa tag class & tanpa tanda kutip

        d.  Icon Background Color : Selera Silahkan pilih warna backgorund yang sesuai selera

        e. Download icon dan rename menjadi 'loan_management.png'

        f.  Buat folder 'statis' di modul 'Arkana Loan Management', lalu buat folder 'statis/         deskripsi' dan pindahkan file yang diunduh ke lokasi tersebut

2. Buatlah 'hr_loan_kasbon_views.xml', 'hr_loan_kasbon_views.xml' dan 'hr_loan_loan_view.xml' di dalam folder 'arkana_loan_management/views'.

```bash
#Struktur Direktori
arkana_loan_management
….> models
….> security
….v views
……… hr_loan_kasbon_views.xml
……… hr_loan_loan_views.xml
……… hr_loan_menu_views.xml
```

3. lalu Impor nama file views baru dengan menambahkan lokasi file ke bagian data di 'manifest.py' seperti ini:

```bash
#Struktur Direktori
arkana_loan_management
….> models
….> security
….> views
....
……… 
………__manifest__.py

'data': [
    'security\hr_loan_role.xml',
    'security\ir.model.access.csv',
    'security\hr_loan_security.xml',
    'views\hr_loan_menu_views.xml',
    'views\hr_loan_kasbon_views.xml',
    'views\hr_loan_loan_views.xml',
],
```
4. Buat Tree,Form,Search,Action Views pada 'hr_loan_kasbon_views.xml'.

```xml
#Struktur Direktori
arkana_loan_management
….> models
….> security
….v views
……… hr_loan_kasbon_views.xml

#hr_loan_kasbon_views.xml

 <record id="hr_loan_kasbon_view_tree" model="ir.ui.view">
        <field name="name">hr.loan.view.tree</field>
        <field name="model">hr.loan</field>
        <field name="arch" type="xml">
            <tree string="Loan Management" decoration-success="state in ['approved', 'done']" 
                decoration-info="state == 'draft'" decoration-danger="state == 'rejected'">
                
                <field name="name"/>
                <field name="start_date"/>
                <field name="end_date"/>
                <field name="employee_id" readonly="1"/>
                <field name="department_id" readonly="1"/>
                <field name="loan_approver_id" readonly="1"/>
                <field name="manager_id" readonly="1"/>
                <field name="loan_type" widget="badge" decoration-success="loan_type in ['petty_cash']" 
                    decoration-warning="loan_type in ['loan']"/>

                <field name="limit_amount" options="{'currency_field' : 'currency_id'}"/>
                <field name="total_amount" options="{'currency_field' : 'currency_id'}"/>
                <field name="residual_amount" options="{'currency_field' : 'currency_id'}"/>

                <field name="state" widget="badge" decoration-success="state in ['approved', 'done']" 
                    decoration-info="state == 'draft'" decoration-warning="state == 'confirm'" 
                    decoration-danger="state == 'rejected'"/>

                <field name="create_uid" optional="show" force_save="1" readonly="1" 
                    options="{'no_open': True, 'no_create': True}"/>

                <field name="currency_id" invisible="1"/>
                <field name="company_id" optional="hide" readonly="1"/>

            </tree>
        </field>
    </record>

    <record id="hr_loan_kasbon_view_form" model="ir.ui.view">
        <field name="name">hr.loan.view.form</field>
        <field name="model">hr.loan</field>
        <field name="arch" type="xml">
            <form string="Loan Detail">

                <header>
                    <field name="is_approver" invisible="1" force_save="1"  readonly="1"/>
                    <button string="Confirm" name="action_confirm"  type="object" class="oe_highlight" states="draft"/>
                    <button string="Set to Draft" name="action_set_to_draft" type="object" class="oe_hinghlight" states="confirm,rejected"/>
                    <button string="Approve" name="action_approve" type="object" class="oe_highlight"
                            attrs="{'invisible':['|', ('state', '!=', 'confirm'), ('is_approver', '=', False)]}"/>
                    <button name="action_rejected" string="Rejected" type="object"
                            class="btn btn-danger text-upercase font-weight-bold"
                            attrs="{'invisible':['|', ('state','!=', 'confirm'), ('is_approver', '=', False)]}"/>
                    <button name="action_loan_report" string="Loan Report" type="object" class="oe_highlight" states="approved,done"/>
                    <button name="action_open_loan_report" string="Open Loan Report" type="object" class="btn btn-secondary font-weight-bold text-uppercase" states="approved,done"/>
                    
                    
                    <field name="state" widget="statusbar" statusbar_visible="draft,confirm,approved,done,rejected"/>
                </header>

                <sheet>

                    <div class="oe_button_box" name="button_box" attrs="{'invisible':[('state', '!=', 'approved')]}">
                        <button name="action_load_loan_details" type="object" class="oe_stat_button" icon="fa-info">
                            <field name="loan_line_count" string="Loan Details" widget="statinfo"/>
                        </button>
                    </div>
                    <field name="residual_amount_percentage" invisible="1"/>
                    <div class="alert alert-warning" role="alert"
                    attrs="{'invisible':['|',('residual_amount_percentage', '&gt;=', 0.20), 
                                            ('residual_amount_percentage', '&lt;=', 0.00)]}">
                    <strong> 
                        Your Residual Amount : <field name="residual_amount" force_save="1" readonly="1"
                        options="{'currency_field' : 'currency_id'}" attrs="{'invisible':[('state','=', 'draft')]}"/>
                    </strong>
                    </div>

                    <div class="alert alert-danger" role="alert"
                        attrs="{'invisible':[('residual_amount_percentage', '&gt;', '0.00')]}">
                        <strong/>
                        Your Residual Amount : <field name="residual_amount" force_save="1" readonly="1"
                        options="{'currency_field' : 'currency_id'}" attrs="{'invisible':[('state','=', 'draft')]}"/>
                        <strong/>
                    </div>

                    <div class="oe_title">
                        <label for="name"/>
                        <h1>
                            <field name="name"
                            force_save="1" readonly="1"/>
                        </h1>
                    </div>

                    <group string="General Information" name="general_information">
                        <group>
                            <field name="loan_type" required="1" readonly="1"/>
                            <label for="start_date" string="Period"/>
                            <div>
                                <field name="start_date" required="1" class="oe_inline" attrs="{'readonly': [('state', '!=', 'draft')]}"/> - 
                                <field name="end_date" required="1" class="oe_inline" attrs="{'readonly': [('state', '!=', 'draft')]}"/>
                            </div>
                            <field name="employee_id" required="1" options="{'no_create' : True, 'no_open' : True}" attrs="{'readonly': [('state', '!=', 'draft')]}"/>
                            <field name="department_id" force_save="1" readonly="1" options="{'no_create' : True, 'no_open' : True}"/>
                            <field name="manager_id" force_save="1" readonly="1" options="{'no_create' : True, 'no_open' : True}"/>
                            <field name="loan_approver_id" required="1" force_save="1" readonly="1" options="{'no_create' : True, 'no_open' : True}" attrs="{'readonly': [('state', '=', 'draft')]}"/>
                        </group>

                        <group>
                            <field name="limit_amount" force_save="1" readonly="1" 
                                options="{'currency_field' : 'currency_id'}"/>

                            <field name="total_amount" force_save="1" readonly="1"
                                options="{'currency_field' : 'currency_id'}"/>

                            <field name="residual_amount" force_save="1" readonly="1"
                                options="{'currency_field' : 'currency_id'}"/>

                            <field name="currency_id" force_save="1" readonly="1" invisible="1"
                                options="{'no_create' : True, 'no_open' : True}"/>
                                
                            <field name="company_id" force_save="1" readonly="1" invisible="1"
                                options="{'no_create' : True, 'no_open' : True}"/>
                        </group>
                    </group>
                </sheet>

                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="hr_loan_view_search" model="ir.ui.view">
        <field name="name">hr.loan.view.search</field>
        <field name="model">hr.loan</field>
        <field name="arch" type="xml">
            <search string="Loan Search">
                <field name="name"/>
                <field name="employee_id"/>
                <field name="loan_approver_id"/>
                <field name="department_id"/>
                <field name="manager_id"/>
                <separator/>

                <filter name="draft_state" string="Draft" domain="[('state', '=', 'draft')]"/>
                <filter name="confirm_state" string="Confirm" domain="[('state', '=', 'confirm')]"/>
                <filter name="approved_state" string="Approved" domain="[('state', '=', 'approved')]"/>
                <filter name="done_state" string="Done" domain="[('state', '=', 'done')]"/>
                <filter name="rejected_state" string="Rejected" domain="[('state', '=', 'rejected')]"/>
                <separator/>

                <filter name="last_month" string="Last Month" domain="['&amp;', ('start_date', '&gt;=', (context_today() + relativedelta(months=-1, day=1)).strftime('%Y-%m-%d')), ('start_date', '&lt;=', (context_today() + relativedelta(day=1, days=-1)).strftime('%Y-%m-%d'))]"/>
                <filter name="month" string="This Month" domain="['&amp;', ('start_date', '&gt;=', (context_today() + relativedelta(day=1)).strftime('%Y-%m-%d')), ('start_date', '&lt;=', (context_today() + relativedelta(months=1, day=1, days=-1)).strftime('%Y-%m-%d'))]"/>
                <separator/>

                <group expand="0" string="Group By">
                    <filter string="Employee" name="group_by_employee_id" domain="[]" context="{'group_by': 'employee_id'}"/>
                    <filter string="Manager" name="group_by_manager_id" domain="[]" context="{'group_by': 'manager_id'}"/>
                    <filter string="Loan Approver" name="group_by_loan_approver_id" domain="[]" context="{'group_by': 'loan_approver_id'}" />
                    <filter string="Department" name="group_by_department_id" domain="[]" context="{'group_by': 'department_id'}"/>
                    <filter string="Date" name="group_by_start_date" domain="[]" context="{'group_by': 'start_date:month'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="hr_loan_kasbon_action" model="ir.actions.act_window">
        <field name="name">Loan Management</field>
        <field name="res_model">hr.loan</field>
        <field name="view_mode">tree,form</field>
        <field name="domain">[('loan_type', '=', 'petty_cash')]</field>
        <field name="context">{'default_loan_type' : 'petty_cash'}</field>
        <field name="help" type="html">
            <p/>
        </field>
    </record>

    <record id="hr_loan_kasbon_action_tree" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">tree</field>
        <field name="act_window_id" ref="hr_loan_kasbon_action"/>
        <field name="view_id" ref="hr_loan_kasbon_view_tree"/>
    </record>

    <record id="hr_loan_kasbon_action_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">form</field>
        <field name="act_window_id" ref="hr_loan_kasbon_action"/>
        <field name="view_id" ref="hr_loan_kasbon_view_form"/>
    </record>
```

5. Lalu Buat Tree,Form,Search,Action Views pada 'hr_loan_loan_views.xml'.

```xml
#Struktur Direktori
arkana_loan_management
….> models
….> security
….v views
……… hr_loan_loan_views.xml

#hr_loan_loan_views.xml
 <!-- Tree View -->
    <record id="hr_loan_loan_view_tree" model="ir.ui.view">
        <field name="name">hr.loan.loan.view.tree</field>
        <field name="model">hr.loan</field>
        <field name="arch" type="xml">
            <tree string="Loan Management" default_order="name asc" decoration-success="state in ['approved', 'done']" 
                decoration-info="state == 'draft'" decoration-danger="state == 'rejected'">
                
                <field name="name" force_save="1" readonly="1"/>
                <field name="start_date"/>
                <field name="end_date"/>
                <field name="employee_id" readonly="1"/>
                <field name="department_id" readonly="1" optional="hide"/>
                <field name="loan_approver_id" readonly="1"/>
                <field name="loan_type" widget="badge" decoration-success="loan_type in ['petty_cash']" 
                                                        decoration-warning="loan_type in ['loan']"/>
                <field name="loan_amount" optional="show"/>
                <field name="manager_id" optional="hide"/>
                <field name="state" widget="badge" decoration-success="state in ['approved', 'done']" 
                                                    decoration-info="state == 'draft'" decoration-warning="state == 'confirm'" 
                                                    decoration-danger="state == 'rejected'"/>
                <field name="company_id" optional="hide"/>
                <field name="currency_id" invisible="1"/>

            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="hr_loan_loan_view_form" model="ir.ui.view">
        <field name="name">hr.loan.loan.view.form</field>
        <field name="model">hr.loan</field>
        <field name="arch" type="xml">
            <form string="Loan Detail">

                <header>
                    <field name="is_approver" invisible="1" force_save="1" readonly="1"/>
                    <button string="Confirm" name="action_confirm"  type="object" class="oe_highlight" states="draft"/>
                    <button string="Set to Draft" name="action_set_to_draft" type="object" class="oe_hinghlight" states="confirm,rejected"/>
                    <button string="Approve" name="action_approve" type="object" class="oe_highlight"
                                            attrs="{'invisible':['|', ('state', '!=', 'confirm'), ('is_approver', '=', False)]}"/>
                    <button string="Rejected" name="action_rejected" type="object"
                                            class="oe_highlight btn btn-danger text-upercase font-weight-bold"
                                            attrs="{'invisible':['|', ('state','!=', 'confirm'), ('is_approver', '=', False)]}"/>
                    <button string="Loan Report" name="action_loan_report" type="object" class="oe_highlight" states='approved,done'/>
                    <button string="Export Loan Report" name="action_open_loan_report" type="object" class="btn btn-secondary text-uppercase font-weight-bold" states='approved,done'/>
                    <!-- <button string="Edit departmen" name="action_add_employee" type="object" class="btn btn-secondary text-uppercase font-weight-bold"/> -->
                    <field name="state" widget="statusbar" statusbar_visible="draft,confirm,approved,done,rejected"/>

                </header>

                <sheet>
                    <div class="oe_button_box" name="button_box" attrs="{'invisible':[('state', '!=', 'approved')]}">
                        <button name="action_load_loan_details" type="object" class="oe_stat_button" icon="fa-info">
                            <field name="loan_line_count" string="Loan Line" widget="statinfo"/>
                        </button>
                    </div>
                    
                    <div class="oe_title">
                        <label for="name"/>
                        <h1>
                            <field name="name" force_save="1" readonly="1"/>
                        </h1>
                    </div>

                    <group string="General Information" name="general_information">
                        <group style="width:60%;" >
                            <field name="loan_type" force_save="1" readonly="1"/>
                            <label for="start_date" string="Period"/>
                            <div>
                                <field name="start_date" required="1" class="oe_inline" attrs="{'readonly': [('state', '!=', 'draft')]}"/> - <field name="end_date" required="1" class="oe_inline" attrs="{'readonly': [('state', '!=', 'draft')]}"/>
                            </div>
                            <field name="employee_id" required="1" options="{'no_create' : True, 'no_open' : True}" attrs="{'readonly': [('state', '!=', 'draft')]}"/>
                            <field name="department_id" force_save="1" readonly="1" options="{'no_create' : True, 'no_open' : True}"/>
                            <field name="manager_id" force_save="1" readonly="1" options="{'no_create' : True, 'no_open' : True}"/>
                            <field name="loan_approver_id" required="1" force_save="1" readonly="1" options="{'no_create' : True, 'no_open' : True}" attrs="{'readonly': [('state', '=', 'draft')]}"/>
                        </group>

                        <group style="width:40%;">
                            <field name="loan_amount" attrs="{'readonly': ['|',('employee_id', '=', False), ('loan_approver_id', '=', False)], 
                                                    'required': ['&amp;',('employee_id', '=', True),('loan_approver_id', '=', True)]}"/>
                            <field name="company_id" force_save="1" readonly="1" invisible="1"
                                                    options="{'no_open': True, 'no_create': True}"/>
                            <field name="currency_id" force_save="1" readonly="1" invisible="1"
                                                    options="{'no_open': True, 'no_create': True}"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Loan Detail">
                            <field name="line_ids" force_save="1" readonly="1" context="{'tree_view_ref':'arkana_loan_management.hr_loan_line_view_tree'}"/>
                        </page>
                    </notebook>
                </sheet>

                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="hr_loan_loan_view_search" model="ir.ui.view">
        <field name="name">hr.loan.loan.view.search</field>
        <field name="model">hr.loan</field>
        <field name="arch" type="xml">
            <search string="Loan Search">
                <field name="name"/>
                <field name="employee_id"/>
                <field name="department_id"/>
                <separator/>

                <filter string="Draft" name="draft_state" domain="[('state', '=', 'draft')]"/>
                <filter string="Approved" name="approved_state" domain="[('state', '=', 'approved')]"/>
                <filter string="Rejected" name="rejected_state" domain="[('state', '=', 'rejected')]"/>
                <filter string="Confirm" name="confirm_state" domain="[('state', '=', 'confirm')]"/>
                <separator/>

                <filter name="month" string="This Month" domain="['&amp;', ('start_date', '&gt;=', (context_today() + relativedelta(day=1)).strftime('%Y-%m-%d')), ('start_date', '&lt;=', (context_today() + relativedelta(months=1, day=1, days=-1)).strftime('%Y-%m-%d'))]"/>
                <filter name="last_month" string="Last Month" domain="['&amp;', ('start_date', '&gt;=', (context_today() + relativedelta(months=-1, day=1)).strftime('%Y-%m-%d')), ('start_date', '&lt;=', (context_today() + relativedelta(day=1, days=-1)).strftime('%Y-%m-%d'))]"/>
                <separator/>

                <group expand="0" string="Group By">
                    <filter string="Employee" name="group_by_employee_id" domain="[]" context="{'group_by': 'employee_id'}"/>
                    <filter string="Department" name="group_by_department_id" domain="[]" context="{'group_by': 'department_id'}"/>
                    <filter string="Date" name="group_by_start_date" domain="[]" context="{'group_by': 'start_date:month'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Action View -->
    <record id="hr_loan_loan_action" model="ir.actions.act_window">
        <field name="name">Loan Management</field>
        <field name="res_model">hr.loan</field>
        <field name="view_mode">tree,form</field>
        <field name="search_view_id" ref="arkana_loan_management.hr_loan_loan_view_search"/>
        <field name="view_id" ref="arkana_loan_management.hr_loan_loan_view_tree"/>
        <field name="domain">[('loan_type', '=', 'loan')]</field>
        <field name="context">{'default_loan_type' : 'loan'}</field>
        <field name="help" type="html">
            <p/>
        </field>
    </record>

    <!-- Action Search View Tree-->
    <record id="hr_loan_loan_action_tree" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">tree</field>
        <field name="act_window_id" ref="hr_loan_loan_action"/>
        <field name="view_id" ref="hr_loan_loan_view_tree"/>
    </record>

    <!-- Action Search View Form -->
    <record id="hr_loan_loan_action_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">form</field>
        <field name="act_window_id" ref="hr_loan_loan_action"/>
        <field name="view_id" ref="hr_loan_loan_view_form"/>
    </record>
```

6. Buat Tree,Form,Search,Action Views pada 'hr_loan_kasbon_views.xml'.
