def run_priority(processes):
    """
    Non-Preemptive Priority Scheduling Algorithm.
    Lower priority number = Higher Priority.
    Deterministic Tie-Breaking: Priority -> Arrival Time -> Process ID.
    """
    if not processes:
        return [], []

    unarrived = [dict(p) for p in processes]
    completed = []
    gantt_chart = []
    current_time = 0

    while unarrived or len(completed) < len(processes):
        ready_queue = [p for p in unarrived if p['arrival'] <= current_time]

        if not ready_queue:
            next_arrival = min(p['arrival'] for p in unarrived)
            gantt_chart.append(('IDLE', current_time, next_arrival))
            current_time = next_arrival
            continue

        # Select process with highest priority (lowest numerical value)
        selected = min(ready_queue, key=lambda x: (x['priority'], x['arrival'], str(x['pid'])))

        start_time = current_time
        end_time = start_time + selected['burst']
        current_time = end_time

        gantt_chart.append((selected['pid'], start_time, end_time))

        selected['completion'] = end_time
        completed.append(selected)
        unarrived.remove(selected)

    return gantt_chart, completed