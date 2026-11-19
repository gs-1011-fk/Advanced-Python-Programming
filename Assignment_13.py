"""
Experiment 13: Multithreading
Create multiple threads to perform different tasks concurrently.
"""

import logging
import threading
import time

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


# ---------------- Tasks ----------------
def count_numbers(n):
    for i in range(1, n + 1):
        print(f"[Count ] {i}")
        time.sleep(0.2)


def calculate_squares(n):
    for i in range(1, n + 1):
        print(f"[Square] {i}^2 = {i ** 2}")
        time.sleep(0.2)


def calculate_cubes(n):
    for i in range(1, n + 1):
        print(f"[Cube  ] {i}^3 = {i ** 3}")
        time.sleep(0.2)


def thread_function(name, delay=2):
    logging.info("Thread %s: starting", name)
    time.sleep(delay)
    logging.info("Thread %s: finishing", name)


# ---------------- Demos ----------------
def single_thread_demo():
    logging.info("Main : before creating thread")
    t = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main : before running thread")
    t.start()
    logging.info("Main : wait for the thread to finish")
    t.join()
    logging.info("Main : all done")


def multiple_tasks_demo(n):
    #Om Kutwal Sy-12 Roll no. 70
    t1 = threading.Thread(target=count_numbers, args=(n,))
    t2 = threading.Thread(target=calculate_squares, args=(n,))
    t3 = threading.Thread(target=calculate_cubes, args=(n,))

    start = time.perf_counter()
    for t in (t1, t2, t3):
        t.start()
    for t in (t1, t2, t3):
        t.join()
    print(f"\nAll tasks completed concurrently in {time.perf_counter() - start:.2f}s")


def many_threads_demo(count):
    threads = []
    for index in range(count):
        logging.info("Main : create and start thread %d.", index)
        t = threading.Thread(target=thread_function, args=(index, 1))
        threads.append(t)
        t.start()
    for index, t in enumerate(threads):
        logging.info("Main : before joining thread %d.", index)
        t.join()
        logging.info("Main : thread %d done", index)


def daemon_demo():
    t = threading.Thread(target=thread_function, args=("daemon", 3), daemon=True)
    t.start()
    time.sleep(1)
    print(f"Daemon flag: {t.daemon} | Still running: {t.is_alive()}")
    print("A daemon thread is killed automatically when the program exits.")
    print("(Choose Exit now and its 'finishing' message will never appear.)")


def sequential_vs_threaded():
    def task():
        time.sleep(1)

    start = time.perf_counter()
    for _ in range(3):
        task()
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    threads = [threading.Thread(target=task) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    thr_time = time.perf_counter() - start

    print(f"Sequential (3 tasks x 1s) : {seq_time:.2f}s")
    print(f"Threaded   (3 tasks x 1s) : {thr_time:.2f}s")


def race_condition_demo():
    counter = {"value": 0}
    lock = threading.Lock()

    def unsafe_increment(times):
        for _ in range(times):
            temp = counter["value"]
            time.sleep(0)            # lets another thread run in between
            counter["value"] = temp + 1

    def safe_increment(times):
        for _ in range(times):
            with lock:
                temp = counter["value"]
                time.sleep(0)
                counter["value"] = temp + 1

    for label, func in (("WITHOUT lock", unsafe_increment), ("WITH lock", safe_increment)):
        counter["value"] = 0
        threads = [threading.Thread(target=func, args=(1000,)) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"{label:<13}: expected 4000, got {counter['value']}")


def get_int(prompt, default):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print(f"Invalid input. Using default {default}.")
        return default


def print_menu():
    print("\n===== MULTITHREADING PROGRAM =====")
    print("1. Single thread demo (start and join)")
    print("2. Run count, square and cube tasks concurrently")
    print("3. Start many threads")
    print("4. Daemon thread demo")
    print("5. Sequential vs threaded time comparison")
    print("6. Race condition demo (with and without Lock)")
    print("7. Exit")
    print("==================================")


def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            single_thread_demo()
        elif choice == "2":
            multiple_tasks_demo(get_int("Enter how many numbers (n): ", 5))
        elif choice == "3":
            many_threads_demo(get_int("Enter number of threads: ", 3))
        elif choice == "4":
            daemon_demo()
        elif choice == "5":
            sequential_vs_threaded()
        elif choice == "6":
            race_condition_demo()
        elif choice == "7":
            print("Exiting the Multithreading Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
