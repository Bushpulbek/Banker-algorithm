# Simulate the Banker's algorithm
import copy
import time
import os

# Given constants
RESOURCES_TYPES = 3
PROCESSES = 5

# Data structures used
available, maximum, allocation = [], [], []
need = [[0 for i in range(RESOURCES_TYPES)] for _ in range(PROCESSES)]


def safety() -> list:
    work = copy.deepcopy(available)
    finish = [False for i in range(PROCESSES)]
    safe_sequence = []
    flag = 1

    while not all(finish) and flag == 1:
        flag = 0
        for i in range(PROCESSES):
            if not finish[i] and all(need[i][k] <= work[k] for k in range(RESOURCES_TYPES)):
                for j in range(RESOURCES_TYPES):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                flag = 1

    if flag == 0:
        safe_sequence.clear()

    return safe_sequence


def resource_request(request: list, process_num: int) -> None:
    global available, allocation, need
    if any(request[i] > need[process_num][i] for i in range(RESOURCES_TYPES)):
        raise ValueError("Process's exceeded its maximum claim")

    elif any(request[i] > available[i] for i in range(RESOURCES_TYPES)):
        print('Process should wait. Resource is not available')

    else:
        for k in range(RESOURCES_TYPES):
            available[k] -= request[k]
            allocation[process_num][k] += request[k]
            need[process_num][k] -= request[k]

        sequence = safety()
        if sequence:
            print('Request is satisfiable. Safe sequence is:')
            for i in sequence:
                print(f'P{i}', end=' ')
            print()

        else:
            print('Request is not possible at the moment. Process should wait')
            print('Restoring to the previous state...')
            for k in range(RESOURCES_TYPES):
                available[k] += request[k]
                allocation[process_num][k] -= request[k]
                need[process_num][k] += request[k]
            time.sleep(5)
            print('Done')


def available_input() -> None:
    global available
    available = input('Input available resources for types 1,2,3 respectively: ')
    available = [int(i) for i in available]


def max_input() -> None:
    global maximum
    for i in range(PROCESSES):
        print(f'For process №{i}')
        max_for_process = input('Input max resources for types 1,2,3 respectively: ')
        max_for_process = [int(i) for i in max_for_process]
        maximum.append(max_for_process)


def allocation_input() -> None:
    global allocation
    for i in range(PROCESSES):
        print(f'For process №{i}')
        alloc_for_process = input('Input allocation resources for types 1,2,3 respectively: ')
        alloc_for_process = [int(i) for i in alloc_for_process]
        while any(alloc_for_process[j] > maximum[i][j] for j in range(RESOURCES_TYPES)):
            print(f"You can't allocate more than maximum")
            alloc_for_process = input('Input allocation resources for types 1,2,3 respectively: ')
            alloc_for_process = [int(i) for i in alloc_for_process]

        allocation.append(alloc_for_process)


def need_initialization() -> None:
    global need
    for i in range(PROCESSES):
        for j in range(RESOURCES_TYPES):
            need[i][j] = maximum[i][j] - allocation[i][j]


def start_point_init() -> None:
    print('*' * 96)
    print('\t\tWARNING: type without any comas, white spaces, etc...')
    print('Example: 123')
    print('*' * 96)
    available_input()
    print()
    max_input()
    print()
    allocation_input()
    print()
    need_initialization()


def start_menu() -> None:
    print('*' * 32)
    print('\tBanker Algorithm')
    print('*' * 32)
    print('\nName: Valikhan Aiguzhin')
    print('ID: 228MLG71')
    print('You have 5 processes and 3 types of resources by given conditions\n')

    input('Press any key to continue:...')
    os.system('cls')


def main_menu() -> int:
    print('*' * 32)
    print('\tBanker Algorithm')
    print('*' * 32)

    print('Press 1 - Make a request')
    print('Press 2 - Set system start_point')
    print('Press 0 - Exit')

    result = int(input('Select the operation: '))
    return result


start_menu()
while True:
    choice = main_menu()

    if choice == 1:
        os.system('cls')
        if not allocation or not maximum or not available:
            print('First you need to set a system')
        else:
            inquire = input('Type requests for resources of types 1,2,3 respectively: ')
            inquire = [int(i) for i in inquire]
            proc_num = int(input('Enter № of process: '))
            resource_request(inquire, proc_num)

    elif choice == 2:
        if available or maximum or allocation:
            available.clear()
            maximum.clear()
            allocation.clear()
            need.clear()

        os.system('cls')
        start_point_init()
        test = safety()
        while not test:
            print('System is not safe. We should start again in few seconds...')
            time.sleep(3)
            os.system('cls')
            start_point_init()

        print('Request is satisfiable. Safe sequence is:')
        for i in test:
            print(f'P{i}', end=' ')
        print()

    elif choice == 0:
        break
