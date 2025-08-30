- how can I run the program locally (after running DBs)?
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

- creating admin user:
    ```bash
    poetry run python app/scripts/create_admin.py
    ```