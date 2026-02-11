from dataclasses import dataclass
import json
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re
import sys

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = []

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	
	#check length of recipeName
	if len(recipeName) <= 0:
		return None
	
	# replcae hypens and underscores with space
	recipeName = recipeName.replace("-", " ")
	recipeName = recipeName.replace("_", " ")

	# check if char is whitespace or alphabet
	for i in recipeName:
		if i != " " and not i.isalpha():
			recipeName = recipeName.replace(i, "")
	
	# split words, capitlalize them and then join them
	words = recipeName.split()
	cap_words = [i.capitalize() for i in words]
	recipeName = " ".join(cap_words)

	return recipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	# TODO: implement me
	data = request.get_json()

	# print(data, file=sys.stderr)
	# string_entry = data.get('enrty', '')
	# entry = json.loads(string_entry)

	# print(entry, file=sys.stderr)

	if data["type"] != "recipe" and data["type"] != 'ingredient':
		return "type is neither a recipe nor ingredient", 400
	
	if data["type"] == "ingredient" and data["cookTime"] < 0:
		return 'cooktime must be greater than or equal to 0', 400
	
	for i in cookbook: 
		if data["name"] == i["name"]:
			return 'entry names must be unique', 400
	
	cookbook.append(data)
	# print(cookbook, file=sys.stderr)
	
	return {}, 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	foodName = request.args.get('name')
	print(foodName, file=sys.stderr)
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
