## Configuration files

This directory contains the static files for each supported resource. Each resource's files are located under its directory and should have the following files:

- ConfigOptions.json
    - File containing the options that will be displayed to the user on the frontend. More details [here](#configuration-options)
- CFNTemplate.json
    - Default CloudFormation template for the resource
- ConformancePack.yaml
    - Conformance pack containing the AWS Config rules which will be checked for the resource
- Rules.json
    - Description file for the rules which apply to this resource. More details [here](#rules-description)


---

### Configuration Options

The configuration file will be parsed by the frontend which will render the available fields to the user. 

<br/>

Each configuration option file should follow the structure:

```
    {
        <resource1-name>: {
            "properties": [
                {
                    <property1-config>
                },
                .
                .
                etc.
            ],
            "multiple": true/false,
            "required": true/false
        },
        .
        .
        etc.
    }
```
| Parameter | Description | Constraint |
| --------- | ----------- | ---------- |
| properties | List of properties to be provided to the frontend | Length should be at least 1 |
| multiple | Boolean to indicate whether the user should be able to add multiple of this resource | True/False
| required | Boolean to indicate if this resource is required | True/False |

<br/>

Each property configuration object should then follow the structure: 

```
    {
        "propertyId": <property-id>,
        "type": <type>,
        "default": <default-value>,
        "values": [
            <value1>
            .
            .
            etc.
        ],
        "pattern": <string-pattern-match>,
        "managedRules: [
            <rule1>,
            .
            .
            etc.
        ]
    }
```

| Parameter | Description | Constraints |
| --------- | ----------- | ----------- |
| propertyId | Property name | Should match the AWS property name format |
| type | Property type which should indicate to the frontend how it should be rendered | one of [boolean, free-text, dropdown, integer, json] |
| values | List of accepted values | Only required if type === dropdown |
| pattern | Regex pattern of the accepted values | Only required if type === free-text |
| managedRules | List of AWS Managed Rules that this property relates to (for user info) | - |

---

### Rules description

File outlining the AWS Managed Rules which will be applied to this resource. Primarily used as documentation and not used in the actual application. Structure as below:

```
    [
        "name": <rule-name>,
        "rule": <rule-description>
    ]
```

| Parameter | Description |
| --------- | ----------- |
| name | Name of the AWS Managed Rule |
| rule | Description of the rule - should be pseudocode to explain what properties should be considered when checking if the resource complies to this rule |