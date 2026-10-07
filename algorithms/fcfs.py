def run_fcfs(processes):
    """
    First-Come, First-Served (FCFS) Non-Preemptive Scheduling Algorithm.
    
    processes: List of dicts, each containing:
               {'pid': str, 'arrival': int, 'burst': int, 'priority': int}
               
    Returns:
      gantt_chart: List of tuples (pid, start_time, end_time)
      process_metrics: List of dicts with CT, TAT, WT included.
    """
    if not processes:
        return [], []

    # Sort processes primarily by Arrival Time, then deterministically by Process ID
    sorted_procs = sorted(processes, key=lambda x: (x['arrival'], str(x['pid'])))
    
    gantt_chart = []
    process_metrics = {}
    current_time = 0

    for proc in sorted_procs:
        pid = proc['pid']
        arrival = proc['arrival']
        burst = proc['burst']
        priority = proc['priority']

        # Handle CPU Idle Time
        if current_time < arrival:
            gantt_chart.append(('IDLE', current_time, arrival))
            current_time = arrival

        start_time = current_time
        end_time = start_time + burst
        current_time = end_time

        gantt_chart.append((pid, start_time, end_time))

        process_metrics[pid] = {
            'pid': pid,
            'arrival': arrival,
            'burst': burst,
            'priority': priority,
            'completion': end_time
        }

    return gantt_chart, list(process_metrics.values())