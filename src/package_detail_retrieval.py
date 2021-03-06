import requests
	
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
			for frontier in explore_frontiers:
				results[frontier] = []
			return
		# loop through the levels
		for frontier in explore_frontiers:
			# # store this frontiers dependency
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
			# collect dependencies keys which will be the pack name
			for dependecy in dependencies:
				new_explore_frontiers.append(dependecy)
				frontier_dependency.append(dependecy)
				# !!! UNCOMMENT BELOW IF VERSION NUMBER NEEDED !!!
				# package_name, package_version = get_viable_npm_version(dependecy,dependencies[dependecy])
				# frontier_dependency.append(package_name+"=="+package_version)
				# new_explore_frontiers.append(package_name+"=="+package_version)
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
			results(dictionary): {packages_1: 1, packages_2: 1, ....}
	'''
	results = {}
	
	if package_manager_type ==  "npm":
		npm_dependecies_search(package_list,level,results)
	return results
	