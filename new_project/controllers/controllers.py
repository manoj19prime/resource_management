# -*- coding: utf-8 -*-
from odoo import http,api

from odoo.http import request

# class New-project(http.Controller):
#     @http.route('/new-project/new-project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new-project/new-project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('new-project.listing', {
#             'root': '/new-project/new-project',
#             'objects': http.request.env['new-project.new-project'].search([]),
#         })

#     @http.route('/new-project/new-project/objects/<model("new-project.new-project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new-project.object', {
#             'object': obj
#         })


class PartnerWithUs(http.Controller):
    @http.route(['/page/partner/register'], type='http', auth="public", website=True)
    def content_spl_form(self):
        values = {}
        return http.request.render('new-project.content_spl_signup', values)

    # Content Specialist Form
    @http.route(['/content_spl/created'], type='http', auth="public", website=True)
    def content_spl_form_signed_up(self, **kw):
        print(kw)
        # customer_val ={'name':kw['name'],'email':kw['email']}

        requested_as = kw.get('requested_as', '')

        if requested_as == 'reseller':
            partner_as = 'reseller'
            # company_type = 'company'
        else:
            partner_as = 'invigilator'
            # company_type = 'person'
        partner_vals = {'name': kw['name'],
                        'work_email': kw['email'],
                        # 'company_type': company_type,
                        # 'req_profession': kw['req_profession'],
                        # 'is_advocate': 'yes',
                        'partner_as': partner_as}
                        # 'phone': kw.get('phone_number', ''),
        print(partner_vals)

        partner = request.env['hr.employee'].sudo().create(partner_vals)
        if partner.partner_as == 'reseller':
            user_vals = {
                'name': partner.name,
                'login': partner.work_email,
                'partner_id': partner.id,  # Link the user to the partner
                # Add any other necessary fields
            }
            user = request.env['res.users'].sudo().create(user_vals)
            print("User created:", user.name)

        values = {}
        return http.request.render('new-project.content_spl_created', values)

    # @http.route(['/reg/form/<int:partner_id>'], type='http', auth="public", website=True)
    @http.route(['/reg/form'], type='http', auth="public", website=True)
    def advocate_registration_form(self, **kw):
        partner_id = kw.get('name', False)
        id_val = kw.get('id_ram', False)
        print('partnerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',partner_id)
        # current_url = request.httprequest.url
        # partner_split = current_url.split("/")
        # # partner_id = partner_split[-1]
        # partner = partner_split[-1]
        # partner_id = ''
        # for pat in partner:
        #     if pat in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        #         partner_id = partner_id + pat
        partner_obj = request.env['hr.employee'].sudo().search([('id', '=', int(id_val))])
        # # print(partner_obj, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        values = {}
        values['name']=partner_id
        values['id_ram']=id_val
        # print('valuesssssssssssssssssssssssssss',values)
        if partner_obj.partner_as == 'invigilator':
            return http.request.render('new-project.invigilator_register_form', values)
        if partner_obj.partner_as == 'reseller':
            values={'name':partner_id,'id_ram':id_val}
            partner_obj.action_create_user()

            return http.request.render('new-project.reseller_register_form', values)
        # return http.request.render('website_registration.advocate_reg_form', values)

    @http.route('/reg/form/submit', type='http', auth="public", website=True)
    def invigilator_registration_form_submit(self,**kw):
        print(kw,">>>>>>>>>>>>")
        partner_id = kw.get('name')  # Assuming you pass the partner_id in the form data
        mobile_phone = kw.get('mobile_phone')
        spec =kw.get('spec')
        certificate_level = kw.get('certificate_level')
        qua_type_name = kw.get('qua_type')
        type = kw.get('type')
        vat = kw.get('vat')
        # qua_type_id = int(kw.get('qua_type'))

        id = int(kw.get('id_ram'))
        print(id,'iiiiiiiiiiii')
        # partner_id = post.get('partner_id')
        mobile=mobile_phone
        spec =spec
        vat = vat
        if qua_type_name:
            qua_type = request.env['qualification.type'].sudo().search([('qua_type', '=', qua_type_name)], limit=1)
            if not qua_type:
                qua_type = request.env['qualification.type'].sudo().create({'qua_type': qua_type_name})

            qua_type_id = qua_type.id
        else:
            qua_type_id = False
        partner_obj = request.env['hr.employee'].sudo().browse(id)
        if partner_obj:
            res=partner_obj.write({
                'mobile_phone': mobile_phone,
                'spec': spec,
                'certificate_level': certificate_level,
                'qua_type': qua_type_id,
                'type': type,
                'vat': vat
            })
            print(res,'3333333333333333333333333333333')
            # request.env['res.users'].sudo().create({'login':res.work_email,'name':res.name})

        print('mobile phone..............',mobile)
        # request.env.cr.execute("update hr_employee set mobile_phone={mobile} where id={id};".format(mobile=mobile_phone,id=id))
        # request.env.cr.commit()
        # valaue=request.env['hr.employee'].browse(id).update({'mobile_phone':mobile_phone})
        # spec_val = request.env['hr.employee'].browse(id).update({'spec':spec})
        # print(valaue,'1111111111111111111111111111111111111111111111111')


        return 'aaaa'
         # Assuming you pass the partner_id in the form data
        # phone_number = post.get('mobile_phone')  # Get the submitted phone number
        #
        # partner_obj = request.env['hr.employee'].sudo().search([('id', '=', partner_id)])

        # # Update the phone number for the partner with the given ID
        # partner_obj = request.env['hr.employee'].sudo().search([('id', '=', partner_id)])
        # if partner_obj:
        #     partner_obj.write({'phone': mobile_phone})
        # if partner_obj:
        #     partner_obj.write({'phone': phone_number})
        #     # You can add more fields if needed
        #
        # # Redirect the user to a success page or do something else
        return http.request.render('new-project.reseller_register_form')







class MassMailing(http.Controller):
    @http.route(route=['/web/accept/response/<response>'], type="http", auth='public', website=True)
    def approve_accept(self,**kw):
        print(kw,'wwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        res = request.env['mailing.trace'].search([])
        res.mail_status = 'approved'
        print('wwwwwwwwwwwwww')

        return request.render('new-project.sucessfull_email_sent')

    # @http.route('/web/accept/response/<response>', type='http', auth="public", website=True)
    # def handle_accept_response(self, response, **kw):
    #     trace_id = int(kw.get('trace_id', 0))
    #
    #     if trace_id:
    #         trace = request.env['mailing.trace'].sudo().browse(trace_id)
    #         if response == 'approve':
    #             trace.write({'mail_status': 'approved'})
    #         elif response == 'refuse':
    #             trace.write({'mail_status': 'refused'})
    #
    #     # You can redirect the user to a thank you page or any other appropriate response.
    #     return http.request.render('new-project.content_spl_created', {})

    # @http.route(route='/web/accept/response', type='http', auth="public", website=True)
    # def approve(self, **kw):
    #    print('Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')



