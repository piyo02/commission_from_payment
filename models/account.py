from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "account.invoice"

    @api.depends('invoice_line_ids', 'commission')
    def _compute_commission_total(self):
        pass
        for invoice in self:
            invoice.commission_total = 0.0
            total = 0
            for line in invoice.invoice_line_ids:
                if not line.product_id.commission_free:
                    total += line.price_subtotal

            if invoice.commission.commission_type == "fixed":
                invoice.commission_total = (total*invoice.commission.fix_qty)/100
            elif invoice.commission.commission_type == "section":
                for section in invoice.commission.sections:
                    if section.amount_from < total < section.amount_to:
                        invoice.commission_total = (total*section.percent)/100
    
    commission_total = fields.Float(
        string="Commissions", compute="_compute_commission_total",
        store=True)
    commission = fields.Many2one(
        comodel_name="sale.commission",
        ondelete="restrict",
        required=True,
    )
    settled = fields.Boolean(
        string="Settled", readonly=True, default=False)