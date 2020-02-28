from googleads import ad_manager, errors
from datetime import datetime, timedelta
import tempfile
import csv
import gzip
import pprint
import json

# Initialize a client object, by default uses the credentials in ~/googleads.yaml.
ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()

countries = ['Brazil', 'India', 'Japan', 'Malaysia', 'Philippines', 'Poland', 'South Korea', 'Thailand', 'Turkey',
             'Vietnam']

format_strings = ', '.join(map(lambda x: '%s', countries))
print('string:>>>', countries)

# Create statement object to filter for an order.
statement = (ad_manager.StatementBuilder()
             .Where(
  "COUNTRY_NAME IN ('Brazil', 'India', 'Japan', 'Malaysia', 'Philippines', 'Poland', 'South Korea', 'Thailand', 'Turkey', 'Vietnam')")
             # .Where("COUNTRY_NAME IN (:country)")
             # .WithBindVariable("country", format_strings)
             .Limit(None)  # No limit or offset for reports
             .Offset(None))
# Set the start and end dates of the report to run (past 8 days).
end_date = datetime.now().date()
start_date = end_date - timedelta(days=8)

print("start date>>>", start_date)
print("end date>>>", end_date)

# Create report job.
report_job = {
  'reportQuery': {
    'dimensions': ['COUNTRY_NAME', 'DATE'],
    'statement': statement.ToStatement(),
    'columns': ['TOTAL_LINE_ITEM_LEVEL_IMPRESSIONS', 'TOTAL_LINE_ITEM_LEVEL_CPM_AND_CPC_REVENUE',
                'TOTAL_INVENTORY_LEVEL_UNFILLED_IMPRESSIONS', 'TOTAL_FILL_RATE'],
    'dateRangeType': 'CUSTOM_DATE',
    'startDate': start_date,
    'endDate': end_date
  }
}

print(report_job)

# Initialize a DataDownloader.
report_downloader = ad_manager_client.GetDataDownloader(version='v201911')

try:
  # Run the report and wait for it to finish.
  print("Report Generating...")

  report_job_id = report_downloader.WaitForReport(report_job)
except errors.AdManagerReportError as e:
  print('Failed to generate report. Error was: %s' % e)

# Change to your preferred export format.
export_format = 'CSV_DUMP'

report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)

# Download report data.
report_downloader.DownloadReportToFile(report_job_id, export_format, report_file)

report_file.close()

# Display results.
print('Report job with id "%s" downloaded to:\n%s' % (
  report_job_id, report_file.name))

csvFile = gzip.open(report_file.name, 'rt', newline='')  # Open in text mode, not binary, no line ending translation
reader = csv.DictReader(csvFile)

data = []

for row in reader:
  data.append(row)

output_dict = json.loads(json.dumps(data))
pprint.pprint(output_dict)