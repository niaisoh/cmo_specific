# -*- coding: utf-8 -*-
from openerp import models, fields, api


class PurchasePRQ(models.Model):
    _name = 'purchase.prq'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(
        string='Number',
    )
    type = fields.Selection(
        [('purchase', 'Purchase Order'),
         ('expense', 'Expense')],
        string='Type',
    )
    purchase_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order Ref',
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice Ref',
    )
    installment = fields.Integer(
        string='Installment',
    )
    prepare_user_id = fields.Many2one(
        'res.users',
        string='Prepared By',
        default=lambda self: self.env.user,
    )
    approve_user_id = fields.Many2one(
        'res.users',
        string='Approved By',
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('approve', 'Approved'),
         ('reject', 'Rejected')],
        default='draft',
        string='Status',
        copy=False,
    )
    note = fields.Text(
        string='Note',
    )
    invoice_line_ids = fields.One2many(
        'account.invoice.line',
        related='invoice_id.invoice_line',
        string='Invoice Detailed',
    )
    expense_id = fields.Many2one(
        'hr.expense.expense',
        string='Expense Ref',
    )
    expense_line_ids = fields.One2many(
        'hr.expense.line',
        related='expense_id.line_ids',
        string='Expense Detailed',
    )

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.multi
    def action_approve(self):
        self.write({'state': 'approve', 'approve_user_id': self.env.user.id})
        return True

    @api.multi
    def action_reject(self):
        self.write({'state': 'reject'})
        return True

    @api.model
    def create(self, vals):
        # Find doctype_id
        doctype = self.env['res.doctype'].get_doctype('purchase_prq')
        fiscalyear_id = self.env['account.fiscalyear'].find()
        # --
        self = self.with_context(doctype_id=doctype.id,
                                 fiscalyear_id=fiscalyear_id)
        vals['name'] = self.env['ir.sequence'].next_by_doctype()
        return super(PurchasePRQ, self).create(vals)
