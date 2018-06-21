import subprocess

commands = [
    ["python", "dynamic_cross_validation.py", "-fname", "exp2/fasttext.downsampled.dataset", "-folder", "exp2/", "-minn", "4", "-maxn", "4", "-dim", "150", "-epoch", "20", "-lr", "0.1", "-wordNgrams", "1", "-comment", ""]
]

errors = []

i = 0
for command in commands:
    try:
        print "Running command", i
        subprocess.call(command)
        i += 1
    except Exception, e:
        errors.append("Error running command " + str(i) + "; Exception: " + str(e))


print "Finished running"
print str(len(errors)) + " errors occurred"

for error in errors:
    print error