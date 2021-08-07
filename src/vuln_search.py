import requests
import asyncio
import aiohttp
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from package_detail_retrieval import package_detail_retrieval 

#The terms vulnerability and CVE are used interchangeably throughout this document. CVE means Common Vulnerability Enumeration

#The terms product and CPE are used interchangeably throughout this document.
#CPE means Common Platform Enumeration, version 2.3, a standard for identifying and searching products. Need to include vulnerability cpes/1.0?addOns=cves

'''
Goes through the dictionary returned from npm dependencies, returning the package name as the key and the cve details as a value
'''
async def package_list_data(package_dic, severity="None", date="None"):
    all_data = {}
    if len(package_dic) == 0:
        return all_data
    work_queue = asyncio.Queue()
    for x in package_dic.keys():
        await work_queue.put(x)
    await asyncio.gather(asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)),asyncio.create_task(extract_relevant_data(work_queue,severity,date,all_data)))
    return all_data

'''
for one package, return the cve details found using the keyword search in the NVD API
https://services.nvd.nist.gov/rest/json/cves/1.0?keyword=
'''
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
                
'''
recursively return our results so that our dependencies belong to the key of our original package list
'''
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

