from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one("hms.patient", string="Related Patient")

    vat = fields.Char(string="Tax ID", required=True)

    @api.constrains("related_patient_id")
    def _check_related_patient_email(self):
        for record in self:
            if record.related_patient_id:
                existing_partner = self.env["res.partner"].search(
                    [
                        ("related_patient_id", "=", record.related_patient_id.id),
                        ("id", "!=", record.id),
                    ]
                )
                if existing_partner:
                    raise ValidationError(
                        "The related patient is already linked to another customer with email: %s"
                        % record.related_patient_id.email
                    )
