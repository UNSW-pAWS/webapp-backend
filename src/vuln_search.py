import requests

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from package_detail_retrieval import package_detail_retrieval 

#The terms vulnerability and CVE are used interchangeably throughout this document. CVE means Common Vulnerability Enumeration

#The terms product and CPE are used interchangeably throughout this document.
#CPE means Common Platform Enumeration, version 2.3, a standard for identifying and searching products. Need to include vulnerability cpes/1.0?addOns=cves

def package_list_data(package_dic, severity=None, date=None):
    all_data = {}
    for x in package_dic.keys():
        all_data[x] = extract_relevant_data(x, severity, date)
    return all_data

def extract_relevant_data(search_word, severity=None, date=None):
    
    search_word = search_word.replace("-", "+")
    if date is None: 
        endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0?keyword=" + f'{search_word}'
    else: 
        endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0?modStartDate=" + f'{date}' + "T00:00:00:000 UTC-05:00&keyword=" + f'{search_word}'
    cve_response = requests.get(endpoint, verify=False)
    cve_result = cve_response.json()

    if cve_result['totalResults'] == 0:
        return []
    cve_result = cve_result['result']['CVE_Items']
    result_list = []
    for x in cve_result:
        dic = {'cve_id': x['cve']['CVE_data_meta']['ID'],
               'reference_links': [y['url'] for y in x['cve']['references']['reference_data']],
               'description': [y['value'] for y in x['cve']['description']['description_data']],
               'cve_data_version': x['configurations']['CVE_data_version'],
               'published_date': x['publishedDate'],
               'last_modified_date': x['lastModifiedDate']}
        if 'baseMetricV3' in x['impact']:
            dic['base_score'] = x['impact']['baseMetricV3']['cvssV3']['baseScore']
            dic['base_severity'] = x['impact']['baseMetricV3']['cvssV3']['baseSeverity']
            dic['exploitability_score'] = x['impact']['baseMetricV3']['exploitabilityScore']
            dic['impact_score'] =  x['impact']['baseMetricV3']['impactScore']
        elif 'baseMetricV2' in x['impact']:
            dic['base_score'] = x['impact']['baseMetricV2']['cvssV2']['baseScore']
            # dic['base_severity'] = x['impact']['baseMetricV2']['cvssV2']['baseSeverity']
            dic['exploitability_score'] = x['impact']['baseMetricV2']['exploitabilityScore']
            dic['impact_score'] = x['impact']['baseMetricV2']['impactScore']

        if severity is None or dic.get("base_severity") in severity: 
            result_list.append(dic)

    return result_list

# test = extract_relevant_data("react", ["CRITICAL"], "2021-01-01")
# print(test)
# print("hi")


root_packages = {"react", "node"}
my_output = {"react" : ["react-dependency1", "react-dependency2"], "node": ["node-dependency2"], 
                "react-dependency1": [] , "react-dependency2": [] , "node-dependency2": [] }
your_output ={"react": {}, "node": {"node vulnerbilities": "bef"}, "react-dependency1": {"react1 vulnerbilities" : "bjef"}, "react-dependency2": {"react2 vulnerbilities" : "ibnief"}, "node-dependency2" : {}}

def new_function(root_package, my_output, your_output):
    resulting_dic = {}
    for i in root_package:
        resulting_dic[i] = [{},your_output[i]]
        dependencies = my_output[i]
        for dependency in dependencies:
            resulting_dic[i][0].update(new_function({dependency}, my_output, your_output))
    return resulting_dic

# print(new_function(root_packages, my_output, your_output))

# print(package_detail_retrieval("npm", ["react", "node"], level=1))

package_list = ["react", "node"]
package_ouput = {'react': ['loose-envify', 'object-assign'], 'node': ['node-bin-setup'], 'loose-envify': ['js-tokens'], 'object-assign': [], 'node-bin-setup': []}

print(package_list_data(package_ouput, ["CRITICAL"], "2021-01-01"))