"""
GSTCalculator — Indian Goods & Services Tax.

The rule:
    - If customer_state == seller_state (or seller_state is "")  =>  intra-state
        -> charge CGST + SGST (split equally, e.g. 9% + 9% = 18%)
    - Else  =>  inter-state
        -> charge IGST (e.g. 18%)

Customers without a state code default to IGST (safe choice).
"""

from decimal import Decimal

from billing_engine.money import Money
from billing_engine.taxes.base import TaxCalculator, TaxContext, TaxBreakdown


class GSTCalculator(TaxCalculator):
    def __init__(self, cgst: Decimal, sgst: Decimal, igst: Decimal) -> None:
        for rate in (cgst, sgst, igst):
            if isinstance(rate, float):
                raise TypeError("tax rates must not be float")

            if rate < Decimal("0") or rate > Decimal("1"):
                raise ValueError("tax rates must be between 0 and 1")

        if cgst + sgst != igst:
            raise ValueError("cgst + sgst must equal igst")

        self.cgst = cgst
        self.sgst = sgst
        self.igst = igst

    def apply(self, taxable: Money, context: TaxContext) -> TaxBreakdown:
        intra = (
            bool(context.customer_state)
            and (
                context.seller_state == ""
                or context.customer_state == context.seller_state
            )
        )

        if intra:
            cgst_tax = taxable * self.cgst
            sgst_tax = taxable * self.sgst

            return TaxBreakdown(
                components=[
                    (f"CGST {int(self.cgst * 100)}%", cgst_tax),
                    (f"SGST {int(self.sgst * 100)}%", sgst_tax),
                ],
                total=cgst_tax + sgst_tax,
            )

        igst_tax = taxable * self.igst

        return TaxBreakdown(
            components=[
                (f"IGST {int(self.igst * 100)}%", igst_tax),
            ],
            total=igst_tax,
        )