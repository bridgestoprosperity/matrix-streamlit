import pandas as pd
import datapane as dp

def report_builder(span, total_costs):
    report = dp.Select(
        dp.Group(
            dp.Text(f"Total span: {span} m"),
            dp.Table(total_costs)
        )
    )
    dp.save_report(report, path='report.html', open=True)