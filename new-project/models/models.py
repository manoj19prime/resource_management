# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class new_project(models.Model):
#
#     _name = 'new-project.new-project'
#     _description = 'new-project.new-project'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class InheritEmployee(models.Model):
    _inherit = 'hr.employee'

    background_emp = fields.One2many('res.background', 'employee_background')
    vat = fields.Char(tracking=5)
    certificate_level = fields.Selection([('post_graduation', 'Post Graduation'),
                                          ('graduation', 'Graduation'), ('diploma', 'Diploma'),
                                          ('twelfth_or_equivalent', '12th or Equivalent'),
                                          ('tenth_or_equivalent', '10th or Equivalent'), ], string="Degree Name")
    qua_type = fields.Many2one('qualification.type',string='Qualification')
    type = fields.Selection([('academic','Academic'),('technical','Technical'),('professional','Professional'),('certificate','Certificate')])
    spec = fields.Char(string='Specialization')
    hig_degree = fields.Boolean(string='Highest Degree')
    job_position_ids = fields.Many2many('job.position', string='Job Position')
    aadhar = fields.Char("Aadhar Number")
    pan_no = fields.Char('Pan Number')
    district_name = fields.Many2one('district.name', string='District Name')
    native_place = fields.Char('Native Place')
    availability = fields.Selection([('full_time', 'Full Time'),
                                     ('part_time', 'Part Time'),
                                     ('weekdays', 'Weekdays'),
                                     ('weekends', 'Weekends'),
                                     ('holidays', 'Holidays')])
    employee_status = fields.Selection([('employee', 'Employeed'),
                                        ('not_employee', 'Not Employeed'),
                                        ])
    partner_as = fields.Selection([('reseller','Reseller'),('invigilator','Invigilator')],string ='Partner as')


    def open_create_mailing_list_wizard(self):
        # Open the wizard
        return {
            'name': 'Create Mailing List',
            'type': 'ir.actions.act_window',
            'res_model': 'mailing.list.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('new-project.view_create_mailing_list_wizard_form').id,
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        res = super(InheritEmployee, self).create(vals)
        if res.partner_as == 'invigilator':
            template_id = self.env.ref('new-project.reg_email_template').id
            print(template_id,"emaillllllllll")
            mail_template = self.env['mail.template'].browse(template_id)

            # partner_id = self.env['res.partner'].sudo().search([('id', '=', vals['partner_id'])])
            if mail_template:
                # records = partner_id
                records = res
                for rec in records:
                    email = vals.get('work_email')
                    print(email,">>>>>>>>>>>>>>>")
                    if email:
                        mail_template.write({'email_to': vals['work_email']})
                        print(mail_template)
                        mail_template.write({'email_from': 'admin@example.com'})
                        mail_id = mail_template.send_mail(rec.id, force_send=True)
        if res.partner_as == 'reseller':
            template_id = self.env.ref('new-project.reg_email_template').id
            print(template_id, "emaillllllllll")
            mail_template = self.env['mail.template'].browse(template_id)

            # partner_id = self.env['res.partner'].sudo().search([('id', '=', vals['partner_id'])])
            if mail_template:
                # records = partner_id
                records = res
                for rec in records:
                    email = vals.get('work_email')
                    print(email, ">>>>>>>>>>>>>>>")
                    if email:
                        mail_template.write({'email_to': vals['work_email']})
                        print(mail_template)
                        mail_template.write({'email_from': 'admin@example.com'})
                        mail_id = mail_template.send_mail(rec.id, force_send=True)

        # if res.is_advocate == 'no':
        #     pass
        print(res)
        return res





class BackgroundVerification(models.Model):
    _name = 'res.background'

    certificate_level = fields.Selection([('post_graduation','Post Graduation'),
                                          ('graduation','Graduation'),('diploma','Diploma'),('twelfth_or_equivalent','12th or Equivalent'),
                                          ('tenth_or_equivalent','10th or Equivalent'),],string="Degree Name")
    employee_background = fields.Many2one('hr.employee')
    # specialization_emp = fields.Char(string="Specialization")



class CreateMailingListWizard(models.TransientModel):
    _name = 'mailing.list.wizard'

    name = fields.Char(string='Name', required=True)

    selected_contacts_ids = fields.Many2many('hr.employee', string='Select Contacts',
                                             default=lambda self: self.env.context.get('active_ids', []))

    def create_mailing_list(self):

        email = self.env['mailing.list'].search([])
        mail_contact = self.env['mailing.contact'].search([])
        active_employee_ids = self.env.context.get('active_ids', [])
        print(active_employee_ids)

        for rec in self:
            emsi = email.create({
                'name': rec.name
            })
            for employee in self.selected_contacts_ids:
                existing_contact = mail_contact.search([('email', '=', employee.work_email)])
                if existing_contact:
                    existing_contact.write({
                        'list_ids': [(4, emsi.id)],
                    })
                else:
                    mail_contact.create({
                        'name': employee.name,
                        'list_ids': [(6, 0, [emsi.id])],
                        'email': employee.work_email
                    })

        return {'type': 'ir.actions.act_window_close'}


class MassMailing(models.Model):
    _inherit = 'mailing.trace'

    mail_status = fields.Selection([('approved','APPROVED'),('refused','REFUSED')])
    name = fields.Char('Employee Name')

    @api.depends('email')
    def _compute_display_name(self):
        for trace in self:
            trace.display_name = trace.name or 'No Email'

    @api.model_create_single
    def create(self, values):
        record = super(MassMailing, self).create(values)

        # You can also set the 'name' field based on the email if needed
        mail = self.env['mailing.contact'].search([('email', '=', record.email)])
        for mails in mail:
            record.name = mails.name

        return record

    @api.depends('email')
    def email_related_field(self):
        data = self.env['hr.employee'].search([])
        for rec in self:
            if rec.email == data.work_email:
                print('its ...')
                data.create({
                    'name': rec.name
                })

    def open_assignee_wizard(self):
        return {
            'name': 'Create Mailing List',
            'type': 'ir.actions.act_window',
            'res_model': 'mailing.trace.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('new-project.view_create_mailing_trace_wizard_form').id,
            'target': 'new',
        }


class MailingTraceWizard(models.TransientModel):
    _name = 'mailing.trace.wizard'

    project_name = fields.Many2one('project.project')
    task = fields.Many2one('project.task', domain="[('project_id', '=', project_name)]")
    selected_contacts_ids = fields.Many2many('mailing.trace', string='Select Contacts',
                                             default=lambda self: self.env.context.get('active_ids', []))

    def create_assignee_list(self):
        tasks = self.env['project.task'].search(
            [('name', '=', self.task.name), ('project_id', '=', self.project_name.display_name)])

        for task in tasks:
            for rec in self:
                for recs in rec.selected_contacts_ids:
                    # Assuming 'employ_assign_ids' is a One2many field in 'project.task'
                    # and 'employee_assign' is a Char field in the comodel 'comodel_name'
                    task.write({'employ_assign_ids': [(0, 0, {'employee_assign': recs.name})]})

        return {'type': 'ir.actions.act_window_close'}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    Employee_assignee_ids = fields.Many2one('hr.employee', string='Assignee')
    # employee_assign = fields.Char(string='Assignee')
    parent_new_id = fields.Many2one('project.task', string='Parent Task', index=True,
                                    domain="['!', ('id', 'child_of', id)]", tracking=True)
    child_new_ids = fields.One2many('project.task', 'parent_id', string="Sub-tasks",
                                    domain="[('recurring_task', '=', False)]")
    employ_assign_ids = fields.One2many('project.task.assign', 'employee_assignee')


class ProjectTaskNotebook(models.Model):
    _name = 'project.task.assign'

    employee_assignee = fields.Many2one('project.task')
    employee_assign = fields.Char(string='Assignee')



















