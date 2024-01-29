# coding=utf-8
# author xin.he
from ..ls_config import ConfigInfo

# all required packages
REQUIRED_PACKAGES = [
    "nvitop==1.3.1",
    "openai==1.3.7",
    "mpi4py==3.1.5",
    'numpy==1.24.3',
    'requests==2.31.0',
    'absl-py==2.1.0',
]


def make_sure_packages(config_info_entity: ConfigInfo):
    """
    make sure all required packages are installed
    :param config_info_entity: an instance of ConfigInfo
    """

    # user can skip package install step
    if not config_info_entity.dynamic_pip_is_auto_install_package:
        # skip install
        return

    from dynamicPip import DynamicPip, StaticResources

    d_pip = DynamicPip()

    if config_info_entity.dynamic_pip_proxy is not None:
        # for users who want to use mirror
        d_pip.set_mirror_list([
            StaticResources.DEFAULT_PYPI_HOST,
            config_info_entity.dynamic_pip_proxy,
        ])

    for req_pkg in REQUIRED_PACKAGES:
        d_pip.install_single_package(req_pkg)

    del d_pip
