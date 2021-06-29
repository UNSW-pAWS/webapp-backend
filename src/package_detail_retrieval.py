import requests

# ^x.y.z y and z can be bigger or itself but x must match
# ~x.y.z z can be bigger or itself but x and y must match
# range
# a || b a and b creteria
# * everything 
# a - b everything from a to b 
def get_viable_npm_version(package_name, version):
	# base case where version had been specified
	if "^" not in version and "~" not in version and "*" not in version and ">" not in version and "<" not in version and "-" not in version:
		return package_name, version
	# query registery and get json reply
	link = "https://registry.npmjs.org/{}".format(package_name)
	response = requests.get(link)
	json_response = response.json()
	# get all the version and turn it into a list
	package_versions = list(json_response["versions"].keys())
	# find latest version that match x
	if "^" in version:
		standard_version = version.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			found_version = False
			for h in range(0, max_length):
				if h==0 and int(compare_version[h]) > int(standard_version[h][1:]):
					break
				if h==0 and int(compare_version[h]) == int(standard_version[h][1:]):
					x_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) == int(standard_version[h][1:]):
					version = package_versions[i]
					found_version = True
				if h==1 and int(compare_version[h]) >= int(standard_version[h]) and x_match==True:
					version = package_versions[i]
					found_version = True
				if h == 2 and not compare_version[h].isnumeric() and x_match==True:
					found_version = False
			if found_version == True:
				break
	# find latest version that match x and y
	elif "~" in version:
		standard_version = version.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			y_match = False
			found_version = False
			for h in range(0, max_length):
				if h==0 and int(compare_version[h]) > int(standard_version[h][1:]):
					break
				if h==0 and int(compare_version[h]) == int(standard_version[h][1:]):
					x_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) == int(standard_version[h][1:]):
					version = package_versions[i]
					found_version = True
				if h==1 and max_length == 2 and int(compare_version[h]) == int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and int(compare_version[h]) == int(standard_version[h]) and x_match==True:
					y_match = True
				if h == 2 and compare_version[h].isnumeric() and int(compare_version[h]) >= int(standard_version[h]) and x_match==True and y_match==True:
					found_version = True
					version = package_versions[i]
			if found_version == True:
				break
	# default to latest as everything fits
	elif "*" in version:
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			found_version = True
			for h in range(0, len(compare_version)):
				if not compare_version[h].isnumeric():
					found_version = False
			if found_version == True:
				version = package_versions[i]
				break
	elif "-" in version:
		upper_bound = version.split("-")[1]
		standard_version = upper_bound.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			y_match = False
			found_version = False
			for h in range(0, max_length):
				if not standard_version[h].isnumeric():
					break
				if h==0 and int(compare_version[h]) > int(standard_version[h]):
					break
				if h==0 and int(compare_version[h]) <= int(standard_version[h]):
					x_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) <= int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and max_length == 2 and int(compare_version[h]) <= int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and int(compare_version[h]) <= int(standard_version[h]) and x_match==True:
					y_match = True
				if h == 2 and compare_version[h].isnumeric() and int(compare_version[h]) <= int(standard_version[h]) and x_match==True and y_match==True:
					found_version = True
					version = package_versions[i]
			if found_version == True:
				break
	# find latest that match createria
	elif "||" in version:
		package_name ,version = get_viable_npm_version(package_name, version.split("||")[1])
	# find latest that match createria
	elif ">=" in version: 
		split_result = version.split(">=")
		if "^" in split_result[1] or "~" in split_result[1] or "*" in split_result[1] or ">" in split_result[1] or "<" in split_result[1] or "-" in split_result[1]:
			return get_viable_npm_version(package_name, split_result[1])
		upper_bound = split_result[1].lstrip()
		standard_version = upper_bound.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			y_match = False
			found_version = False
			for h in range(0, max_length):
				if not standard_version[h].isnumeric() and h ==0:
					break
				if h==0 and int(compare_version[h]) >= int(standard_version[h]):
					x_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) >= int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and max_length == 2 and int(compare_version[h]) >= int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and int(compare_version[h]) >= int(standard_version[h]) and x_match==True:
					y_match = True
				if h == 2 and compare_version[h].isnumeric() and int(compare_version[h]) >= int(standard_version[h]) and x_match==True and y_match==True:
					found_version = True
					version = package_versions[i]
			if found_version == True:
				break
	elif ">" in version:
		split_result = version.split(">=")
		if "^" in split_result[1] or "~" in split_result[1] or "*" in split_result[1] or ">" in split_result[1] or "<" in split_result[1] or "-" in split_result[1]:
			return get_viable_npm_version(package_name, split_result[1])
		upper_bound = split_result[1].lstrip()
		standard_version = upper_bound.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			y_match = False
			found_version = False
			for h in range(0, max_length):
				if not standard_version[h].isnumeric() and h ==0:
					break
				if h==0 and int(compare_version[h]) >= int(standard_version[h]):
					x_match = True
				if h==1 and int(compare_version[h]) >= int(standard_version[h]) and x_match==True:
					y_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) > int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and max_length == 2 and int(compare_version[h]) > int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h == 2 and compare_version[h].isnumeric() and int(compare_version[h]) > int(standard_version[h]) and x_match==True and y_match==True:
					found_version = True
					version = package_versions[i]
			if found_version == True:
				break
	elif "<=" in version:
		split_result = version.split("<=")
		if "^" in split_result[1] or "~" in split_result[1] or "*" in split_result[1] or ">" in split_result[1] or "<" in split_result[1] or "-" in split_result[1]:
			return get_viable_npm_version(package_name, split_result[1])
		upper_bound = split_result[1].lstrip()
		standard_version = upper_bound.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			y_match = False
			found_version = False
			for h in range(0, max_length):
				if not standard_version[h].isnumeric() and h ==0:
					break
				if h==0 and int(compare_version[h]) <= int(standard_version[h]):
					x_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) <= int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and max_length == 2 and int(compare_version[h]) <= int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and int(compare_version[h]) <= int(standard_version[h]) and x_match==True:
					y_match = True
				if h == 2 and compare_version[h].isnumeric() and int(compare_version[h]) <= int(standard_version[h]) and x_match==True and y_match==True:
					found_version = True
					version = package_versions[i]
			if found_version == True:
				break
	elif "<" in version:
		split_result = version.split("<")
		if "^" in split_result[1] or "~" in split_result[1] or "*" in split_result[1] or ">" in split_result[1] or "<" in split_result[1] or "-" in split_result[1]:
			return get_viable_npm_version(package_name, split_result[1])
		upper_bound = split_result[1].lstrip()
		standard_version = upper_bound.split(".")
		for i in range(len(package_versions)-1,-1,-1):
			compare_version = package_versions[i].split(".")
			max_length = min(len(standard_version),len(compare_version))
			x_match = False
			y_match = False
			found_version = False
			for h in range(0, max_length):
				if not standard_version[h].isnumeric() and h ==0:
					break
				if h==0 and int(compare_version[h]) <= int(standard_version[h]):
					x_match = True
				if h==0 and max_length == 1 and int(compare_version[h]) < int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and max_length == 2 and int(compare_version[h]) < int(standard_version[h]):
					version = package_versions[i]
					found_version = True
				if h==1 and int(compare_version[h]) <= int(standard_version[h]) and x_match==True:
					y_match = True
				if h == 2 and compare_version[h].isnumeric() and int(compare_version[h]) < int(standard_version[h]) and x_match==True and y_match==True:
					found_version = True
					version = package_versions[i]
			if found_version == True:
				break
	return package_name,version
	
