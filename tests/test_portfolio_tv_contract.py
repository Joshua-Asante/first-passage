import pandas as pd

import portfolio_mc


def test_portfolio_normalization_wrapper_supports_futures_return_alias():
    raw = pd.DataFrame(
        {
            "Trade number": [1],
            "Net PnL USD": [25.0],
            "Return %": [0.5],
        }
    )

    normalized = portfolio_mc._normalize_tv_columns(raw)

    assert normalized.columns.tolist() == ["Trade #", "Net P&L USD", "Net P&L %"]
    assert normalized.iloc[0].tolist() == [1.0, 25.0, 0.5]
