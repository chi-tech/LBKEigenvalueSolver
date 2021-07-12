import os
import sys
import subprocess
import textwrap

# To run a range of tests pass a text string via the command line.
# i.e., "tests_to_run=[*range(14,16)]"

# This python script executes the regression test suite.
# In order to add your own test, copy one of the test blocks
# and modify the logic to what you would like tested.

# General guidance: Do not write a regression test that checks
# for number of iterations. Rather make it check for answers
# since something as simple as a preconditioner can change
# iteration count but still produce the same answer

kscript_path = os.path.dirname(os.path.abspath(__file__))
kchi_src_path = os.path.join(kscript_path, '..')
kpath_to_exe = os.path.join(kchi_src_path, 'bin/LBKEigenvalueSolver')

tests_to_run = []
print_only = False

if len(sys.argv) >= 2:
    exec(sys.argv[1])

msg = "*" * 15
msg = msg + " LBKEigenvalueSolver Regression Test " + msg
print("\n" + msg + "\n")

test_number = 0
num_failed = 0

# Determine if we are on TACC or tamu cluster
# (each test will require a separate job)
hostname = subprocess.check_output(['hostname']).decode('utf-8')
tacc = False
tamu = False
if "tacc.utexas.edu" in hostname:
    tacc = True
elif "ne.tamu.edu" in hostname and "orchard" in hostname:
    tamu = True


# ================================================== Formatting routines
def format3(number):
    return "{:3d}".format(number)


def format_filename(filename):
    return "{:35s}".format(filename)


# ================================================== Parsing routines
def parse_output(out, search_strings_vals_tols):
    global num_failed
    test_passed = True
    for search in search_strings_vals_tols:
        find_str = search[0]
        true_val = search[1]
        tolerance = search[2]

        # start of the string to find (<0 if not found)
        test_str_start = out.find(find_str)
        # end of the string to find
        test_str_end = test_str_start + len(find_str)
        # end of the line at which string was found
        test_str_line_end = out.find("\n", test_str_start)

        test_passed = True
        if test_str_start >= 0:
            # convert value to number
            test_val = float(out[test_str_end:test_str_line_end])
            if not abs(test_val - true_val) < tolerance:
                test_passed = False
        else:
            test_passed = False

    if test_passed:
        print(" - Passed")
    else:
        print(" - FAILED!")
        num_failed += 1
        print(out)

    return test_passed


# ================================================== Run routines
def run_test_tacc(file_name, comment, num_procs,
                  search_strings_vals_tols):
    # Define test name
    test_name = " ".join([format_filename(file_name), comment,
                         str(num_procs), "MPI Processes"])

    # Print test info
    printout = " ".join(["Running Test", format3(test_number), test_name])
    print(printout, end='', flush=True)

    # Print job info without running
    if print_only:
        print("")
        return

    # Run the job
    with open(f"Test/{file_name}.job", 'w') as job_file:
        job_file.write(textwrap.dedent(f"""
            #!/usr/bin/bash
            #
            #SBATCH -J {file_name} # Job name
            #SBATCH -o Test/{file_name}.o # output file
            #SBATCH -e Test/{file_name}.e # error file
            #SBATCH -p skx-normal # Queue (partition) name
            #SBATCH -N {num_procs // 48 + 1} # Total # of nodes
            #SBATCH -n {num_procs} # Total # of mpi tasks
            #SBATCH -t 00:05:00 # Runtime (hh:mm:ss)
            #SBATCH -A Massively-Parallel-R # Allocation name (req'd if you have more than 1)

            export I_MPI_SHM=disable

            ibrun {kpath_to_exe} Test/{file_name}.lua master_export=false
            """).strip())

    # -W means wait for job to finish
    os.system(f"sbatch -W Test/{file_name}.job > /dev/null")
    with open(f"ChiTest/{file_name}.o", 'r') as outfile:
        out = outfile.read()

    # Parse results to check for passing result
    passed = parse_output(out, search_strings_vals_tols)

    # Cleanup
    if passed:
        os.system(f"rm Test/{file_name}.job "
                  f"Test/{file_name}.o "
                  f"Test/{file_name}.e")


