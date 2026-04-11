from time import sleep

class Colors:
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def visualize_tape(
    data_list,
    head_index,
    window_size=5,
    speed=0.7,
    tape_color=Colors.CYAN,
    head_color=Colors.YELLOW
):
    if not data_list:
        print(f"{Colors.YELLOW}The list is empty!{Colors.RESET}")
        return

    num_elements = len(data_list)
    normalized_head_index = head_index % num_elements
    if normalized_head_index < 0:
        normalized_head_index += num_elements

    visible_elements = []
    total_window_length = (2 * window_size) + 1

    for i in range(total_window_length):
        current_offset = i - window_size
        actual_data_index = (normalized_head_index + current_offset) % num_elements
        visible_elements.append(data_list[actual_data_index])
    
    local_head_index = window_size

    total_segment_width = len(visible_elements) * 5 + 1

    print(f"{tape_color}╭{'─' * total_segment_width}╮{Colors.RESET}")

    tape_line = f"{tape_color}│{Colors.RESET}"
    pointer_line = " "

    for i, item in enumerate(visible_elements):
        formatted_item = str(item).center(3)
        block_width = 5

        if i == local_head_index:
            tape_line += f"{head_color}{Colors.BOLD} {formatted_item} {Colors.RESET}{tape_color}"
            pointer_line += f"{' ' * ((block_width - 1) // 2)}{head_color}▲{Colors.RESET}{' ' * ((block_width - 1) // 2)}"
        else:
            tape_line += f" {formatted_item} {tape_color}"
            pointer_line += " " * block_width
            
    tape_line += f"│{Colors.RESET}"
    print(tape_line)

    print(f"{tape_color}╰{'─' * total_segment_width}╯{Colors.RESET}")
    print(pointer_line)

    print(f"{Colors.BOLD}{Colors.WHITE}----------------------------------------{Colors.RESET}")
    print(f"Current Head: {head_color}{Colors.BOLD}{data_list[normalized_head_index]}{Colors.RESET} at index {normalized_head_index}\n")
    sleep(speed)
