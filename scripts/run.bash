python my_bot/main.py

EXIT_CODE=$?

while [ $EXIT_CODE -eq 104 ] || [ $EXIT_CODE -eq 108 ]; do
    if [ $EXIT_CODE -eq 104 ]; then
        python my_bot/main.py
        EXIT_CODE=$?
    elif [ $EXIT_CODE -eq 108 ]; then
        git pull
        python my_bot/main.py
        EXIT_CODE=$?
    fi
done
