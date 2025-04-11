def apply_simplifier(base_prompt, eli5_mode):
    if eli5_mode:
        return base_prompt + "\nExplain everything in a simple, beginner-friendly way."
    return base_prompt
