# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from dominate.tags import div, img, p, span

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.tools import file_open
from trytond.transaction import Transaction
from trytond.modules.html_report import words
from trytond.modules.html_report.dominate_report import DominateReport
from trytond.modules.html_report.engine import render as html_render
from trytond.modules.html_report.i18n import _


class Payment(metaclass=PoolMeta):
    __name__ = 'account.payment'

    amount_literal = fields.Function(fields.Char('Amount Literal'),
        'get_amount_literal')

    def get_amount_literal(self, name):
        lang_code = self.party.lang.code if self.party and self.party.lang else None
        return words.number_to_words(self.amount, lang=lang_code)


class Receipt(DominateReport):
    __name__ = 'account.payment.receipt'
    _single = True

    @classmethod
    def language(cls, records):
        record = records[0] if records else None
        if record and record.party and record.party.raw.lang:
            return record.party.raw.lang.code
        return Transaction().language or 'en'

    @classmethod
    def css(cls, action, data, records):
        with file_open('account_payment_receipt/receipt.css') as css_file:
            return css_file.read()

    @classmethod
    def show_company_info(cls, company, show_party=True,
            show_contact_mechanism=True, show_phone=True,
            show_email=True, show_website=True):
        return cls.common().show_company_info(
            company, show_party=show_party,
            show_contact_mechanism=show_contact_mechanism,
            show_phone=show_phone, show_email=show_email,
            show_website=show_website)

    @classmethod
    def header(cls, action, data, records):
        pass

    @classmethod
    def footer(cls, action, data, records):
        pass

    @classmethod
    def _invoice_number(cls, record):
        return (record.line and record.line.origin
            and record.line.origin.render.rec_name or '')

    @classmethod
    def _receipt_number(cls, record):
        return (record.line and record.line.move
            and record.line.move.render.number or '')

    @classmethod
    def _maturity_date(cls, record):
        return (record.line and record.line.raw.maturity_date
            and html_render(record.line.raw.maturity_date) or '')

    @classmethod
    def _payment_address(cls, record):
        address = record.party.addresses[0] if record.party.addresses else None
        return address.render.street_single_line if address else ''

    @classmethod
    def _amount_display(cls, record):
        return '# %s %s #' % (
            html_render(record.raw.amount),
            record.currency.render.symbol)

    @classmethod
    def body(cls, action, data, records):
        record, = records
        company = record.company

        page = div(cls='receipt-page')

        company_box = div(cls='receipt-company')
        if company.render.logo:
            company_box.add(img(src=company.render.logo, cls='receipt-logo'))
        company_info = div(cls='receipt-company-info')
        company_info.add(cls.show_company_info(company))
        company_box.add(company_info)
        page.add(company_box)

        receipt_box = div(cls='receipt-field blue-box receipt-number-box')
        receipt_box.add(span(_('RECEIPT NUM.'), cls='field-label'))
        receipt_box.add(span(cls._receipt_number(record), cls='field-value'))
        page.add(receipt_box)

        invoice_box = div(cls='receipt-field blue-box invoice-number-box')
        invoice_box.add(span(_('INVOICE NUM.'), cls='field-label'))
        invoice_box.add(span(cls._invoice_number(record), cls='field-value'))
        page.add(invoice_box)

        amount_display_box = div(cls='receipt-field blue-box amount-number-box')
        amount_display_box.add(span(_('IMPORT EUROS'), cls='field-label'))
        amount_display_box.add(span(cls._amount_display(record),
                cls='field-value amount-number-value'))
        page.add(amount_display_box)

        date_box = div(cls='receipt-field blue-box receipt-date-box')
        date_box.add(span(_('DATE'), cls='field-label'))
        date_box.add(span(html_render(record.raw.date), cls='field-value'))
        page.add(date_box)

        maturity_box = div(cls='receipt-field blue-box maturity-box')
        maturity_box.add(span(_('MATURITY'), cls='field-label'))
        maturity_box.add(span(cls._maturity_date(record), cls='field-value'))
        page.add(maturity_box)

        maturity_note = div(cls='receipt-note')
        maturity_note.add(_('For this RECEIPT you will pay on specified maturity'))
        page.add(maturity_note)

        amount_box = div(cls='receipt-amount blue-box')
        amount_box.add(span(_('the quantity of:'), cls='field-label inline'))
        amount_box.add(p(record.render.amount_literal.lower(),
                cls='amount-literal'))
        page.add(amount_box)

        payment_box = div(cls='receipt-payment blue-box')
        payment_box.add(p(_('payment at the address below:'), cls='section-title'))
        entity_row = div(cls='payment-row')
        entity_row.add(span(_('PERSON OR ENTITY'), cls='field-label side-label'))
        entity_row.add(span(record.party.render.rec_name, cls='field-value'))
        payment_box.add(entity_row)
        address_row = div(cls='payment-row')
        address_row.add(span(_('ADDRESS'), cls='field-label side-label'))
        address_row.add(span(cls._payment_address(record), cls='field-value'))
        payment_box.add(address_row)
        account_box = div(cls='receipt-account blue-box')
        account_box.add(span(_('ACCOUNT NUM.'), cls='field-label account-label'))
        account_box.add(p(record.bank_account.render.rec_name if record.bank_account else '',
                cls='account-value'))

        payment_section = div(cls='receipt-payment-section')
        payment_section.add(payment_box)
        payment_section.add(account_box)
        page.add(payment_section)

        bottom_box = div(cls='receipt-bottom blue-box')
        bottom_box.add(div(record.render.reference or '', cls='receipt-description'))
        bottom_box.add(div(company.party.render.rec_name.upper(),
                cls='receipt-company-sign'))
        page.add(bottom_box)

        return page
