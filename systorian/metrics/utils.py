import subprocess


def maybe_find_data_at_indices(output, first_index, second_index):
    try:
        return output[first_index].split()[second_index]
    except IndexError:
        return '^NODATA'  # ^ is not normally in top's output


def read_top(command):
    """ Parse the output of bash's `top` command when called for a single
    iteration with no processes listed (this returns only system usage info).

    Optional keyword arguments
        - `options` : Adds supplied CLI flags to the `top` command; e.g. `-d`
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error_code = process.communicate()
    if error_code:
        # For the logger in metrics.tasks
        raise Exception(
            'error in read_top: subprocess encountered an error while running '
            '{}'.format(command)
        )

    output = output.split('\n')

    stats = {
        'processes': {
            'total': maybe_find_data_at_indices(output, 0, 1),
            'running': maybe_find_data_at_indices(output, 0, 3),
            'stuck': maybe_find_data_at_indices(output, 0, 5),
            'sleeping': maybe_find_data_at_indices(output, 0, 7),
            'threads': maybe_find_data_at_indices(output, 0, 9),
        },
        'capture_time': {  # This is NOT the same data as `Entry.created`
            'date': maybe_find_data_at_indices(output, 1, 0),
            'time': maybe_find_data_at_indices(output, 1, 1),
        },
        'load_avg': {
            'one_minute': maybe_find_data_at_indices(output, 2, 2),
            'five_minute': maybe_find_data_at_indices(output, 2, 3),
            'fifteen_minute': maybe_find_data_at_indices(output, 2, 4),
        },
        'cpu_usage': {
            'user': maybe_find_data_at_indices(output, 3, 2),
            'sys': maybe_find_data_at_indices(output, 3, 4),
            'idle': maybe_find_data_at_indices(output, 3, 6),
        },
        'sharedlibs': {
            'resident': maybe_find_data_at_indices(output, 4, 1),
            'data': maybe_find_data_at_indices(output, 4, 3),
            'linkedit': maybe_find_data_at_indices(output, 4, 5),

        },
        'memregions': {
            'total': maybe_find_data_at_indices(output, 5, 1),
            'resident': maybe_find_data_at_indices(output, 5, 3),
            'private': maybe_find_data_at_indices(output, 5, 5),
            'shared': maybe_find_data_at_indices(output, 5, 7),
        },
        'physmem': {
            'used': maybe_find_data_at_indices(output, 6, 1),
            'wired': maybe_find_data_at_indices(output, 6, 3).strip('('),
            'unused': maybe_find_data_at_indices(output, 6, 5),
        },
        'vm': {
            'vsize': maybe_find_data_at_indices(output, 7, 1),
            'framework_vsize': maybe_find_data_at_indices(output, 7, 3),
            'swapins': maybe_find_data_at_indices(output, 7, 6),
            'swapouts': maybe_find_data_at_indices(output, 7, 8),
        },
        'networks': {
            'packets_in': maybe_find_data_at_indices(output, 8, 2),
            'packets_out': maybe_find_data_at_indices(output, 8, 4),
        },
        'disks': {
            'read': maybe_find_data_at_indices(output, 9, 1),
            'written': maybe_find_data_at_indices(output, 9, 3)
        },
    }

    return stats
