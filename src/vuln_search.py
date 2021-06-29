import requests

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#The terms vulnerability and CVE are used interchangeably throughout this document. CVE means Common Vulnerability Enumeration

#The terms product and CPE are used interchangeably throughout this document.
#CPE means Common Platform Enumeration, version 2.3, a standard for identifying and searching products. Need to include vulnerability cpes/1.0?addOns=cves

def package_list_data(package_dic):
    all_data = {}
    for x in package_dic.keys():
        all_data[x] = extract_relevant_data(x)
    return all_data

def extract_relevant_data(search_word):
    search_word = search_word.replace("-", "+")
    endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0?keyword=" + f'{search_word}'
    cve_response = requests.get(endpoint, verify=False)
    cve_result = cve_response.json()

    if cve_result['totalResults'] == 0:
        return []
    cve_result = cve_result['result']['CVE_Items']
    result_list = []
    for x in cve_result:
        dic = {'cve_id': x['cve']['CVE_data_meta']['ID'],
               ''
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

        # not sure about versionEndExcluding - might be multiple
        result_list.append(dic)

    return result_list


#replace - with + (e.g. prop+types)






