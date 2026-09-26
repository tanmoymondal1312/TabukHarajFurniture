import math

from django.utils.safestring import mark_safe


def _axis(peak):
    """Pick a top value and tick step that give clean labels."""
    if peak <= 4:
        return 4, [0, 1, 2, 3, 4]
    exp = math.floor(math.log10(peak))
    for e in (exp, exp - 1):
        base = 10 ** e
        for mult in (1, 2, 2.5, 5, 10):
            step = base * mult
            count = math.ceil(peak / step)
            if 3 <= count <= 6 and step * count >= peak:
                vmax = step * count
                ticks = [step * i for i in range(count + 1)]
                return vmax, [_clean(t) for t in ticks]
    return peak, [peak * k / 4 for k in range(5)]


def _clean(value):
    return int(value) if float(value).is_integer() else value


def line_chart(days, series, height=260, width=760):
    """SVG line chart. `days` are x labels, `series` hold aligned int values."""
    left, right, top, bottom = 44, 14, 16, 30
    inner_w = width - left - right
    inner_h = height - top - bottom
    n = len(days)
    if not n:
        return mark_safe("")

    peak = max(max(s["values"]) for s in series)
    vmax, ticks = _axis(peak)

    def x(i):
        return left + (inner_w * i / (n - 1)) if n > 1 else left + inner_w / 2

    def y(v):
        return top + inner_h - (inner_h * v / vmax)

    parts = []
    for val in ticks:
        yy = y(val)
        parts.append(
            f'<line x1="{left}" y1="{yy:.1f}" x2="{width - right}" y2="{yy:.1f}" '
            f'stroke="#EFEFED" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{left - 8}" y="{yy + 4:.1f}" text-anchor="end" '
            f'class="chart__tick">{val}</text>'
        )

    label_step = max(1, math.ceil(n / 8))
    for i in range(0, n, label_step):
        parts.append(
            f'<text x="{x(i):.1f}" y="{height - 8}" text-anchor="middle" '
            f'class="chart__tick">{days[i].strftime("%d %b")}</text>'
        )

    for s in series:
        color = s["color"]
        values = s["values"]
        if s.get("fill") and n > 1:
            area = f"M {x(0):.1f},{y(0):.1f} "
            area += " ".join(
                f"L {x(i):.1f},{y(v):.1f}" for i, v in enumerate(values)
            )
            area += f" L {x(n - 1):.1f},{y(0):.1f} Z"
            parts.append(f'<path d="{area}" fill="{color}" opacity="0.12"/>')
        points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
        parts.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        if n <= 90:
            for i, v in enumerate(values):
                tip = f"{days[i].strftime('%d %b %Y')} — {s['name']}: {v}"
                parts.append(
                    f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.2" fill="#fff" '
                    f'stroke="{color}" stroke-width="2"><title>{tip}</title></circle>'
                )

    svg = (
        f'<svg viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Visits over time" xmlns="http://www.w3.org/2000/svg">'
        + "".join(parts)
        + "</svg>"
    )
    return mark_safe(svg)
