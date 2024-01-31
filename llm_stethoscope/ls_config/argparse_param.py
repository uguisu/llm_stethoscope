# coding=utf-8
# author xin.he
from absl.flags import argparse_flags as argparse


def declare_argparse():
    parser = argparse.ArgumentParser(description="Large Language Model(llm) stethoscope")

    parser.add_argument('--configFile',
                        action='store',
                        dest='configFile',
                        default=None,
                        help='Config file path')

    return parser


args = declare_argparse().parse_args()
