# py -3 my_bot\main.py

do {
    py -3 my_bot\main.py
} while ($LastExitCode -eq 104)

exit $LastExitCode