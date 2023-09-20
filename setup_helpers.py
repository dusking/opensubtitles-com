from setuptools.dist import Distribution


def wheel_name(**kwargs):
    # create a fake distribution from arguments
    dist = Distribution(attrs=kwargs)
    # finalize bdist_wheel command
    bdist_wheel_cmd = dist.get_command_obj('bdist_wheel')
    bdist_wheel_cmd.ensure_finalized()
    # assemble wheel file name
    dist_name = bdist_wheel_cmd.wheel_dist_name
    tag = '-'.join(bdist_wheel_cmd.get_tag())
    return f'{dist_name}-{tag}.whl'
