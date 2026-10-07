from collections import deque

def run_round_robin(processes, quantum):
    """
    Round Robin Preemptive Scheduling Algorithm.
    Handles exact arrival timings, idle periods, preemptions, and ready queue ordering.
    """
    if not processes or quantum <= 0:
        return [], []

    # Sort initial procs by arrival time
    unarrived = sorted([dict(p) for p in processes], key=lambda x: (x['arrival'], str(x['pid'])))
    for p in unarrived:
        p['remaining'] = p['burst']

    ready_queue = deque()
    gantt_chart = []
    completed = []
    current_time = 0
    
    # Fast access map for completion metrics
    proc_map = {p['pid']: dict(p) for p in processes}

    # Helper to load arriving processes up to target time
    def load_arrived_processes(until_time, exclude_pid=None):
        nonlocal unarrived
        to_add = []
        for p in unarrived:
            if p['arrival'] <= until_time:
                to_add.append(p)
        for p in to_add:
            ready_queue.append(p)
            unarrived.remove(p)

    # Initial loading at current_time
    load_arrived_processes(current_time)

    while ready_queue or unarrived:
        if not ready_queue:
            # Handle Idle period
            next_arrival = unarrived[0]['arrival']
            gantt_chart.append(('IDLE', current_time, next_arrival))
            current_time = next_arrival
            load_arrived_processes(current_time)
            continue

        curr = ready_queue.popleft()
        exec_time = min(curr['remaining'], quantum)
        start_time = current_time
        end_time = start_time + exec_time

        gantt_chart.append((curr['pid'], start_time, end_time))
        curr['remaining'] -= exec_time
        current_time = end_time

        # Load any new processes that arrived during this execution window
        load_arrived_processes(current_time)

        if curr['remaining'] > 0:
            # Re-enqueue preempted process after newly arrived ones
            ready_queue.append(curr)
        else:
            # Process finished
            proc_map[curr['pid']]['completion'] = current_time
            completed.append(proc_map[curr['pid']])

    return gantt_chart, list(proc_map.values())