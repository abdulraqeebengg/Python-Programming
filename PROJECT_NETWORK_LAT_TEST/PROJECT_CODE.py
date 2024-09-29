import time
import random
import unittest
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class LatencyTestRecord:
    def __init__(self, source, latency, test_time=None):
        """
        Initializes a latency test record with provided details.
        :param source: The source location for the latency test.
        :param latency: The measured latency for the source.
        :param test_time: Optional time the test was performed.
        """
        self.source = source
        self.latency = latency
        self.test_time = test_time if test_time else datetime.now()

    def __str__(self):
        return f"{Fore.CYAN}Latency for {Fore.YELLOW}{self.source}{Fore.CYAN}: {Fore.GREEN}{self.latency}ms{Fore.CYAN}, tested at {Fore.MAGENTA}{self.test_time}{Style.RESET_ALL}"


class DataStorage:
    """ Class for handling storage of latency test records. """

    def __init__(self):
        self.records = []

    def add_record(self, record):
        """Adds a latency record to the storage."""
        self.records.append(record)

    def get_record(self, idx):
        """Retrieves a latency record by its index."""
        return self.records[idx] if 0 <= idx < len(self.records) else f"{Fore.RED}Record not found{Style.RESET_ALL}"

    def modify_record(self, idx, new_record):
        """Modifies a specific latency record at the given index."""
        if 0 <= idx < len(self.records):
            self.records[idx] = new_record
            return True
        return False

    def remove_record(self, idx):
        """Removes a latency record at the given index."""
        if 0 <= idx < len(self.records):
            self.records.pop(idx)
            return True
        return False

    def display_all(self):
        """Displays all latency records."""
        if not self.records:
            print(f"{Fore.RED}No records available.{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Displaying all records:{Style.RESET_ALL}")
            for idx, record in enumerate(self.records):
                print(f"{Fore.CYAN}[{idx}] {record}")


def run_latency_simulation(source):
    """
    Simulates latency for a given source location.
    :param source: The source location for the latency test.
    :return: Simulated latency in milliseconds.
    """
    latency = random.randint(1, 100)  # Random simulated latency in ms
    print(f"{Fore.YELLOW}Simulating latency for {source}...{Style.RESET_ALL}")
    time.sleep(1)  # Simulate a delay
    print(f"{Fore.GREEN}Simulated latency: {latency} ms for {source}{Style.RESET_ALL}")
    return LatencyTestRecord(source, latency)


class LatencyTestCase(unittest.TestCase):
    def setUp(self):
        self.storage = DataStorage()

    def test_add_and_get_record(self):
        test_record = run_latency_simulation("New York")
        self.storage.add_record(test_record)
        self.assertEqual(self.storage.get_record(0), test_record, "Error in adding and retrieving record")

    def test_modify_record(self):
        self.storage.add_record(run_latency_simulation("New York"))
        modified_record = LatencyTestRecord("New York", 75)
        self.assertTrue(self.storage.modify_record(0, modified_record))
        self.assertEqual(self.storage.get_record(0), modified_record, "Error in modifying the record")

    def test_remove_record(self):
        self.storage.add_record(run_latency_simulation("New York"))
        self.assertTrue(self.storage.remove_record(0))
        self.assertEqual(self.storage.get_record(0), "Record not found", "Error in deleting the record")


def print_stylish_header():
    """Prints a stylish header with ASCII art."""
    print(f"{Fore.CYAN}========================================")
    print(f"        {Fore.YELLOW}⚡ Network Latency Tester ⚡")
    print(f"{Fore.CYAN}========================================{Style.RESET_ALL}")


def main_menu():
    """Displays the main menu and handles user interaction."""
    storage = DataStorage()

    while True:
        print_stylish_header()
        print(f"{Fore.GREEN}1. {Fore.CYAN}Add new latency record")
        print(f"{Fore.GREEN}2. {Fore.CYAN}Measure latency")
        print(f"{Fore.GREEN}3. {Fore.CYAN}Update latency record")
        print(f"{Fore.GREEN}4. {Fore.CYAN}Delete latency record")
        print(f"{Fore.GREEN}5. {Fore.CYAN}Show all records")
        print(f"{Fore.GREEN}6. {Fore.CYAN}Quit")
        print(f"{Fore.CYAN}========================================{Style.RESET_ALL}")

        choice = input(f"{Fore.YELLOW}Choose an option (1-6): {Style.RESET_ALL}")

        if choice == '1':
            source = input(f"{Fore.CYAN}Enter the source location: {Style.RESET_ALL}")
            test_record = run_latency_simulation(source)
            storage.add_record(test_record)
            print(f"\n{Fore.GREEN}Record added: {test_record}{Style.RESET_ALL}")

        elif choice == '2':
            source = input(f"{Fore.CYAN}Enter the source location: {Style.RESET_ALL}")
            test_record = run_latency_simulation(source)
            print(f"\n{Fore.GREEN}Latency measured: {test_record}{Style.RESET_ALL}")

        elif choice == '3':
            if not storage.records:
                print(f"{Fore.RED}No records to update. Add a record first.{Style.RESET_ALL}")
                continue

            try:
                idx = int(input(f"{Fore.CYAN}Enter the index of the record to update: {Style.RESET_ALL}"))
                source = input(f"{Fore.CYAN}Enter the source location: {Style.RESET_ALL}")
                latency = int(input(f"{Fore.CYAN}Enter the new latency (ms): {Style.RESET_ALL}"))
                new_record = LatencyTestRecord(source, latency)
                if storage.modify_record(idx, new_record):
                    print(f"{Fore.GREEN}Record at index {idx} updated successfully.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: Invalid index.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Error: Invalid input. Please enter numeric values for index and latency.{Style.RESET_ALL}")

        elif choice == '4':
            if not storage.records:
                print(f"{Fore.RED}No records to delete. Add a record first.{Style.RESET_ALL}")
                continue

            try:
                idx = int(input(f"{Fore.CYAN}Enter the index of the record to delete: {Style.RESET_ALL}"))
                if storage.remove_record(idx):
                    print(f"{Fore.GREEN}Record at index {idx} deleted successfully.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: Invalid index.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Error: Invalid input. Please enter a numeric index.{Style.RESET_ALL}")

        elif choice == '5':
            print(f"\n{Fore.CYAN}Displaying all records:{Style.RESET_ALL}")
            storage.display_all()

        elif choice == '6':
            print(f"{Fore.CYAN}Exiting Network Latency Tester. Goodbye!{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}Invalid choice. Please choose an option between 1 and 6.{Style.RESET_ALL}")


if __name__ == '__main__':
    main_menu()
