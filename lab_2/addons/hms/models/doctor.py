from odoo import fields, models


class HmsDoctor(models.Model):
    _name = "hms.doctor"
    _description = "HMS Doctor"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Image(string="Image")

    patient_ids = fields.Many2many("hms.patient", string="Patients")
