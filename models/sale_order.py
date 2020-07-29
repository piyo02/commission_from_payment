from odoo import api, fields, models
from lxml import etree
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line', 'commission')
    def _compute_commission_total(self):
        for order in self:
            order.commission_total = 0.0
            if order.commission.commission_type == "fixed":
                order.commission_total = order.amount_total*order.commission.fix_qty
            elif order.commission.commission_type == "section":
                for section in order.commission.sections:
                    if section.amount_from < order.amount_total < section.amount_to:
                        order.commission_total = order.amount_total*section.percent

    commission_total = fields.Float(
        string="Commissions", compute="_compute_commission_total",
        store=True)
    commission = fields.Many2one(
        comodel_name="sale.commission",
        ondelete="restrict",
        required=True,
    )