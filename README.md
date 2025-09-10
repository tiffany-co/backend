- how can I run the program locally (after running DBs)?
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

- creating admin user:
    ```bash
    poetry run python app/scripts/create_admin.py
    ```

- in windows we can use this commands to unreserve port range (**run as administrator**):
    ```bash
    net stop winnat
    netsh int ipv4 delete excludedportrange protocol=tcp startport=5341 numberofports=100
    net start winnat
    ```

- database migration after all modifications:
    ```bash
    make db-migrate
    make db-upgrade
    ```