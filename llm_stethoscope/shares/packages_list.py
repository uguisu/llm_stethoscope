# coding=utf-8
# author xin.he

# all required packages
REQUIRED_PACKAGES = [
    "nvitop==1.3.1",
    "openai==1.2.2",
]


def make_sure_packages(logger, is_auto_install_package: bool = True):
    """
    make sure all required packages are installed
    :param logger: logger
    :param is_auto_install_package: auto install package
    """

    # user can skip package install step
    if not is_auto_install_package:
        # skip install
        return

    from dynamicPip import DynamicPip, StaticResources

    d_pip = DynamicPip()

    for req_pkg in REQUIRED_PACKAGES:
        d_pip.install_single_package(req_pkg)

    del d_pip
