# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2014
#    OpenERP Italian Community (<http://www.openerp-italia.org>)
#    OpenERP Italian Partner
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import string
import vatnumber

from openerp.osv import fields, osv
from openerp.tools.translate import _

class utility_service_invoice(osv.osv):
    
    _inherit = 'res.partner'

    _columns = {
        'fiscalcode_invoice': fields.char('Fiscal Code Invoice', size=16),
        'customer_invoice_name': fields.char('Customer Invoice Name', size=64),
        'date_of_birth': fields.date('Date of Birth'),
        'place_of_birth': fields.char('Place of Birth', size=64),
        'date_subscription': fields.date('Date Subscription'),
        'accounting_code': fields.char('Accounting Code', size=5),
        'counter_code': fields.char('Counter Code', size=5),
        'invoice_address': fields.char('Invoice Address', size=128),
        'invoice_zip': fields.char('Invoice Zip', size=5),
        'invoice_city': fields.char('Invoice City', size=64),
        'reading_ids': fields.one2many('consumption', 'partner_id', 'Reading')
    }

utility_service_invoice()

class cadastral_data(osv.osv):
    
    _inherit = 'res.partner'
    
    _columns = {
        'sheet': fields.char('Sheet', size=2),
        'particle': fields.char('Particle', size=3),
        'subaltern': fields.char('Subaltern', size=11),
        'notes': fields.char('Notes', size=128),
        'category': fields.char('Category', size=20),
        'income': fields.float('Income', digits=(9,2))  
    }


cadastral_data()


class consumption(osv.osv):

    _name = "consumption"

    _columns = {
        'start_reading_date': fields.date('Start Date of Reading'),
        'final_reading_date': fields.date('Final Date of Reading'),
        'start_consumption': fields.integer("Start consumption"),
        'final_consumption': fields.integer("Final consumption"),
        'consumption': fields.integer('Consumption'),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        'invoice_id': fields.many2one('account.invoice', 'Invoice Rel'),
        'consumption_notes': fields.char('Consumption Notes', size=150),
        'account_balance': fields.float('Account Balance', digits=(9,2))
    }
    
consumption()


class invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    _columns = {
        'reading_ids': fields.one2many('consumption', 'invoice_id', 'Reading')
    }


    def invoice_print(self, cr, uid, ids, context=None):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        return self.pool['report'].get_action(cr, uid, ids, 'utility_service_invoice.report_cogemo_invoice', context=context)

invoice()
