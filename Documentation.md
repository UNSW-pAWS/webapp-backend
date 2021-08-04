ENDPOINTS

Enpoint | Method | Description | Parameters | Response
:------- | :------- | :----------------| :-------- | :---------
/threat/search | GET/POST | Returns vulnerabilities based on user's package list and dependencies | String: package manager type, <br /> List: user's packages, <br /> Date (optional): vulnerabilities after this date e.g. '2021-01-01', <br /> List (optional): vulnerabilities with given severity e.g. "CRITICAL"   | A nested dictionary with the user's packages as the keys, where the value of the keys are it's vulnerabilities and it's respective dependencies. 


