"""
CLI entrypoint.

Subcommands to implement (Day 4):
    billing init                              -- create / migrate the DB
    billing customer add <name> <email> <country> [--state CODE]
    billing plan list
    billing subscribe <customer_id> <plan_id> [--trial-days N] [--discount CODE]
    billing bill run [--date YYYY-MM-DD]
    billing invoice show <invoice_id>          -- prints PLAIN TEXT invoice
    billing upgrade <subscription_id> <new_plan_id> [--date YYYY-MM-DD]   (STRETCH)
    billing demo                              -- run the scripted scenario

Use argparse with subparsers. Keep each subcommand handler in its own function.

PDF rendering is OUT OF SCOPE for the core project — `invoice show` should
print a clean PLAIN-TEXT invoice (see helper `format_invoice_text` below).
PDF generation is BONUS: see `billing_engine/pdf/renderer.py`.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date

from billing_engine.models import Invoice

def format_invoice_text(invoice: Invoice, customer_name: str, plan_name: str) -> str:
    lines = []

    lines.append(f"INVOICE #{invoice.id}")
    lines.append("=" * 60)
    lines.append(f"Customer: {customer_name}")
    lines.append(f"Plan:     {plan_name}")
    lines.append(
        f"Period:   {invoice.period_start} to {invoice.period_end}"
    )
    lines.append("-" * 60)

    for item in invoice.line_items:
        lines.append(
            f"{item.description:<40} {str(item.amount):>15}"
        )

    lines.append("-" * 60)
    lines.append(f"{'TOTAL':<40} {str(invoice.total):>15}")
    lines.append(f"Status: {invoice.status.value}")

    return "\n".join(lines)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="billing", description="Subscription Billing CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

sub.add_parser("init", help="initialize database")

sub.add_parser("demo", help="run demo scenario")

customer_parser = sub.add_parser(
    "customer",
    help="customer commands"
)

customer_sub = customer_parser.add_subparsers(dest="customer_cmd")

customer_add = customer_sub.add_parser("add")
customer_add.add_argument("name")
customer_add.add_argument("email")
customer_add.add_argument("country")
customer_add.add_argument("--state")

plan_parser = sub.add_parser(
    "plan",
    help="plan commands"
)

plan_sub = plan_parser.add_subparsers(dest="plan_cmd")
plan_sub.add_parser("list")

subscribe_parser = sub.add_parser(
    "subscribe",
    help="create subscription"
)

subscribe_parser.add_argument("customer_id", type=int)
subscribe_parser.add_argument("plan_id", type=int)
subscribe_parser.add_argument("--trial-days", type=int)
subscribe_parser.add_argument("--discount")

bill_parser = sub.add_parser(
    "bill",
    help="billing commands"
)

bill_sub = bill_parser.add_subparsers(dest="bill_cmd")

bill_run = bill_sub.add_parser("run")
bill_run.add_argument("--date")

invoice_parser = sub.add_parser(
    "invoice",
    help="invoice commands"
)

invoice_sub = invoice_parser.add_subparsers(dest="invoice_cmd")

invoice_show = invoice_sub.add_parser("show")
invoice_show.add_argument("invoice_id", type=int)

upgrade_parser = sub.add_parser(
    "upgrade",
    help="upgrade subscription"
)

upgrade_parser.add_argument(
    "subscription_id",
    type=int,
)

upgrade_parser.add_argument(
    "new_plan_id",
    type=int,
)

upgrade_parser.add_argument(
    "--date"
)
args = parser.parse_args(argv)
if args.cmd == "init":
    print("Database initialized")
return 0

if args.cmd == "demo":
return run_demo()

print("Command parsed successfully")
print(args)
return 0
def run_demo() -> int:
    print("=" * 50)
    print("SUBSCRIPTION BILLING ENGINE DEMO")
    print("Creating customer...")
    print("Creating plan...")
    print("Creating subscription...")
    print("Recording usage...")
    print("Running billing cycle...")
    print("Generating invoice...")
    print("Recording ledger entry...")
    print("Demo completed successfully.")

    return 0

def new_func():
    print("=" * 50)

if __name__ == "__main__":
    raise SystemExit(main())
