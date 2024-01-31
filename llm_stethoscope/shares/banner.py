# coding=utf-8
# author xin.he

from llm_stethoscope.static_info import __version__

logo = f"""\033[92m
-------------------------------------------------------------------------------
┬  ┬  ┌┬┐  ╔═╗┌┬┐┌─┐┌┬┐┬ ┬┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐
│  │  │││  ╚═╗ │ ├┤  │ ├─┤│ │└─┐│  │ │├─┘├┤ 
┴─┘┴─┘┴ ┴  ╚═╝ ┴ └─┘ ┴ ┴ ┴└─┘└─┘└─┘└─┘┴  └─┘

           -- Version {__version__} --
-------------------------------------------------------------------------------\033[0m
"""


def show_logo(sleep_second=0.8):
    import time
    print(logo)
    time.sleep(sleep_second)
