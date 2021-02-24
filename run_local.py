#! /usr/bin/python3

from dumify import lambda_function

"""
    Use this script to run dumify() and isdumified() locally.
"""


def main():
    undumified = 'My name is Elon Musk and I want to build rockets so I can die on Mars.'
    dumified = lambda_function.dumify(undumified)
    isdumified = lambda_function.isdumified(dumified)


if __name__ == '__main__':
    main()
