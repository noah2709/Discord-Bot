python my_bot/main.py

while [ $? -eq 104 || $? -eq 187 ]; do
    if [$? -eq 104]; then
        python my_bot/main.py
    elif [$? -eq 187]; then
        git pull
        python my_bot/main.py
    fi
done