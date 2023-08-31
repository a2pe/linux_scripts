import subprocess
from collections import Counter
from datetime import datetime


def run_command(command='ps', param='-aux'):
    result = subprocess.run(
        [command, param],
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    new_file = result.stdout

    # Counting the number of lines in the output.
    num_lines = len([line for line in new_file.split('\n')])

    # Selecting the titles for the columns in the output.
    params = new_file.split('\n')[0].split(' ')

    # Excluding empty strings from the output.
    upd_params = [i for i in params if i]

    # Retrieving the data from the output excluding the command titles.
    data = [new_file.split('\n')[i].split(' ') for i in range(1, num_lines)]

    # Dumping all the data into the list to count the number of the processes per the user.
    some_data = [x for row in data for x in row if x]

    # Excluding 'Nones' from the output data, but leaving the separation of each process in the list within the list.
    upd_data = [list(filter(None, data[i])) for i in range(len(data))]

    # Selecting the users from the output.
    users = set([x[0] for x in upd_data])

    # Selecting all the CPU values from the output. Calculating the sum and selecting the maximum value.
    cpus = [float(x[2]) for x in upd_data]
    cpus_sum = sum(cpus)
    cpu_max = max(cpus)

    # Selecting all the MEM values from the output. Calculating the sum and selecting the maximum value.
    mems = [float(x[3]) for x in upd_data]
    mems_sum = sum(mems)
    mems_max = max(mems)

    # Extracting the PIDs from the output with the maximum CPU and MEM.
    max_mem_pid = int([x[1] for x in upd_data if float(x[3]) == mems_max][0])
    max_cpu_pid = int([x[1] for x in upd_data if float(x[2]) == cpu_max][0])

    # Building the dictionary with the number of processes per the user.
    cnt = dict(Counter(some_data))
    user_per_process = {}
    for user in users:
        if user in cnt.keys():
            user_per_process[user] = cnt[user]

    filename = datetime.now().strftime("%m-%d-%Y-%H:%M:%S") + '.txt'
    with open(filename, 'w') as f:
        f.write(f'Отчёт о состоянии системы:')
        f.write(f'Пользователи системы: {users}')
        f.write(f'Процессов запущено: {num_lines - 1}')
        f.write(f'Пользовательских процессов: {user_per_process}')
        f.write(f'Всего памяти используется: {mems_sum:.3f}')
        f.write(f'Всего CPU используется: {cpus_sum:.3f}')
        f.write(f'Больше всего памяти использует PID: {max_mem_pid}')
        f.write(f'Больше всего CPU использует PID: {max_cpu_pid}')


run_command()
