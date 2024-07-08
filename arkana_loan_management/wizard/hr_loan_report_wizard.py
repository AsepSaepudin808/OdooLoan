from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64, xlsxwriter
from io import BytesIO


class hr_loan_report_wizard(models.TransientModel):
    _name = 'hr.loan.report.wizard'
    _description = 'Hr Loan Report Wizard'

    company_id = fields.Many2one('res.company', string='Company', index =True, copy =False,
                                                default =lambda self: self.env.company.id)
    employee_ids = fields.Many2many('hr.employee', 
                                    'employee_loan_report', 
                                    'hr_loan_report_id',
                                    'employee_id',
                                    check_company=True,
                                    string='Employee')
    include_details = fields.Boolean('Include Details', default=False)
    loan_type = fields.Selection([
        ('all', 'All'),
        ('petty_cash', 'Casbon'),
        ('loan', 'Loan')
    ], string='Loan Type', default='all')

    excel_file = fields.Binary('Exel File')
    wbf = {}

    # Fungsi untuk menambahkan format workbook
    def add_workbook_format(self, workbook):
        self.wbf["header"] = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "font_size": 12,
                "fg_color": "#c9c9c9",
                "border": 1,
                "text_wrap": True,
            }
        )
        self.wbf["header"].set_border()
        self.wbf["content"] = workbook.add_format()
        self.wbf["content"].set_left()
        self.wbf["content"].set_right()
        return workbook

    # Fungsi untuk mengekspor laporan pinjaman
    def action_export_loan_report(self):
        result = True
        for rec in self:
            if not rec.include_details:
                result = rec._export_summary_loan_report()
            else:
                result = rec._export_loan_report_details()
        return result

    def _prepare_loan_report_header(self):
        return {
            'sheet_name' : 'Loan Report', 
            'column' :[
                'NO',
                'NAME',
                'LOAN_TYPE',
                'EMPLOYEE_NAME',
                'EMPLOYEE_NIK',
                'EMPLOYEE_APPROVER',
                'EMPLOYEE_MANAGER',
                'DEPARTMENT_NAME',
                'START_DATE',
                'END_DATE',
                'AMOUNT',
        ]}
    

    # Fungsi untuk menyiapkan header (judul kolom) dari laporan rincian pinjaman yang akan diekspor ke file Excel
    def _prepare_loan_report_header_details(self):
        return {
            'sheet_name': 'Loan Report',
            'column': [
                'NO',
                'DATE',
                'NAME_ID',
                'START_DATE',
                'END_DATE',
                'NAME_LOAN_DETAILS',
                'LOAN_TYPE',
                'REMARKS',
                'AMOUNT',
                'STATE',
            ],
        }

    # Fungsi untuk menyiapkan data rincian laporan pinjaman
    def _prepare_loan_report_datas_details(self):
        params = "AND hl.loan_type = 'loan'" if self.loan_type == "loan"\
                else "AND hl.loan_type = 'petty_cash'" if self.loan_type == "petty_cash" else ""
        try:
            query = """
                SELECT hl.name AS NAME_ID, CASE WHEN hl.loan_type = 'loan' THEN 'Loan Long Term' ELSE 'Kasbon' END AS LOAN_TYPE,
                he.name AS EMPLOYEE_NAME,
                COALESCE(he.identification_id, '-') AS EMPLOYEE_NIK,
                hd.name AS DEPARTMENT_NAME,

                rp.name AS EMPLOYEE_APPROVER, 
                mg.name AS EMPLOYEE_MANAGER,
                
                TO_CHAR(hl.start_date, 'DD/MM/YYYY') AS START_DATE,
                TO_CHAR(hl.end_date, 'DD/MM/YYYY') AS END_DATE,
                COALESCE(hl.loan_amount, 0) AS AMOUNT,
                TO_CHAR(hll.date, 'DD/MM/YYYY') AS DATE,
                hll.name AS NAME_LOAN_DETAILS,
                hll.remarks AS REMARKS,
                hll.state AS STATE
                FROM hr_loan hl
                INNER JOIN hr_employee he ON he.id = hl.employee_id

                LEFT JOIN res_users la ON la.id = he.loan_approver_id
                INNER JOIN res_partner rp ON rp.id = la.partner_id
                LEFT JOIN hr_employee mg ON mg.id = he.parent_id

                LEFT JOIN hr_department hd ON hd.id = hl.department_id
                RIGHT JOIN hr_loan_line hll ON hll.loan_id = hl.id
                WHERE hl.company_id IN %s AND hl.employee_id IN %s {}
                ORDER BY NAME_ID ASC, DATE ASC
            """.format(params)
            self._cr.execute(query,[tuple(self.company_id.ids),tuple(self.employee_ids.ids),])
            result = self._cr.dictfetchall()
            return result

        except Exception as Err:
            raise ValidationError("Error: {}".format(Err))

    # Fungsi untuk menyiapkan data laporan pinjaman
    def _prepare_loan_report_datas(self):
        try: 
            params = "AND hl.loan_type = 'loan'" if self.loan_type == "loan"\
                else "AND hl.loan_type = 'petty_cash'" if self.loan_type == "petty_cash" else ""
            query = """
                SELECT hl.name AS NAME,
                CASE WHEN hl.loan_type = 'loan' THEN 'Loan Long Term' ELSE 'Kasbon' END AS LOAN_TYPE,
                he.name AS EMPLOYEE_NAME,
                COALESCE(he.identification_id, '_') AS EMPLOYEE_NIK,
                TO_CHAR(hl.start_date, 'DD/MM/YYYY') AS START_DATE,
                TO_CHAR(hl.end_date, 'DD/MM/YYYY') AS END_DATE,
                COALESCE(hl.loan_amount, 0) AS AMOUNT
                FROM hr_loan hl
                INNER JOIN hr_employee he ON he.id = hl.employee_id
                LEFT JOIN hr_department hd ON hd.id = hl.department_id
                WHERE hl.company_id IN %s AND hl.employee_id IN %s {}
            """.format(params)
            self._cr.execute(query, [tuple(self.company_id.ids), tuple(self.employee_ids.ids),])
            result = self._cr.dictfetchall()
            return result
        except Exception as Err:
                raise ValidationError('Error : {}'.format(Err))

    # Fungsi untuk mengekspor rincian laporan pinjaman
    def _export_summary_loan_report(self):
        # Menyiapkan header dan data rincian laporan pinjaman
        loan_report_header = self._prepare_loan_report_header()
        loan_report_datas = self._prepare_loan_report_datas()

        # Inisialisasi objek BytesIO untuk menyimpan file Excel dalam bentuk bytes
        fp = BytesIO()
        # Membuat workbook menggunakan xlsxwriter
        workbook = xlsxwriter.Workbook(fp)
        workbook = self.add_workbook_format(workbook)
        wbf = self.wbf
        row, column = 0,0
        headercolumn = column
        content_line, linenum  = row +1, 1
        
        worksheet = workbook.add_worksheet(loan_report_header['sheet_name'])
        column_length = len(loan_report_header['column'])

        for header in loan_report_header['column']:
            worksheet.write(row, headercolumn, header, wbf['header'])
            worksheet.set_column(headercolumn, headercolumn, 8 if len(header) <=3 else 15 if len(header) <=5 else 25)
            headercolumn +=1

        datas = {
            'linenum' : linenum, 
            'content_line' : content_line,
            'column_length' : column_length, 
            'header_report' : loan_report_header['column'],
            }

        for vals in loan_report_datas:
            self._set_summary_loan_report_values(worksheet, wbf, vals, datas)
            datas['linenum'] += 1
            datas['content_line'] +=1

        # Menutup workbook dan menyimpan file Excel dalam objek BytesIO
        workbook.close()
        self.excel_file = base64.encodebytes(fp.getvalue())
        fp.close()
        # Menentukan nama file
        filename="{}".format(loan_report_header['sheet_name'])

        # Mengembalikan tindakan URL untuk mengunduh file Excel
        return {
            "type": "ir.actions.act_url",
            "url": "web/content/?model={}&field=excel_file&download=true&id={}&filename={}".format(self._name, self.id, filename),
            "target": "new",
        }

    # Fungsi untuk menentukan nilai dalam laporan rincian
    def _set_summary_loan_report_values(self, worksheet, wbf, vals, datas):
        # Inisialisasi daftar indeks untuk setiap kolom dalam worksheet
        list_of_index = [index for index in range(datas["column_length"])]
        # Iterasi melalui setiap kolom
        for num in range(datas["column_length"]):
            # Mendapatkan nama kolom dalam huruf kecil
            column_name = datas['header_report'][num].lower()
            if column_name == 'no':
                worksheet.write(
                    datas['content_line'],
                    list_of_index[num],
                    datas['linenum'],
                    wbf['content']
                )
            elif column_name in vals:
                worksheet.write(
                    datas['content_line'],
                    list_of_index[num],
                    vals[column_name],
                    wbf['content']
                )
            else :
                worksheet.write(
                    datas['content_line'],
                    list_of_index[num],
                    '_',
                    wbf['content']
                )

    # Fungsi untuk mengekspor rincian laporan pinjaman
    def _export_loan_report_details(self):
        loan_report_header = self._prepare_loan_report_header_details()
        loan_report_datas = self._prepare_loan_report_datas_details()

        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        workbook = self.add_workbook_format(workbook)
        wbf = self.wbf

        # Set unik dari data employee
        employee_set = set()
        for data in loan_report_datas:
            employee_set.add((data['employee_name'],data['employee_nik'],data['department_name'],data['employee_approver'], data['employee_manager']))
        
        for employee in employee_set:
            row, column = 0, 0
            headercolumn = column
            content_line, linenum = row + 7, 1
            worksheet = workbook.add_worksheet(employee[0])
            
            value_state = workbook.add_format({"align": "left",
                "font_size": 12,
                "fg_color": "#c9c9c9",
                "border": 1,
                "text_wrap": True})

            # detail information
            worksheet.merge_range("A1:J1", "LOAN MANAGEMENT REPORT", workbook.add_format({"bold": True, "align": "center"}))
            worksheet.write("B3", "Name", value_state)
            worksheet.write("B4", "NIK", value_state)
            worksheet.write("B5", "Department", value_state)
            worksheet.write("E3", "Manager", value_state)    
            worksheet.write("E4", "Approver", value_state)
            worksheet.write("C3", employee[0], value_state)
            worksheet.write("C4", employee[1], value_state)
            worksheet.write("C5", employee[2], value_state)
            worksheet.write("F3", employee[3], value_state)
            worksheet.write("F4", employee[4], value_state)

            # header
            column_length = len(loan_report_header["column"])

            for header in loan_report_header["column"]:
                # Mengatur lebar kolom berdasarkan panjang teks dalam judul kolom
                worksheet.write(6, headercolumn, ' '.join(header.split('_')), wbf["header"])
                worksheet.set_column(
                    headercolumn,
                    headercolumn,
                    8 if len(header) <= 3 else 15 if len(header) <= 5 else 25,
                )
                headercolumn += 1

            # content
            datas = {
                
                "linenum": linenum,
                "content_line": content_line,
                "column_length": column_length,
                "header_report": loan_report_header["column"],
                
            }

            count_draft = 0
            count_confirm = 0
            total_amount = 0
            for vals in loan_report_datas:
                if vals['employee_name'] == employee[0]:
                    self._set_summary_loan_report_values(worksheet, wbf, vals, datas)
                    # print(vals['state'])
                    datas["linenum"] += 1
                    datas["content_line"] += 1
                    total_amount += vals["amount"]
                    if vals['state'] == 'draft':
                        count_draft += 1
                    elif vals['state'] == 'confirm': 
                        count_confirm += 1 

            worksheet.write(datas["content_line"], 7, "TOTAL", wbf["header"])
            worksheet.write(datas["content_line"], 8, total_amount, workbook.add_format({"text_wrap": True}))
            worksheet.write(datas["content_line"]+2, 7,"STATE", wbf["header"])
            worksheet.write(datas["content_line"]+3, 7, "Draft : {}".format(count_draft), value_state)
            worksheet.write(datas["content_line"]+4, 7, "Confirm : {}".format(count_confirm), value_state)
            
        workbook.close()
        self.excel_file = base64.encodebytes(fp.getvalue())
        fp.close()

        filename = "{}".format(loan_report_header["sheet_name"])

        return {
            "type": "ir.actions.act_url",
            "url": "web/content/?model={}&field=excel_file&download=true&id={}&filename={}".format(
                self._name, self.id, filename
            ),
            "target": "new",
        }



