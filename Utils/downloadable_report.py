import pandas as pd
import datapane as dp

def report_builder(span, total_costs):
    report = dp.Report(

            dp.Text(f"Total span: {span} m"),
            dp.Table(total_costs)

    )
    report.save(path='report.html', open=True)

