require 'csv'
require 'rake'

# converts csv file to text file to be consumed by deid
#
# USAGE ruby convert_csv_to_text.rb path/to/generated.csv
#
# OUTPUT path/to/generated.text

csv_file_path = ARGV[0]
csv_records = CSV.read(csv_file_path, headers: true)
text_content = csv_records.map do |row|
  "START_OF_RECORD=#{row['patient_id']}||||#{row['id']}||||\n"\
  "#{row['note']}\n"\
  "||||END_OF_RECORD"
end.join("\n")

text_output_path = csv_file_path.ext('text')
IO.write(text_output_path, text_content)
