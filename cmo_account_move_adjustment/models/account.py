# -*- coding: utf-8 -*-
from openerp import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        # For adj journal
        invoice_id = self._context.get('src_invoice_id', False)
        if invoice_id:
            Invoice = self.env['account.invoice']
            invoice = Invoice.browse(invoice_id)
            invoice.write({'adjust_move_id': move.id})
        # For unbilled case
        invoice_id = self._context.get('src_unbilled_invoice_id', False)
        if invoice_id:
            Invoice = self.env['account.invoice']
            invoice = Invoice.browse(invoice_id)
            invoice.write({'unbilled_move_id': move.id})
        return move
