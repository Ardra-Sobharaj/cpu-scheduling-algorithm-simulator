def run_sjf(processes):
    """
    Non-Preemptive Shortest Job First (SJF) Scheduling Algorithm.
    Deterministic Tie-Breaking: Burst Time -> Arrival Time -> Process ID.
    """
    if not processes:
        return [], []

    # Make working copies
    unarrived = [dict(p) for p in processes]
    completed = []
    gantt_chart = []
    current_time = 0

    while unarrived or len(completed) < len(processes):
        # Filter processes that have arrived up to current_time
        ready_queue = [p for p in unarrived if p['arrival'] <= current_time]

        if not ready_queue:
            # CPU is idle until the next earliest process arrives
            next_arrival = min(p['arrival'] for p in unarrived)
            gantt_chart.append(('IDLE', current_time, next_arrival))
            current_time = next_arrival
            continue

        # Select process with shortest burst time
        # Tie-breakers: Burst Time -> Arrival Time -> Process ID
        selected = min(ready_queue, key=lambda x: (x['burst'], x['arrival'], str(x['pid'])))

        start_time = current_time
        end_time = start_time + selected['burst']
        current_time = end_time

        gantt_chart.append((selected['pid'], start_time, end_time))

        selected['completion'] = end_time
        completed.append(selected)
        unarrived.remove(selected)

    return gantt_chart, completed