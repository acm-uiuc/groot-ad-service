# groot-ad-service
A service that triggers a script that adds members to the ACM Active Directory group once they have paid membership fees.
## Install / Setup
1. Clone repo:

    ```
    git clone https://github.com/acm-uiuc/groot-ad-service
    cd groot-ad-service
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Copy secrets template and add secrets:

    ```
    cp secrets.template.py secrets.py
    ```

## Run Application
```
python groot-ad-service/app.py
```

## Routes
Requires an Authorization Token passed in through an `Authorization` header, which is set in `secrets.py`

`GET /activedirectory/add/:netid`

Adds the member with the provided netid to the ACM Active Directory group 

## Contributing

Contributions to `groot-ad-service` are welcomed!

1. Fork the repo.
2. Create a new feature branch.
3. Add your feature / make your changes.
4. Install [pep8](https://pypi.python.org/pypi/pep8) and run `pep8 *.py` in the root project directory to lint your changes. Fix any linting errors.
5. Create a PR.
6. ???
7. Profit.
