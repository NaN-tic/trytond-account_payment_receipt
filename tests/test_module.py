# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import datetime
from decimal import Decimal

from trytond.modules.account.tests import create_chart, get_fiscalyear
from trytond.modules.company.tests import (
    CompanyTestMixin, create_company, set_company)
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction


class AccountPaymentReceiptTestCase(CompanyTestMixin, ModuleTestCase):
    'Test AccountPaymentReceipt module'
    module = 'account_payment_receipt'

    @with_transaction()
    def test_receipt_report_execute(self):
        pool = Pool()
        Account = pool.get('account.account')
        FiscalYear = pool.get('account.fiscalyear')
        Journal = pool.get('account.journal')
        Move = pool.get('account.move')
        Party = pool.get('party.party')
        Address = pool.get('party.address')
        Payment = pool.get('account.payment')
        PaymentJournal = pool.get('account.payment.journal')
        PaymentType = pool.get('account.payment.type')
        Report = pool.get('account.payment.receipt', type='report')

        company = create_company()
        with set_company(company):
            create_chart(company)
            fiscalyear = get_fiscalyear(company)
            fiscalyear.save()
            FiscalYear.create_period([fiscalyear])
            period = fiscalyear.periods[0]

            journal_revenue, = Journal.search([
                    ('code', '=', 'REV'),
                    ], limit=1)
            revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ('closed', '=', False),
                    ('company', '=', company.id),
                    ], limit=1)
            receivable, = Account.search([
                    ('type.receivable', '=', True),
                    ('closed', '=', False),
                    ('company', '=', company.id),
                    ], limit=1)

            party = Party(name='Customer')
            party.addresses = [Address(street='Main street', city='City')]
            party.save()

            move, = Move.create([{
                        'period': period.id,
                        'journal': journal_revenue.id,
                        'date': period.start_date,
                        'lines': [('create', [{
                                        'account': revenue.id,
                                        'credit': Decimal('100.00'),
                                        }, {
                                        'party': party.id,
                                        'account': receivable.id,
                                        'debit': Decimal('100.00'),
                                        'maturity_date': datetime.date.today(),
                                        }])],
                        }])
            Move.post([move])
            payment_line = next(
                line for line in move.lines if line.account == receivable)

            payment_type, = PaymentType.create([{
                        'name': 'Cash',
                        'code': 'CASH',
                        'kind': 'receivable',
                        'company': company.id,
                        }])
            payment_journal, = PaymentJournal.create([{
                        'name': 'Manual',
                        'company': company.id,
                        'currency': company.currency.id,
                        'process_method': 'manual',
                        'payment_type': payment_type.id,
                        }])
            payment, = Payment.create([{
                        'company': company.id,
                        'journal': payment_journal.id,
                        'party': party.id,
                        'kind': 'receivable',
                        'amount': Decimal('100.00'),
                        'line': payment_line.id,
                        'date': datetime.date.today(),
                        'reference': 'PAY-001',
                        }])

            ext, content, _, _ = Report.execute([payment.id], {})
            self.assertEqual(ext, 'pdf')
            self.assertTrue(content)


del ModuleTestCase
