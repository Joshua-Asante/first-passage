---
name: pinescript-v6
description: Write, review, debug, or refactor Pine Script v6 code for TradingView. Use this skill whenever the user mentions Pine Script, TradingView strategies or indicators, .pine files, or asks to build/fix/optimize any trading script. Also trigger for locked-book strategy work (Guardian Gold, Striker DJ30/NAS100 and their MYM/MNQ venue editions), backtesting scripts, alert conditions, or any task involving ta.*, strategy.*, request.security(), or other Pine Script functions.
---

# Pine Script v6 Developer Skill

Specialized in writing production-quality Pine Script v6 code for TradingView.

---

## ⚠️ CRITICAL: Pine Script Syntax Rules

BEFORE writing ANY multi-line Pine Script code, remember:

- **TERNARY OPERATORS (`? :`)** — MUST stay on ONE line or use intermediate variables
- **Line continuation** — ALL continuation lines must be indented MORE than the starting line
- **Common error:** `"end of line without line continuation"` — caused by improper line breaks

---

## CRITICAL: Ternary Operators MUST Stay on One Line

```pine
// ❌ WRONG - Will cause "end of line without line continuation" error
text = condition ?
    "true value" :
    "false value"

// ✅ CORRECT - Entire ternary on one line
text = condition ? "true value" : "false value"

// ✅ CORRECT - For long ternaries, assign intermediate variables
trueText = str.format("Long true value with {0}", param)
falseText = str.format("Long false value with {0}", other)
text = condition ? trueText : falseText
```

---

## CRITICAL: Line Wrapping Rules

Pine Script has STRICT line continuation rules:

- Lines MUST be indented **more** than the first line
- Break at operators/commas: split AFTER operators or commas, not before
- No explicit continuation character in Pine Script v6

```pine
// ✅ CORRECT - indented continuation
longCondition = ta.crossover(ema50, ema200) and
     rsi < 30 and
     volume > ta.sma(volume, 20)

// ✅ CORRECT - function arguments
plot(series,
     title="My Plot",
     color=color.blue,
     linewidth=2)

// ❌ WRONG - same indentation (WILL CAUSE ERRORS)
longCondition = ta.crossover(ema50, ema200) and
rsi < 30 and
volume > ta.sma(volume, 20)
```

### SYSTEMATIC CHECK — Review ALL of these before finalizing:
- [ ] `indicator()` or `strategy()` declarations at the top
- [ ] All `plot()`, `plotshape()`, `plotchar()` functions
- [ ] All `if` statements with multiple conditions
- [ ] All variable assignments with long expressions
- [ ] All `strategy.entry()`, `strategy.exit()` calls
- [ ] All `alertcondition()` calls
- [ ] All `table.cell()` calls
- [ ] All `label.new()` and `box.new()` calls
- [ ] Any line longer than 80 characters

---

## CRITICAL: Plot Scope Restriction

NEVER use `plot()` inside local scopes — causes `"Cannot use 'plot' in local scope"` error.

```pine
// ❌ WRONG - These will ALL fail:
if condition
    plot(value)       // ERROR!
for i = 0 to 10
    plot(close[i])    // ERROR!
myFunc() =>
    plot(close)       // ERROR!

// ✅ CORRECT - Use these patterns instead:
plot(condition ? value : na)
plot(value, color=condition ? color.blue : color.new(color.blue, 100))

// For dynamic drawing in local scopes, use:
if condition
    line.new(...)     // OK
    label.new(...)    // OK
    box.new(...)      // OK
```

---

## Script Structure Template

```pine
//@version=6
indicator(title="", shorttitle="", overlay=true)

// ============================================================================
// INPUTS
// ============================================================================

// ============================================================================
// CALCULATIONS
// ============================================================================

// ============================================================================
// CONDITIONS
// ============================================================================

// ============================================================================
// PLOTS
// ============================================================================

// ============================================================================
// ALERTS
// ============================================================================
```

---

## TradingView Platform Limits

| Constraint | Limit |
|---|---|
| Historical bars reference | 500 max |
| plot/hline/fill outputs | 500 max |
| Drawing objects (label/line/box/table) | 64 max |
| `security()` calls | 40 max |
| Compiled script size | 100KB max |
| Table cells | 100 max |
| Array elements | 100,000 max |

Compile/object caps only. **Strategy Report / Deep / continuous-futures (`1!`) warehouse** is a different limiter — chart candles and `plotchar` can run after the report series has already ended. Owner: [`docs/notes/research/2026-08-28-tradingview-strategy-report-july-2026.md`](../../../docs/notes/research/2026-08-28-tradingview-strategy-report-july-2026.md).

### Strategy Report traps (July 2026+)

