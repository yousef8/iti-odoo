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
        string="Department Capacity", related="department_id.capacity", store=False
    )
    doctor_ids = fields.Many2many("hms.doctor", string="Doctors")
    state = fields.Selection(
        [
            ("undetermined", "Undetermined"),
            ("good", "Good"),
            ("fair", "Fair"),
            ("serious", "Serious"),
        ],
        string="State",
        default="undetermined",
    )
    log_history_ids = fields.One2many(
        "hms.patient.log.history", "patient_id", string="Log History"
    )

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

    @api.model
    def create(self, vals):
        res = super(Patient, self).create(vals)
        if "state" in vals:
            self.env["hms.patient.log.history"].create(
                {
                    "patient_id": res.id,
                    "description": f"State changed to {vals['state']}",
                }
            )
        return res

    def write(self, vals):
        res = super(Patient, self).write(vals)
        if "state" in vals:
            for record in self:
                self.env["hms.patient.log.history"].create(
                    {
                        "patient_id": record.id,
                        "description": f"State changed to {vals['state']}",
                    }
                )
        return res
