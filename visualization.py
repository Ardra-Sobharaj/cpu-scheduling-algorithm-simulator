import matplotlib.pyplot as plt

def render_gantt_chart(gantt_data, figure):
    """
    Renders an embedded Matplotlib Gantt Chart into the provided figure.
    Theme: Modern Black & Beige palette matching the GUI dashboard.
    """
    figure.clear()
    if not gantt_data:
        figure.canvas.draw()
        return

    ax = figure.add_subplot(111)
    
    # Modern Black & Beige Styling
    bg_color = "#1E1E1E"
    card_bg = "#2D2D2D"
    text_color = "#F5F5DC"  # Beige
    accent_colors = ["#D4AF37", "#C5A059", "#E6C687", "#9A7B38", "#B8860B"]
    idle_color = "#3A3A3A"

    figure.patch.set_facecolor(bg_color)
    ax.set_facecolor(card_bg)

    # Distinct processes setup
    unique_pids = sorted(list({item[0] for item in gantt_data if item[0] != 'IDLE'}))
    color_map = {pid: accent_colors[i % len(accent_colors)] for i, pid in enumerate(unique_pids)}
    color_map['IDLE'] = idle_color

    # Merge contiguous identical blocks for clean rendering
    merged_gantt = []
    for item in gantt_data:
        if merged_gantt and merged_gantt[-1][0] == item[0] and merged_gantt[-1][2] == item[1]:
            merged_gantt[-1] = (merged_gantt[-1][0], merged_gantt[-1][1], item[2])
        else:
            merged_gantt.append(item)

    y_pos = 10
    height = 5

    ticks = [0]
    for pid, start, end in merged_gantt:
        duration = end - start
        c = color_map.get(pid, accent_colors[0])
        edge_c = "#F5F5DC" if pid != 'IDLE' else "#666666"

        ax.broken_barh([(start, duration)], (y_pos, height), facecolors=c, edgecolors=edge_c, linewidth=1.2)
        
        # Center Label inside bar
        mid_point = start + (duration / 2)
        label_text = pid if pid == 'IDLE' else f"P:{pid}"
        text_c = "#000000" if pid != 'IDLE' else "#AAAAAA"
        
        if duration > 0.3:  # Only print text if bar is wide enough
            ax.text(mid_point, y_pos + (height / 2), label_text, color=text_c,
                    ha='center', va='center', fontweight='bold', fontsize=9)
            
        ticks.append(end)

    # Customize Axes and Labels
    ax.set_ylim(0, 25)
    ax.set_yticks([])
    
    unique_ticks = sorted(list(set(ticks)))
    ax.set_xticks(unique_ticks)
    ax.set_xticklabels([str(x) for x in unique_ticks], color=text_color, fontsize=9)
    
    ax.set_xlabel("Time Units", color=text_color, fontweight='bold', labelpad=10)
    ax.set_title("Execution Timeline (Gantt Chart)", color=text_color, fontsize=12, fontweight='bold', pad=12)

    # Spines styling
    for spine in ax.spines.values():
        spine.set_color('#555555')
        
    ax.tick_params(axis='x', colors=text_color)
    ax.grid(True, axis='x', color='#444444', linestyle='--', alpha=0.5)

    figure.tight_layout()
    figure.canvas.draw()