'''
for npm query site: https://registry.npmjs.org/npm/,
Documentation: https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md,
usage: https://registry.npmjs.org/[package name]/[version if specified or type 'latest'] -> return json object -> json_object["dependencies"] to get dependencies
need to understand the version number system: https://semver.npmjs.com/
'''
def npm_dependecies_search(package_list, level, results):
	# first exploration
	explore_frontiers = package_list
	# first level is level 0 so start from -1
	level_explored = -1
	# keep exploring till there is nothing to explore
	while len(explore_frontiers) != 0:
		# keep track of package in the next level
		new_explore_frontiers = []
		# if explored to level desired return result
		if level_explored == level:
			return
		# loop through the levels
		for frontier in explore_frontiers:
			# store this frontiers dependency
			frontier_dependency = []
			# if in results the frontier had been explored no visiting again
			if frontier in results:
				continue
			# need both package and version to query
			package = ""
			version = ""
			# package version specified
			if "==" in frontier:
				split_result = frontier.split("==")
				package = split_result[0]
				version = split_result[1]
			# no package version specified default to latest
			else:
				package = frontier
				version = "latest"
			# query registery and get json reply
			link = "https://registry.npmjs.org/{}/{}".format(package, version)
			response = requests.get(link)
			json_response = response.json()
			# store the dependencies
			dependencies = {}
			# if there is dependencies store them
			if "dependencies" in json_response:
				dependencies = json_response["dependencies"]
			# scan the dependencies if it needs latest or a specific version
			for dependecy in dependencies:
				package_name, package_version = get_viable_npm_version(dependecy,dependencies[dependecy])
				frontier_dependency.append(package_name+"=="+package_version)
				new_explore_frontiers.append(package_name+"=="+package_version)
			# store the dependencies in the dictionary
			results[frontier] = frontier_dependency
		# update the next level
		explore_frontiers = new_explore_frontiers
		# level explored increased
		level_explored += 1
	
def package_detail_retrieval(package_manager_type, package_list, level=1):
	'''
	Returns a dictionary of packages(key) and their relavent dependencies(value).
		
		Parameters:
			package_manager_type (string): (e.g) npm, yarn
			package_list(list of strings): a list of packages with or without version numbers (e.g react-dom, react-dom==1.2.1)
			level(int): the level user wants to explore (default to 1)
		
		Returns:
			results(dictionary): {packages_1: [dependency_1, dependency_2, ...], packages_2: [dependency_1, dependency_2, ...], ....}
	'''
	results = {}
	
	if package_manager_type ==  "npm":
		npm_dependecies_search(package_list,level,results)
	return results
	