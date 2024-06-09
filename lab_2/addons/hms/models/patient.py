from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


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
    image = fields.Binary(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age", compute="_compute_age")
    department_id = fields.Many2one(
        "hms.department", string="Department", domain=[("is_opened", "=", True)]
    )
    department_capacity = fields.Integer(
        string="Department Capacity", related="department_id.capacity", store=True
    )
    doctor_ids = fields.Many2many("hms.doctor", string="Doctors")

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

    @api.onchange("age")
    def _onchange_age(self):
        for record in self:
            if record.age and record.age < 30:
                record.pcr = True
                return {
                    "warning": {
                        "title": "PCR Test Checked",
                        "message": "PCR test has been automatically checked because the age is lower than 30.",
                    }
                }

    @api.constrains("pcr", "cr")
    def _check_cr_mandatory(self):
        for record in self:
            if record.pcr and not record.cr:
                raise ValidationError(
                    "Creatinine Level is required if PCR Test is checked."
                )
