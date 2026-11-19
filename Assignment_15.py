"""
Experiment 15: Manual Garbage Collection using the gc module
Analyze Python's garbage collection and its impact on memory and performance.
"""

import gc
import time
import tracemalloc


class Node:
    """Object that can form a reference cycle."""
    def __init__(self):
        self.ref = None


def create_cycle():
    a, b = Node(), Node()
    a.ref = b
    b.ref = a          # reference cycle: a <-> b


def create_dict_cycles(count=10):
    for i in range(count):
        x = {}
        x[i + 1] = x   # dictionary refers to itself
        print(x)


def current_memory():
    current, _ = tracemalloc.get_traced_memory()
    return current / 1024


def show_status():
    print("GC enabled         :", gc.isenabled())
    print("GC thresholds      :", gc.get_threshold())
    print("Objects per generation (count):", gc.get_count())


def dict_cycle_demo():
    gc.disable()
    gc.collect()
    print("Creating cycles...")
    create_dict_cycles(10)
    collected = gc.collect()
    print(f"Garbage collector: collected {collected} objects.")
    gc.enable()


def memory_demo():
    tracemalloc.start()
    gc.disable()
    gc.collect()
    print(f"Initial memory usage          : {current_memory():.1f} KB")

    for _ in range(20000):
        create_cycle()
    print(f"After creating 20000 cycles   : {current_memory():.1f} KB")

    print("\nEnabling garbage collection debugging (stats go to stderr)...")
    gc.set_debug(gc.DEBUG_STATS)
    collected = gc.collect()
    gc.set_debug(0)
    #Om Kutwal Sy-12 Roll no. 70
    print(f"Garbage collector: collected {collected} objects.")
    print(f"After manual collection       : {current_memory():.1f} KB")
    gc.enable()
    tracemalloc.stop()


def forced_collection_demo():
    obj1 = [1, 2, 3]
    obj2 = {"a": 1, "b": 2}
    obj3 = "Hello, world!"
    print("Created obj1 (list), obj2 (dict), obj3 (string).")
    del obj1, obj2, obj3
    print("References deleted. Forcing garbage collection...")
    print(f"Garbage collector: collected {gc.collect()} objects.")


def toggle_gc():
    if gc.isenabled():
        gc.disable()
        print("Garbage collector DISABLED.")
    else:
        gc.enable()
        print("Garbage collector ENABLED.")


def set_thresholds():
    try:
        g0 = int(input("Enter threshold for generation 0: ").strip())
        g1 = int(input("Enter threshold for generation 1: ").strip())
        g2 = int(input("Enter threshold for generation 2: ").strip())
    except ValueError:
        print("Invalid input. Please enter integers.")
        return
    gc.set_threshold(g0, g1, g2)
    print("Garbage collector thresholds set")
    print("Current thresholds:", gc.get_threshold())


def performance_demo():
    def work():
        for _ in range(100000):
            create_cycle()

    gc.enable()
    start = time.perf_counter()
    work()
    t_enabled = time.perf_counter() - start
    gc.collect()

    gc.disable()
    start = time.perf_counter()
    work()
    t_disabled = time.perf_counter() - start
    gc.collect()
    gc.enable()

    print(f"Time with GC enabled  : {t_enabled:.3f}s")
    print(f"Time with GC disabled : {t_disabled:.3f}s")


def print_menu():
    print("\n===== GARBAGE COLLECTION (gc module) =====")
    print("1. Show GC status and thresholds")
    print("2. Create reference cycles and collect manually")
    print("3. Memory usage before/after collection")
    print("4. Delete objects and force garbage collection")
    print("5. Enable / Disable garbage collector")
    print("6. Set GC thresholds")
    print("7. Performance: GC enabled vs disabled")
    print("8. Exit")
    print("==========================================")


def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            show_status()
        elif choice == "2":
            dict_cycle_demo()
        elif choice == "3":
            memory_demo()
        elif choice == "4":
            forced_collection_demo()
        elif choice == "5":
            toggle_gc()
        elif choice == "6":
            set_thresholds()
        elif choice == "7":
            performance_demo()
        elif choice == "8":
            print("Exiting the Garbage Collection Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
