import asyncio
import pytest
from queue import Queue

from package_detail_retrieval import package_detail_retrieval 
from vuln_search import package_list_data, root_format, extract_relevant_data

from unittest import TestCase

class TestPackageList(TestCase):
    def test_valid_return(self):
        loop = asyncio.get_event_loop()
        package_output = {'react': ['loose-envify', 'object-assign'], 'node': ['node-bin-setup'], 'loose-envify': ['js-tokens'], 'object-assign': [], 'node-bin-setup': []}
        result = loop.run_until_complete(package_list_data(package_output))
        assert(len(result) > 0)

    def test_invalid_input(self):
        loop = asyncio.get_event_loop()
        package_output = {}
        result = loop.run_until_complete(package_list_data(package_output))
        assert(result == {}) 

class TestExtractRelevantData(TestCase):
    def test_invalid_input(self):
        loop = asyncio.get_event_loop()
        queue = Queue()
        # queue.put("react")
        # queue.put("node")
        result = loop.run_until_complete(extract_relevant_data(queue))
        result_no_severity = loop.run_until_complete(extract_relevant_data(queue, "None"))
        result_no_date = loop.run_until_complete(extract_relevant_data(queue, "None", "None"))
        assert(result is None)
        assert(result_no_severity is None)
        assert(result_no_date is None)

class TestRootFormat(TestCase):
    def test_valid_root_input(self):
        package_output = {'react': ['loose-envify', 'object-assign'], 'node': ['node-bin-setup'], 'loose-envify': ['js-tokens'], 'object-assign': [], 'node-bin-setup': []}
        loop = asyncio.get_event_loop() #, ["CRITICAL"], "2021-01-01")
        result = loop.run_until_complete(package_list_data(package_output))
        package_dic = package_detail_retrieval("npm", ["react", "node"])
        assert (len(root_format(["react", "node"], package_dic, result, 0, 1)) > 0 )

    def test_invalid_root_input(self):
        package_output = {'react': ['loose-envify', 'object-assign'], 'node': ['node-bin-setup'], 'loose-envify': ['js-tokens'], 'object-assign': [], 'node-bin-setup': []}
        loop = asyncio.get_event_loop() #, ["CRITICAL"], "2020-01-01")
        result = loop.run_until_complete(package_list_data(package_output))
        package_dic = package_detail_retrieval("npm", ["react", "node"])
        assert (root_format(["react", "node"], package_dic, result, 1, 0) == {} )