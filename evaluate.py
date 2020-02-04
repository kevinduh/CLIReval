import argparse
import os
import shutil
import logging
from modules import Search, DocParser, TrecEval

if __name__ == '__main__':
    cmdline_parser = argparse.ArgumentParser(description='MT2IR')

    cmdline_parser.add_argument('ref_file', help='reference file')
    cmdline_parser.add_argument('mt_file', help='translation file')
    cmdline_parser.add_argument('--doc_mapping_file', type=str,
                                default=None,
                                help='Path to an optional document boundary file. Used only ref and mt files are raw text files.')
    cmdline_parser.add_argument('--doc_length', type=int,
                                default=1,
                                help='Number of sentences per auto-generated document. This is only used when the input files are raw text files and a doc_mapping_file is not specified')
    cmdline_parser.add_argument('--port', type=int,
                                default=9200,
                                help='elasticsearch port (default: 9200)')
    cmdline_parser.add_argument(
        '--query_mode',
        type=str,
        default='sentences',
        choices=[
            'sentences',
            'unique_terms'],
        help='method used to generate queries')
    cmdline_parser.add_argument(
        '--relv_mode',
        type=str,
        default='jenks',
        choices=[
            'jenks',
            'percentile',
            'query_in_document'],
        help='method used to convert raw BM25 scores relevance judgment labels.')
    cmdline_parser.add_argument(
        '--jenks_nb_class',
        type=int,
        default=5,
        help='Number of classes for Jenks natural breaks optimization. Used only when relv_mode = jenks.')
    cmdline_parser.add_argument(
        '--n_percentile',
        type=int,
        default=25,
        help='Set relevance judgments of documents with BM25 scores in the top n percentile to 1, else 0. Used only when relv_mode = percentile.')
    cmdline_parser.add_argument(
        '--n_ret',
        type=int,
        default=100,
        help='Number of documents return by ElasticSearch.')
    cmdline_parser.add_argument('--qrel_save_path', type=str,
                                default=None,
                                help='path to save qrel file')
    cmdline_parser.add_argument('--res_save_path', type=str,
                                default=None,
                                help='path to save res file')
    cmdline_parser.add_argument('--output_format', type=str,
                                default='json',
                                choices=['tsv', 'json'],
                                help='output format of IR metrics')
    cmdline_parser.add_argument('--target_langcode', type=str,
                                default='en')
    cmdline_parser.add_argument(
        '--output_file',
        type=str,
        default=None,
        help='Write metrics to output_file. If unspecified, metrics will print to stdout.')

    args = cmdline_parser.parse_args()
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"),
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.info('Loading ref document:  %s', (args.ref_file))
    ref = DocParser(args.ref_file, args.doc_mapping_file, args.doc_length)
    ref.log_doc_stats()

    logging.info('Loading mt document: %s', (args.mt_file))
    mt = DocParser(args.mt_file, args.doc_mapping_file, args.doc_length)
    mt.log_doc_stats()

    query_iterable = ref.get_queries()

    es = Search(
        ref.get_docs(),
        mt.get_docs(),
        query_iterable,
        **vars(args))
    tmp_qrel_f, tmp_res_f = es.get_qrel_and_res_files()
    qrel_f = tmp_qrel_f
    res_f = tmp_res_f

    if args.qrel_save_path is not None:
        shutil.move(qrel_f, args.qrel_save_path)
        qrel_f = args.qrel_save_path

    if args.res_save_path is not None:
        shutil.move(res_f, args.res_save_path)
        res_f = args.res_save_path

    metrics = TrecEval(qrel_f, res_f)
    metrics.print_metrics(
        output_format=args.output_format,
        output_file=args.output_file)
