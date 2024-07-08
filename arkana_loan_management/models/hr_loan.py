from odoo import _, api, fields, models
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class HrLoan(models.Model):
    _name = 'hr.loan'
    _description = 'Loan'
    _inherit = ['mail.thread','mail.activity.mixin']

    def _get_default_employee_id(self):
        employee_ids = self.env.user.employee_ids.filtered(lambda r : r.company_id.id == self.env.company.id)
        return employee_ids[0] if len(employee_ids) > 0 else False

    def action_open_loan_report(self):
        context = {'default_employee_ids' :[(6, 0, self.employee_id.ids)]}
        return{
            'name': 'Export Loan Report',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.loan.report.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('arkana_loan_management.hr_loan_report_wizard_view_form').id,
            'target': 'new',
            'context': context
        }
    

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
    name =fields.Char("Name", default ='New', copy=False)
    state =fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
    ], string = 'State', default = 'draft', copy = False, tracking = True, index = True)
    start_date = fields.Date('Start Date', tracking=True, default=lambda self: fields.Date.to_string(datetime.today().replace(day=1)), index=True)
    end_date = fields.Date('End Date', tracking=True, compute='_compute_end_date', readonly=False, store=True, index=True)
    employee_id = fields.Many2one('hr.employee', string = 'Employee', index = True, copy = False,
                                                    tracking = True, ondelete = 'restrict', default = '_get_default_employee_id')
    department_id = fields.Many2one('hr.department', string = 'Department', index = True,
                                                    store = True, compute = '_compute_employee_id', tracking = True, ondelete='set null')
    manager_id = fields.Many2one('hr.employee', compute='_compute_employee_id', string='Manager', store = True,
                                                    index=True, tracking=True, ondelete='set null')
    loan_approver_id = fields.Many2one('res.users', compute='_compute_employee_id', string='Loan Approver', store = True, readonly=False,
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
                                        compute='_compute_residual_amount',
                                        digits=(3,2))
    loan_amount = fields.Monetary("Loan Amount", currency_field="currency_id")

    #Compute Residual Amount
    @api.depends('limit_amount', 'total_amount')
    def _compute_residual_amount(self):
        for rec in self:
            rec.residual_amount = rec.limit_amount - rec.total_amount
            try:
                rec.residual_amount_percentage = (
                    rec.limit_amount - rec.total_amount
                ) / rec.limit_amount
            except:
                rec.residual_amount_percentage = 0

    
    #Check Authorized User
    def _compute_is_authorized_user(self):
        for rec in self:
            rec.is_authorized_user = bool(rec.employee_id.user_id.id == self.env.user.id
            ) or bool(self.env.user.has_group('arkana_loan_management.group_loan_management_finance'))
    
    #Check Approver User
    def _compute_is_approver(self):
        for rec in self:
            rec.is_approver = bool(rec.loan_approver_id.id == self.env.user.id)\
                or bool(self.env.user.has_group('arkana_loan_management.group_loan_management_administrator'))

    #Action to Confirm
    def action_confirm(self):
        values = {'state' : 'confirm'}
        for rec in self:
            if rec.name == 'New':
                values['name'] = rec._generate_name_by_seq(rec.loan_type)
            rec.write(values)
            rec._send_message_to_partner()
        return True

    #Get Default Message
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
            request = "Your Request" if not line else "Your Loan Line Request with Name : <b> {} </b>".format(line_name)
            action = 'Approved' if type in ['approved', 'confirm'] else 'Rejected' 
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
        partner_ids = (self.loan_approver_id.partner_id + \
            self.employee_id.user_id.partner_id + self.env.user.partner_id
            )
        display_msg = self._get_default_message(type, line, line_name)
        self.message_post(body=display_msg, 
                        partner_ids=partner_ids.ids,
                        massage_type='comment',
                        subtype_xmlid='mail.mt_comment')
        return True
        
    #Compute Loan Line Count
    @api.depends('line_ids', 'line_ids.state')
    def _compute_loan_line_count(self):
        for rec in self:
            rec.loan_line_count = len(rec.line_ids)

    #Compute End Date
    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = start_date + timedelta(days=1)
            record.end_date = fields.Date.to_string(end_date)

    #Compute Total Amount
    @api.depends('line_ids.amount', 'line_ids', 'line_ids.state')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.filtered(lambda x : x.state == 'confirm').mapped('amount'))

    #Compute Employee Data
    @api.depends('employee_id')
    def _compute_employee_id(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id.id if rec.employee_id.department_id \
                and rec.employee_id else False
                
            rec.loan_approver_id = rec.employee_id.loan_approver_id.id if rec.employee_id.loan_approver_id \
                and rec.employee_id else rec.employee_id.parent_id.id and rec.employee_id \
                    if rec.employee_id.parent_id else False
                    
            rec.manager_id = rec.employee_id.parent_id.id if rec.employee_id.parent_id and rec.employee_id else False
            rec.limit_amount = rec.employee_id.limit_amount if rec.employee_id.limit_amount and rec.employee_id else False
    
    #action to draft
    def action_set_to_draft(self):
        self.write({'state' : 'draft'})
        return True

    #Generate Sequence
    def _generate_name_by_seq(self, loan_type):
        try:
            if loan_type == "loan":
                name = self.env['ir.sequence'].next_by_code('hr.loan.loan.sequence')
            if loan_type == "petty_cash":
                name = self.env['ir.sequence'].next_by_code('hr.loan.kasbon.sequence')
            return name
        except Exception as err:
            raise ValidationError(f'''Sequence not Found! {err}''')

    #action to approve
    def action_approve(self):
        self.write({'state' : 'approved'})
        self._send_message_to_partner(type = 'approved')
        if self.loan_type == "loan":
            self._generate_data()
        return True

    def _generate_data(self):
        start_date = self.start_date
        end_date = self.end_date
        next_pay = start_date + relativedelta(day=2)
        pay_dates = []

        message_var = {
            "employee_name": self.employee_id.user_id.partner_id.name,
            "loan_number": self.name,
            "company_name": self.company_id.name,
        }
        while next_pay <= end_date:
            pay_dates.append(next_pay)
            next_pay = next_pay + relativedelta(months=+1, day=2)

        count = 1
        for pay_date in pay_dates:
            vals = {
                "name": "{} - {}".format(self.name, pay_date.strftime("%d %m %Y")),
                "loan_id": self.id,
                "employee_id": self.employee_id.id,
                "loan_type": self.loan_type,
                "company_id": self.company_id,
                "date": pay_date,
                "amount": self.loan_amount / len(pay_dates),
                "remarks": "Pembayaran bulan ke-{}".format(count),
                "create_uid": False,
            }

            self._send_messages_loan_schedule(vals, message_var)
            self.line_ids.create(vals)
            count += 1

    def _send_messages_loan_schedule(self, vals, message_var):
        partner_ids = (
            self.loan_approver_id.partner_id
            + self.employee_id.user_id.partner_id
            + self.env.user.partner_id
        )
        display_msg = self._get_default_message_loan_schedule(vals, message_var)
        self.message_post(
            body=display_msg,
            partner_ids=partner_ids.ids,
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
        )
        return True

    def _get_default_message_loan_schedule(self, vals, message_var):
        return """ Dear <b> {} </b>,
            <br/>
            Your loan schedule has been generated.
            <br/>
            Loan ID : <b> {} </b>
            <br/>
            Date : <b> {} </b>
            <br/>
            Amount : <b> {} </b>
            <br/>
            Company : <b> {} </b>
            <br/>
            """.format(
            message_var["employee_name"],
            message_var["loan_number"],
            vals["date"],
            vals["amount"],
            message_var["company_name"],
        )

    #action to rejected
    def action_rejected(self):
        self.write({'state' : 'rejected'})
        self._send_message_to_partner(type = 'rejected')
        return True

    def _check_authorized_user(self):
        is_authorized = bool(self.employee_id.user_id.id == self.env.user.id) \
                or bool(self.env.user.has_group('arkana_loan_management.group_loan_management_finance')) if self.loan_type == 'petty_cash' else True
        return is_authorized


    #Action to Load Loan Details
    def action_load_loan_details(self):
        # Memeriksa apakah pengguna memiliki otoritas untuk mengakses rincian pinjaman
        is_authorized = self._check_authorized_user()
        action = self.env.ref('arkana_loan_management.hr_loan_line_action').sudo().read()[0]
        action['domain'] = [('loan_id', '=', self.id)]
        action['context'] = {'default_loan_id' : self.id} if is_authorized else \
                {'default_loan_id' : self.id, 'create' : 0, 'edit' : 0, 'delete' : 0}
        return action

    # def action_add_employee(self):
    #     loans = self.env['hr.loan'].search([])
    #     for loan in loans:
    #         if not loan.department_id:
    #             print(loan.id,'aaaaaaaaaaaaaaaaaa')
    #             loan.write({
    #                 'department_id' : loan.employee_id.department_id.id
    #             })
    #             # loan.department_id = loan.employee_id.department_id.id
    #         print(loan.employee_id.department_id.id,'sssssssssssssssssssssss')

    def unlink(self):
        for rec in self:
            if rec.state != 'draft' or len(rec.line_ids.filtered(lambda x : x.state == 'confirm')) > 0:
                raise UserError("You can't Delete the Data because not in Draft State or has Confimed Lines")
        return super(HrLoan, self).unlink()

    def action_loan_report(self):
        return self.env.ref('arkana_loan_management.action_report_hr_loan').report_action(self)

    def _prepare_header_datas(self):
        return [{
            'label' : 'Loan Amount',
            'value' : self.loan_amount
        },{
            'label' : 'Start Date',
            'value' : self.start_date.strftime('%d - %m - %Y')
        },{
            'label' : 'End Date',
            'value' : self.end_date.strftime('%d - %m - %Y')
        }]
    

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
        # if res.loan_type != "loan":
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
        if not self.loan_id._check_authorized_user() and self.loan_type != "loan":
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
        if self.loan_type == 'loan':
            self._check_loan_month()
        datas = self.filtered(lambda x : x.state not in ['confirm', 'rejected'])
        line_name = (
            ", ".join([data.name for data in datas]) if len(datas) > 1 else self.name
        )
        datas.write({'state' : state})
        datas.loan_id._send_message_to_partner(state, True, line_name)
        return True

    def _check_loan_month(self):
        if self.date.month != date.today().month:
            raise ValidationError("You can't confirm the Loan at this Month")

    @api.model
    def _confirm_loan_details(self):
        today = fields.Date.context_today(self)
        result = self.search([('loan_type','!=', 'petty_cash'), 
                            ('state', '=', 'draft'),
                            ('date', '<=', today)])
        for res in result:
            res.write({'state' : 'confirm'})
        return True
    