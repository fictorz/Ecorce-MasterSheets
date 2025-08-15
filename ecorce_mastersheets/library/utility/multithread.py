import threading
import queue

def run_function_in_thread(func, args, kwargs, output_queue, index):
    """Runs a function in a separate thread and puts the result in a queue."""
    try:
        result = func(*args, **kwargs)
        output_queue.put((index, result))
    except Exception as e:
        output_queue.put((index, f"Error in function {func.__name__}: {e}")) # include function name

def run_functions_in_threads(functions, args_list=None, kwargs_list=None):
    """Runs multiple functions in threads and returns combined results."""

    num_functions = len(functions)

    if args_list is None:
        args_list = [()] * num_functions  # Default to empty tuples
    elif len(args_list) != num_functions:
        raise ValueError("args_list must have the same length as functions")

    if kwargs_list is None:
        kwargs_list = [{}] * num_functions  # Default to empty dictionaries
    elif len(kwargs_list) != num_functions:
        raise ValueError("kwargs_list must have the same length as functions")

    threads = []
    output_queue = queue.Queue()
    results = [None] * num_functions

    for i, func in enumerate(functions):
        thread = threading.Thread(target=run_function_in_thread, args=(func, args_list[i], kwargs_list[i], output_queue, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not output_queue.empty():
        index, result = output_queue.get()
        results[index] = result

    return results
