from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one("hms.patient", string="Related Patient")
