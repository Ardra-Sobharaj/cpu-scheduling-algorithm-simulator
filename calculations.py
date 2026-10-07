def compute_metrics(process_list):
    """
    Calculates Completion Time (CT), Turnaround Time (TAT), Waiting Time (WT),
    and overall averages.
    
    Formulae:
    TAT = CT - Arrival Time
    WT = TAT - Burst Time
    """
    if not process_list:
        return [], 0.0, 0.0

    detailed_results = []
    total_tat = 0
    total_wt = 0

    for proc in process_list:
        ct = proc['completion']
        arrival = proc['arrival']
        burst = proc['burst']
        
        tat = ct - arrival
        wt = tat - burst

        total_tat += tat
        total_wt += wt

        detailed_results.append({
            'pid': proc['pid'],
            'arrival': arrival,
            'burst': burst,
            'priority': proc['priority'],
            'completion': ct,
            'tat': tat,
            'wt': wt
        })

    # Sort results by Process ID for clean presentation
    detailed_results.sort(key=lambda x: str(x['pid']))
    n = len(detailed_results)
    avg_wt = total_wt / n if n > 0 else 0.0
    avg_tat = total_tat / n if n > 0 else 0.0

    return detailed_results, round(avg_wt, 2), round(avg_tat, 2)