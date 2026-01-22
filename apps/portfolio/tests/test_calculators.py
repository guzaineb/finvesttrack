import pytest
from decimal import Decimal
from datetime import date, timedelta
from apps.portfolio.services.calculators import (
    SimpleROICalculator,
    AnnualizedROICalculator
)

class FakeAsset:
    performance_percentage = 20.0
    purchase_date = date.today() - timedelta(days=365)

def test_simple_roi_calculator():
    calculator = SimpleROICalculator()
    asset = FakeAsset()

    assert calculator.calculate(asset) == 20.0


def test_annualized_roi_calculator():
    calculator = AnnualizedROICalculator()
    asset = FakeAsset()

    result = calculator.calculate(asset)
    assert isinstance(result, float)