Read the note before rewriting entries because “trades stopped in April.” Short checklist:

1. Price pane ≠ Strategy Report. Chart arrows are always **regular** (chart-loaded bars). Any non-default **Testing period** activates **Deep**; those fills live in the report only.
2. `Available chart range` / Last-N / custom dates can still be Deep-class. Reset gray means you are already on the advertised default — not “you left Deep.”
3. `MNQ1!` / `NQ1!` / `ES1!` Deep is a spliced warehouse with extra depth rules. Partial data is **silent** (no error). Buy-and-hold on the **report** dying with the last fill = engine bars ended, not “no setups.”
4. **Bar detalization** `High` pulls a lower TF (15m→2m / 28 ticks; 30m→5m / 24 ticks). `Default` is 4 OHLC ticks. The detalization menu being visible is not Magnifier-on.
5. **Script execution** dropdown is calc events (`On bar close` always on). It is not the unread warning log.
6. Do not gate diagnostic tables on `barstate.islast`. Put a `var table` of `strategy.closedtrades` on the **candlestick** pane.
7. Regular mode now **trims at 9,000** trades (no error-and-stop). Deep keeps up to 1M. `500` is labels/lines, not a documented trade cap.
8. To split “Pine died” vs “`1!` warehouse died”: same script on the **dated front month**, then 1h/4h `1!`, then Last-90. A **different** `1!` that still prints on the same Deep Last-N pane rules out a global Deep hole — it does not clear the dead symbol. Do not judge post-cliff logic on a `1!` pane whose report B&H already flatlined.

This does **not** unpark a FALSIFIED/PARK candidate.

---

## Best Practices

### Avoid Repainting
- Use `barstate.isconfirmed` for signals
- Use `request.security()` with `lookahead=barmerge.lookahead_off`
- Document any intentional repainting

### Performance Optimization
- Minimize `security()` calls
- Cache repeated calculations in variables
- Use `switch` instead of multiple `if/else` chains

### User Experience
- Group inputs with `group=` parameter
- Add `tooltip=` for complex inputs
- Use sensible default values

### Error Handling
- Check for `na` values before operations
- Handle edge cases (first bars, division by zero)

---

## Config-Fingerprint Convention (ACTIVE-DERIVATION scripts)

Ratified 2026-06-11 (`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`, proposal P3). All ACTIVE-DERIVATION strategy scripts embed the current cfg-ID in the strategy title, updated per run, so TradingView export filenames self-identify their configuration:

```pine
strategy(title="SVRN USDCAD v0.2-X15 [cfg10]", ...)
```

- Update the `[cfgNN]` tag **every run** — the tag must match the config actually loaded, not the script's lineage.
- Step-0 of the reconcile pipeline parses the tag out of the export filename and verifies it against the declared run; a mismatch halts analysis.
- **Exemption: frozen / pre-registered scripts** (e.g. BPC USDCAD Tuesday) are immutable and exempt — their exports are identified by the pre-registration itself. Never retro-tag a frozen script for convention uniformity.
- Existing active scripts adopt at their next legitimate edit, not as a standalone title-only touch (a convention-only edit creates a phantom config generation).

Rationale: three relay defects on 2026-06-11 alone (wrong timeframe, duplicate export, mislabeled subset) were caught only by manual review; the tag makes the class machine-detectable.

---

## Code Review Checklist

- [ ] Version declaration (`//@version=6`)
- [ ] Proper title and overlay setting
- [ ] Inputs have tooltips and groups
- [ ] No repainting issues
- [ ] `na` values handled
- [ ] Efficient calculations
- [ ] Clear variable names
- [ ] Comments for complex logic
- [ ] Proper plot styling
- [ ] Alert conditions if needed

---

## Example: Moving Average Cross Strategy

```pine
//@version=6
strategy("MA Cross Strategy", overlay=true,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=10)

// Inputs
fastLength = input.int(50, "Fast MA Length", minval=1, group="Moving Averages")
slowLength = input.int(200, "Slow MA Length", minval=1, group="Moving Averages")
maType = input.string("EMA", "MA Type",
     options=["SMA", "EMA", "WMA"],
     group="Moving Averages")

// Calculations
ma(source, length, type) =>
    switch type
        "SMA" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "WMA" => ta.wma(source, length)

fastMA = ma(close, fastLength, maType)
slowMA = ma(close, slowLength, maType)

// Conditions
longCondition = ta.crossover(fastMA, slowMA)
shortCondition = ta.crossunder(fastMA, slowMA)

// Strategy
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.close("Long")

// Plots
plot(fastMA, "Fast MA", color.blue, 2)
plot(slowMA, "Slow MA", color.red, 2)
```
