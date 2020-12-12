# To be used to select a sample of records after deid generator has been used
#
# USAGE: ruby sample_res.rb path/to/deid/generated.res 100
#
# OUTPUT: path/to/deid/generated.res-sample-100.res

RES_REGEX = /START_OF_RECORD=(?<PT_ID>.*?)\|\|\|\|(?<ENC_ID>.*?)\|\|\|\|\n(?<NOTE>.*)/
res_file_path = ARGV[0]
sample_number = ARGV[1] || 50

res_file_content = IO.read(res_file_path)
sampled_res_content = res_file_content.
  split("\n||||END_OF_RECORD").
  sample(sample_number.to_i).
  join("\n||||END_OF_RECORD")

IO.write(
  "#{res_file_path}-sample-#{sample_number}.res",
  sampled_res_content
)
