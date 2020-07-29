from odoo import api, exceptions, fields, models, _
import logging
from datetime import date, timedelta

_logger = logging.getLogger(__name__)
class Settlement(models.Model):
    _name = "sale.commission.settlement"

    name = fields.Char('Name')
    total = fields.Float(compute="_compute_total", readonly=True, store=True)
    date_from = fields.Date(string="From")
    date_to = fields.Date(string="To")
    agent = fields.Many2one(
        comodel_name="res.partner", domain="[('agent', '=', True)]")
    lines = fields.One2many(
        comodel_name="sale.commission.settlement.line",
        inverse_name="settlement", string="Settlement lines", readonly=True)
    state = fields.Selection(
        selection=[("draft", "Draft"),
                   ("validated", "Validated"),
                   ("cancel", "Canceled")], string="State",
        readonly=True, default="draft")
    invoice = fields.Many2one(
        comodel_name="account.invoice", string="Generated invoice",
        readonly=True)

    @api.depends('lines', 'lines.settled_amount')
    def _compute_total(self):
        for record in self:
            record.total = sum(x.settled_amount for x in record.lines)
    
    def action_validated(self):
        if any(x.state != 'draft' for x in self):
            raise exceptions.Warning(
                _('Cannot va;idated an settlement when it canceled.'))
        self.write({'state': 'validated'})
        for line in self.lines:
            line.invoice.write({'settled': True})

    def action_cancel(self):
        if any(x.state != 'draft' for x in self):
            raise exceptions.Warning(
                _('Cannot cancel an settlement when it validated.'))
        self.write({'state': 'cancel'})

class SettlementLines(models.Model):
    _name = "sale.commission.settlement.line"

    settlement = fields.Many2one(
        "sale.commission.settlement",
        readonly=True,
        ondelete="cascade",
        required=True,
    )
    invoice = fields.Many2one(
        comodel_name='account.invoice', store=True, string="Invoice")
    date = fields.Date(store=True)
    commission = fields.Many2one(
        comodel_name="sale.commission")
    settled_amount = fields.Float(
        readonly=True, store=True)