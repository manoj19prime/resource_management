# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Qualification(models.Model):
    _name = 'qualification.type'
    _rec_name = 'qua_type'

    qua_type = fields.Char('Qualification')


class JobPosition(models.Model):
    _name = 'job.position'
    _rec_name = 'job_position'

    job_position= fields.Char(string='Job Position')

class DistrictDetail(models.Model):
    _name = 'district.name'
    _rec_name = 'district_name'
    district_name = fields.Char('District Name')