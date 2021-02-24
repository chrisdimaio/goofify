#! /usr/bin/python3

from dumify import lambda_function

"""
    Use this script to run dumify() locally.
"""


def main():
    print(lambda_function.dumify(
        'My name is Elon Musk and I want to build rockets so I can die on Mars.'))


if __name__ == '__main__':
    main()
