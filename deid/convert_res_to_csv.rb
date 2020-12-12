require 'csv'
require 'pry'

# Converts deid res file into csv
#
# USAGE: ruby convert_res_to_csv.rb path/to/deid/generated.res og_csv_file_path
#
# OUTPUT path/to/deid/generated.res.csv

RES_REGEX = /START_OF_RECORD=(?<PT_ID>.*?)\|\|\|\|(?<ENC_ID>.*?)\|\|\|\|\n(?<NOTE>.*)/
res_file_path = ARGV[0]
og_enc_csv_file_path = ARGV[1]

og_enc_csv_records = CSV.parse(IO.read(og_enc_csv_file_path), headers: true)
res_file_content = IO.read(res_file_path)
res_records = res_file_content.
  split("\n||||END_OF_RECORD").
  map{|rec| rec.match(RES_REGEX)}.
  map{|md| {patient_id: md[:PT_ID], id: md[:ENC_ID], note: md[:NOTE]}}.
  map do |r|
    og_row = og_enc_csv_records.find{|o| o['id'] == r[:id]}
    binding.pry if og_row.nil?
    r.merge({
      purpose: og_row['purpose'],
      duration: og_row['duration']
    })
  end
res_csv = CSV.generate do |csv|
  csv << ['id', 'patient_id', 'purpose', 'duration', 'note']
  res_records.each do |row|
    csv << [
      row[:id],
      row[:patient_id],
      row[:purpose],
      row[:duration],
      row[:note]
    ]
  end
end
IO.write("#{res_file_path}.csv", res_csv)
