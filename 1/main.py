import subprocess
import time
import os

def run_test(program_path, arguments, expected_result, test_number):
    try:
        start_time = time.time()
        process = subprocess.run(
            ["python", program_path],
            input=arguments,
            text=True,
            capture_output=True,
            timeout=1
        )
        end_time = time.time()

        prog_time = round(end_time - start_time, 3)
        if process.returncode != 0:
            return f"Test #{test_number}: Runtime Error ({prog_time}s)"

        output = process.stdout.strip()
        if output == expected_result:
            return f"Test #{test_number}: Accepted ({prog_time}s)"
        else:
            return f"Test #{test_number}: Wrong Answer ({prog_time}s)"

    except subprocess.TimeoutExpired:
        return f"Test #{test_number}: Time Limit Exceeded (1.000s)"
    except Exception as e:
        return f"Test #{test_number}: Runtime Error (0.000s)"

def main():
    tests_file_path = input("Enter the path to the tests file: ").strip()
    if not os.path.isfile(tests_file_path):
        print("The test file does not exist or is not a file.")
        return
    with open(tests_file_path, "r") as file:
        lines = file.readlines()
    results = []

    for test_number, line in enumerate(lines, start=1):
        try:
            program_path, arguments, expected_result = line.strip().split(" ")
            arguments = arguments.strip("()")
            expected_result = expected_result.strip("()")
        except ValueError:
            results.append(f"Test #{test_number}: Invalid Test Format (0.000s)")
            continue

        if not os.path.isfile(program_path):
            results.append(f"Test #{test_number}: Program Not Found (0.000s)")
            continue

        if not program_path.endswith('.py'):
            results.append(f"Test #{test_number}: Invalid File Type (Not a .py) (0.000s)")
            continue

        result = run_test(program_path, arguments, expected_result, test_number)
        results.append(result)

    for result in results:
        print(result)

if __name__ == "__main__":
    main()

