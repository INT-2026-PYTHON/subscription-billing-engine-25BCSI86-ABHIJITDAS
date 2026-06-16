"""
PaymentGateway — abstract + two mock implementations.

In real life this would talk to Stripe / Razorpay / Adyen. For the project
we use mocks so tests are deterministic and the demo never hits the network.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from billing_engine.models import Invoice


@dataclass(frozen=True)
class PaymentResult:
    success: bool
    failure_reason: Optional[str] = None


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, invoice: Invoice) -> PaymentResult:
        raise NotImplementedError


# ----------------------------------------------------------------
# # ----------------------------------------------------------------
# Scripted — for deterministic tests
# ----------------------------------------------------------------
class ScriptedGateway(PaymentGateway):
    """Returns pre-set results from a queue. Used in tests."""

    def __init__(self, results: list[PaymentResult]) -> None:
        self._results = list(results)

    def charge(self, invoice: Invoice) -> PaymentResult:
        if not self._results:
            raise RuntimeError(
                "ScriptedGateway has no remaining scripted results."
            )

        return self._results.pop(0)


# ----------------------------------------------------------------
# Fake-random — for the CLI demo
# ----------------------------------------------------------------
class FakeRandomGateway(PaymentGateway):
    """Succeeds at a configurable rate; seeded for reproducibility."""

    def __init__(
        self,
        success_rate: float = 0.7,
        seed: Optional[int] = None,
    ) -> None:
        import random

        if not 0 <= success_rate <= 1:
            raise ValueError(
                "success_rate must be between 0 and 1."
            )

        self.success_rate = success_rate
        self._random = random.Random(seed)

    def charge(self, invoice: Invoice) -> PaymentResult:
        if self._random.random() < self.success_rate:
            return PaymentResult(True)

        return PaymentResult(
            False,
            "PAYMENT_DECLINED",
        )