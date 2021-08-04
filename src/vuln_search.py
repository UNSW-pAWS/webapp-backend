import requests
import asyncio
import aiohttp
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from package_detail_retrieval import package_detail_retrieval 

#The terms vulnerability and CVE are used interchangeably throughout this document. CVE means Common Vulnerability Enumeration

#The terms product and CPE are used interchangeably throughout this document.
#CPE means Common Platform Enumeration, version 2.3, a standard for identifying and searching products. Need to include vulnerability cpes/1.0?addOns=cves

async def package_list_data(package_dic, severity="None", date="None"):
    all_data = {}
    if len(package_dic) == 0:
        return all_data
    work_queue = asyncio.Queue()
    for x in package_dic.keys():
        await work_queue.put(x)
    await asyncio.gather(asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)))
    return all_data

async def extract_relevant_data(work_queue, severity="None", date="None",all_data={}):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            original_word = await work_queue.get()
            if original_word == "": return []

            search_word = original_word.replace("-", "+")
            if date == "None": 
                endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0?keyword=" + f'{search_word}'
            else: 
                endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0?modStartDate=" + f'{date}' + "T00:00:00:000 UTC-05:00&keyword=" + f'{search_word}'
            async with session.get(endpoint) as cve_response:
                if (cve_response.status == 200):
                    cve_result = await cve_response.json()
    
                    if cve_result['totalResults'] == 0:
                        all_data[original_word] = []
                        return
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
    
                        if severity == "None" or dic.get("base_severity") in severity: 
                            result_list.append(dic)
                    all_data[original_word] = result_list
                else:
                    all_data[original_word] = []
                

# root_packages = {"react", "node"}
# my_output = {"react" : ["react-dependency1", "react-dependency2"], "node": ["node-dependency2"], 
#                 "react-dependency1": [] , "react-dependency2": [] , "node-dependency2": [] }
# your_output ={"react": [], "node": [{"node vulnerbilities": "bef", "xyz": "bb"}, {"x": "y"}], "react-dependency1": [{"react1 vulnerbilities" : "bjef"}], "react-dependency2": [{"react2 vulnerbilities" : "ibnief"}], "node-dependency2" : []}

def root_format(root_package, my_output, your_output, level, max_level):
    resulting_dic = {}
    if level == max_level+1:
        return resulting_dic
    for i in root_package:
        resulting_dic[i] = [{},your_output[i]]
        dependencies = my_output[i]
        for dependency in dependencies:
            resulting_dic[i][0].update(root_format({dependency}, my_output, your_output, level+1, max_level))
    return resulting_dic

# print(new_function(root_packages, my_output, your_output))

# print(package_detail_retrieval("npm", ["react", "node"], level=1))

# package_list = ["react", "node"]
# package_output = {'react': ['loose-envify', 'object-assign'], 'node': ['node-bin-setup'], 'loose-envify': ['js-tokens'], 'object-assign': [], 'node-bin-setup': []}
# steven_output = package_list_data(package_output) #, ["CRITICAL"], "2021-01-01")

# print(root_format(package_list, package_output, steven_output, 0, 1))

# package_dic = package_detail_retrieval("npm", ["react", "node"])
# output = package_list_data(package_dic, ["CRITICAL"], "2021-01-01")
# print(root_format(["react", "node"], package_dic, output, 0, 1))

# print(len(package_list_data({"react" : ['loose-envify', 'object-assign']})))
