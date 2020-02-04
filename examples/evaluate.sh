ref_file=example/en-de.ref.sgm
mt_file=example/en-de.mt.sgm
output_format=json
target_langcode=de
es_port=9200

bash ./scripts/server.sh start
es_port=$es_port bash ./scripts/server.sh check-start-wait
python evaluate.py $ref_file $mt_file --output_format $output_format --target_langcode target_langcode --port $es_port
bash ./scripts/server.sh stop
