#!/usr/bin/python3

from distutils.core import setup

setup(name='mtk-bpf-patcher',
      version='1.0',
      description="CLI tool to patch MTK-based kernel(s) in order to fix BPF regression(s).",
      author='Roger Ortiz',
      author_email='me@r0rt1z2.com',
      url='https://github.com/R0rt1z2/mtk-bpf-patcher',
      packages=['mtk_bpf_patcher', 'mtk_bpf_patcher.utils', 'mtk_bpf_patcher.data'],
      scripts=['mtk-bpf-patcher'],
)