from odoo import fields, models


class PatientLogHistory(models.Model):
    _name = "hms.patient.log.history"
    _description = "Patient Log History"

    date = fields.Datetime(string="Date", default=fields.Datetime.now, required=True)
    description = fields.Text(string="Description", required=True)
    patient_id = fields.Many2one("hms.patient", string="Patient", required=True)