def run_test_tamu(file_name, comment, num_procs,
                  search_strings_vals_tols):
    # Define test name
    test_name = " ".join([format_filename(file_name), comment,
                          str(num_procs), "MPI Processes"])

    # Print test info
    printout = " ".join(["Running Test", format3(test_number), test_name])
    print(printout, end='', flush=True)

    # Print job info without running
    if print_only:
        print("")
        return

    # Run the job
    with open(f"Test/{file_name}.job", 'w') as job_file:
        job_file.write(textwrap.dedent(f"""
            #!/usr/bin/bash
            #
            #SBATCH -J {file_name} # Job name
            #SBATCH -o Test/{file_name}.o # output file
            #SBATCH -e Test/{file_name}.e # error file
            #SBATCH -p class # Queue (partition) name
            #SBATCH -N {num_procs // 48 + 1} # Total # of nodes
            #SBATCH -n {num_procs} # Total # of mpi tasks
            #SBATCH -t 00:05:00 # Runtime (hh:mm:ss)
            #SBATCH -A class # Allocation name (req'd if you have more than 1)

            mpiexec -n {num_procs} {kpath_to_exe} Test/{file_name}.lua master_export=false
            """).strip())

    # -W means wait for job to finish
    os.system(f"sbatch -W Test/{file_name}.job > /dev/null")
    with open(f"ChiTest/{file_name}.o", 'r') as outfile:
        out = outfile.read()

    # Parse results to check for passing result
    passed = parse_output(out, search_strings_vals_tols)

    # Cleanup
    if passed:
        os.system(f"rm Test/{file_name}.job "
                  f"Test/{file_name}.o "
                  f"Test/{file_name}.e")


def run_test_local(file_name, comment, num_procs,
                   search_strings_vals_tols):
    # Define test name
    test_name = " ".join([format_filename(file_name), comment,
                          str(num_procs), "MPI Processes"])

    # Print test info
    printout = " ".join(["Running Test", format3(test_number), test_name])
    print(printout, end='', flush=True)

    # Print job info without running
    if print_only:
        print("")
        return

    # Run the job
    run_file = os.path.join("Test", file_name + ".lua")
    cmd = ["mpiexec", "-np", str(num_procs), kpath_to_exe,
           run_file, "master_export=false"]
    process = subprocess.Popen(cmd, cwd=kchi_src_path,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    process.wait()
    out, err = process.communicate()

    # Parse results to check for passing result
    parse_output(out, search_strings_vals_tols)


def run_test(file_name, comment, num_procs,
             search_strings_vals_tols):
    global test_number
    test_number += 1

    if (tests_to_run and test_number in tests_to_run) or \
            not tests_to_run:
        if tacc:
            run_test_tacc(file_name, comment, num_procs,
                          search_strings_vals_tols)
        elif tamu:
            run_test_tamu(file_name, comment, num_procs,
                          search_strings_vals_tols)
        else:
            run_test_local(file_name, comment, num_procs,
                           search_strings_vals_tols)


# ================================================== Run tests
run_test(
    file_name="KEigenvalueTransport1D_1G",
    comment="1D KSolver LinearBSolver Test - PWLD",
    num_procs=4,
    search_strings_vals_tols=[["[0]          Final k-eigenvalue    :", 0.99954, 1.0e-5]])

# ================================================== End of tests
msg = "\n"
if num_failed == 0:
    msg += "All regression tests passed!"
else:
    msg += "ERROR: Not all regression tests passed!"
    msg += f"\nNumber of tests failed = {num_failed}"
msg += "\n************* End of Regression Test *************\n"
print(msg)
if num_failed == 0:
    sys.exit(0)
else:
    sys.exit(1)

