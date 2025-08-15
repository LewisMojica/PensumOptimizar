import sys
import json
from typing import List, Dict, Set
from collections import defaultdict, deque

class Course:
	def __init__(self, code: str, name: str, credits: int, prerequisites: List[str]):
		self.code = code
		self.name = name
		self.credits = credits
		self.prerequisites = prerequisites
 
	 	  	
	def __repr__(self):
		return f"{self.code}({self.credits}cr)"

class PensumDAG:
	def __init__(self, courses: List[Course]):
		self.courses = {course.code: course for course in courses}
		self.in_degree = {}
		self.graph = defaultdict(list)	# prerequisite -> [courses that need it]
		self._build_graph()
	
	def _build_graph(self):
		# Initialize in-degrees
		for course_code in self.courses:
			self.in_degree[course_code] = 0
		
		# Build dependency graph and calculate in-degrees
		for course in self.courses.values():
			self.in_degree[course.code] = len(course.prerequisites)
			for prereq in course.prerequisites:
				if prereq in self.courses:	# Make sure prerequisite exists
					self.graph[prereq].append(course.code)
	
	def get_available_courses(self) -> List[Course]:
		"""Return courses with no pending prerequisites"""
		available = []
		for course_code, degree in self.in_degree.items():
			if degree == 0 and course_code in self.courses:
				available.append(self.courses[course_code])
		return available
	
	def complete_courses(self, completed_courses: List[Course]):
		"""Remove completed courses and update dependencies"""
		for course in completed_courses:
			# Remove from courses dict
			if course.code in self.courses:
				del self.courses[course.code]
			
			# Remove from in_degree
			if course.code in self.in_degree:
				del self.in_degree[course.code]
			
			# Update in-degrees of courses that depended on this one
			for dependent_course in self.graph[course.code]:
				if dependent_course in self.in_degree:
					self.in_degree[dependent_course] -= 1
	
	def has_courses(self) -> bool:
		return len(self.courses) > 0

def greedy_knapsack(courses: List[Course], max_credits: int) -> List[Course]:
	"""Simple greedy knapsack: select courses until credit limit reached"""
	selected = []
	total_credits = 0
	
	# Sort by credits ascending (take smaller courses first to fit more)
	courses.sort(key=lambda c: c.credits)
	
	for course in courses:
		if total_credits + course.credits <= max_credits:
			selected.append(course)
			total_credits += course.credits
	
	return selected

def optimal_knapsack_dp(courses: List[Course], max_credits: int) -> List[Course]:
	"""Dynamic programming knapsack for optimal course selection"""
	n = len(courses)
	if n == 0:
		return []
	
	# DP table: dp[i][w] = maximum courses we can take with first i courses and w credits
	dp = [[0 for _ in range(max_credits + 1)] for _ in range(n + 1)]
	
	# Fill the DP table
	for i in range(1, n + 1):
		course = courses[i-1]
		for w in range(max_credits + 1):
			# Don't take this course
			dp[i][w] = dp[i-1][w]
			
			# Take this course if possible (and if it's beneficial)
			if course.credits <= w:
				dp[i][w] = max(dp[i][w], dp[i-1][w - course.credits] + 1)
	
	# Backtrack to find which courses were selected
	selected = []
	w = max_credits
	for i in range(n, 0, -1):
		course = courses[i-1]
		if dp[i][w] != dp[i-1][w]:	# This course was selected
			selected.append(course)
			w -= course.credits
	
	return selected

class GreedyScheduler:
	def __init__(self, max_credits_per_semester: int, use_optimal_knapsack: bool = False):
		self.max_credits_per_semester = max_credits_per_semester
		self.use_optimal_knapsack = use_optimal_knapsack
	
	def schedule(self, dag: PensumDAG) -> List[List[Course]]:
		schedule = []
		semester = 0
		
		while dag.has_courses():
			semester += 1
			print(f"Planning semester {semester}...")
			
			# Get available courses
			available = dag.get_available_courses()
			print(f"  Available courses: {available}")
			
			if not available:
				print("  ERROR: No available courses but DAG not empty!")
				print(f"  Remaining courses: {list(dag.courses.keys())}")
				break
			
			# Select courses for this semester
			if self.use_optimal_knapsack:
				selected = optimal_knapsack_dp(available, self.max_credits_per_semester)
			else:
				selected = greedy_knapsack(available, self.max_credits_per_semester)
			
			total_credits = sum(course.credits for course in selected)
			print(f"  Selected: {selected} (Total: {total_credits} credits)")
			
			# Complete the selected courses
			dag.complete_courses(selected)
			schedule.append(selected)
		
		return schedule

def load_pensum_from_json(filename: str) -> List[Course]:
	"""Load pensum from JSON file"""
	with open(filename, 'r', encoding='utf-8') as f:
		data = json.load(f)
	
	courses = []
	for course_data in data['courses']:
		course = Course(
			code=course_data['code'],
			name=course_data['name'],
			credits=course_data['credits'],
			prerequisites=course_data['prerequisites']
		)
		courses.append(course)
	
	return courses

def remove_convalidated_courses(courses: List[Course], convalidated: Set[str]) -> List[Course]:
	"""Remove convalidated courses from the course list"""
	return [course for course in courses if course.code not in convalidated]

def main():
	print("=== Pensum Scheduler Phase 1 ===\n") 
	json_file = sys.argv[1] if len(sys.argv) > 1 else None
	# Load pensum
	try:
		courses = load_pensum_from_json(json_file)
		print(f"Loaded {len(courses)} courses from {json_file}")
	except FileNotFoundError:
		print(f"{json_file} not found.")
		return 1	
	# Get convalidated courses
	convalidated_input = input("\nEnter convalidated course codes (comma separated, or Enter for none): ").strip()
	convalidated = set()
	if convalidated_input:
		convalidated = {code.strip() for code in convalidated_input.split(',')}
		print(f"Convalidated courses: {convalidated}")
	
	# Remove convalidated courses
	courses = remove_convalidated_courses(courses, convalidated)
	print(f"Remaining courses after convalidation: {len(courses)}")
	
	# Get max credits per semester
	max_credits = int(input("Enter max credits per semester (default 18): ") or "18")
	
	# Choose algorithm
	algo_choice = input("Use optimal knapsack? (y/N): ").strip().lower()
	use_optimal = algo_choice == 'y'
	
	# Create DAG and scheduler
	dag = PensumDAG(courses)
	scheduler = GreedyScheduler(max_credits, use_optimal)
	
	print(f"\n=== Scheduling with {'Optimal' if use_optimal else 'Greedy'} Knapsack ===")
	
	# Generate schedule
	schedule = scheduler.schedule(dag)
	
	# Display results
	print(f"\n=== RESULTS ===")
	print(f"Total semesters needed: {len(schedule)}")
	
	for i, semester in enumerate(schedule, 1):
		total_credits = sum(course.credits for course in semester)
		print(f"\nSemester {i} ({total_credits} credits):")
		for course in semester:
			print(f"  - {course.code}: {course.name} ({course.credits} cr)")
	
	total_credits = sum(sum(course.credits for course in semester) for semester in schedule)
	print(f"\nTotal credits: {total_credits}")

if __name__ == "__main__":
	main()
