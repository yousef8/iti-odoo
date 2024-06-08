from datetime import date

from odoo import api, fields, models


class Patient(models.Model):
    _name = "hms.patient"
    _description = "HMS Patient"
    _rec_name = "first_name"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date(string="Birth Date", required=True)
    history = fields.Html(string="History")
    cr = fields.Float(string="CR")
    blood_type = fields.Selection(
        [
            ("a+", "A+"),
            ("a-", "A-"),
            ("b+", "B+"),
            ("b-", "B-"),
            ("ab+", "AB+"),
            ("ab-", "AB-"),
            ("o+", "O+"),
            ("o-", "O-"),
        ],
        string="Blood Type",
    )
    pcr = fields.Boolean(string="PCR")
    image = fields.Image(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age", compute="_compute_age")

    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = (
                    today.year
                    - record.birth_date.year
                    - (
                        (today.month, today.day)
                        < (record.birth_date.month, record.birth_date.day)
                    )
                )
            else:
                record.age = 0