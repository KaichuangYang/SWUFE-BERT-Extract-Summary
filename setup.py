#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Yu Zheng",
    author_email='yu.zheng@inboc.net',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="python code of group2. Fine-tuning the swufe-bert model with extractive summary task.",
    entry_points={
        'console_scripts': [
            'extract_summary_finetune=extract_summary_finetune.main:run_tool',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='extract_summary_finetune',
    name='extract_summary_finetune',
    packages=find_packages(include=['extract_summary_finetune', 'extract_summary_finetune.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/yu.zheng/extract_summary_finetune',
    version='0.1.0',
    zip_safe=False,
    package_data={'': ['*.yaml']},
)
