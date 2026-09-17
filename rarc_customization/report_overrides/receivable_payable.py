# rarc_customization/report_overrides/receivable_payable.py

import frappe
from frappe import _
from frappe.query_builder import DocType

from erpnext.accounts.report.accounts_receivable.accounts_receivable import (
    ReceivablePayableReport,
)

_original_prepare_ple_query = ReceivablePayableReport.prepare_ple_query
_original_build_voucher_dict = ReceivablePayableReport.build_voucher_dict
_original_get_columns = ReceivablePayableReport.get_columns
_original_get_data = ReceivablePayableReport.get_data


def prepare_ple_query_with_profit_center(self):
    _original_prepare_ple_query(self)
    ple = DocType("Payment Ledger Entry")
    self.ple_query = self.ple_query.select(ple.profit_center)


def build_voucher_dict_with_profit_center(self, ple):
    row = _original_build_voucher_dict(self, ple)
    row.profit_center = ple.get("profit_center")
    row.profit_center_name = self._profit_center_name_map.get(ple.get("profit_center"))
    return row


def get_data_with_profit_center_map(self):
    # ek hi query se saare profit center code->name map bana lo, cache ke saath
    self._profit_center_name_map = dict(
        frappe.get_all(
            "Profit Center",
            fields=["name", "profit_center_name"],
            as_list=True,
        )
    )
    _original_get_data(self)


def get_columns_with_profit_center(self):
    _original_get_columns(self)
    self.add_column(
        label=_("Profit Center"),
        fieldname="profit_center",
        fieldtype="Link",
        options="Profit Center",
    )
    self.add_column(
        label=_("Profit Center Name"),
        fieldname="profit_center_name",
        fieldtype="Data",
    )


def apply_patch():
    ReceivablePayableReport.prepare_ple_query = prepare_ple_query_with_profit_center
    ReceivablePayableReport.build_voucher_dict = build_voucher_dict_with_profit_center
    ReceivablePayableReport.get_data = get_data_with_profit_center_map
    ReceivablePayableReport.get_columns = get_columns_with_profit_center