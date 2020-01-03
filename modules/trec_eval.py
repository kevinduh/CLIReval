import subprocess
import os
import json
import logging


class TrecEval():
    trec_eval_bin = "./external_tools/trec_eval/trec_eval"

    def __init__(self, qrel_f, res_f):
        self.qrel_f = qrel_f
        self.res_f = res_f
        self.metrics = None

        if not os.path.exists(self.trec_eval_bin):
            raise Exception(
                "trec_eval binary does not exists. Please download using ./scripts/install_external_tools.sh")

    def get_metrics(self):
        if not self.metrics:
            trec_eval_output = subprocess.check_output(
                [self.trec_eval_bin, "-m", "all_trec", "-M1000", self.qrel_f, self.res_f]).decode('ascii')

            self.metrics = {}
            # remove first 5 items and last item
            for metric in trec_eval_output.split('\n')[5:-2]:
                metric = metric.split('\t')
                metric_name, _, metric_value = metric
                metric_name = metric_name.strip()
                metric_value = float(metric_value)
                self.metrics[metric_name] = metric_value

        return self.metrics

    def print_metrics(self, output_format="tsv", output_file=None):
        if output_format.lower() == 'json':
            output_str = json.dumps(self.get_metrics())
        else:
            output_str = "\n".join(["%s\t%s" % (k, v)
                                    for k, v in self.get_metrics().items()])

        if output_file:
            with open(output_file, 'w') as fout:
                print(output_str, file=fout)
            logging.info("Evaluation results written to %s...", output_file)
        else:
            print(output_str)
