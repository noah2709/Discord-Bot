python my_bot/main.py

while [ $? -eq 104] || [ $? -eq 108 ]; do
    if [$? -eq 104]; then
        python my_bot/main.py
    elif [$? -eq 108]; then
        git pull
        python my_bot/main.py
    fi
done