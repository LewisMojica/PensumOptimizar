# Pensum Optimizer

> **Minimize the number of semesters needed to complete your degree by finding the fastest path through course prerequisites and credit constraints.**

Find the optimal academic path through your university degree requirements using graph algorithms and mathematical optimization.

## 🎯 What It Does

Pensum Optimizer calculates the **minimum time to graduation** by optimally scheduling courses while respecting:
- Course prerequisites (dependency chains)
- Credit limits per semester/cuatrimestre
- Convalidated (transferred) credits

## 🚀 Key Benefits

- **Front-load your degree**: Take heavy course loads early, light loads later
- **Work-life balance**: Create opportunities for internships and part-time work in later periods
- **Strategic planning**: See the critical path through your program requirements
- **Optimize transfers**: Account for convalidated credits in your planning

## 📊 Example Results

**Traditional Schedule**: 12 cuatrimestres @ ~18 credits each  
**Optimized Schedule**: 
- **Cuatrimestres 1-3**: Heavy load (~24 credits) - grind it out early
- **Cuatrimestres 4-12**: Light load (4-16 credits) - work part-time, less stress

*Same graduation timeline, but 75% of your degree with manageable course loads!*

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.7+
- No additional dependencies required (uses only standard library)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pensum-optimizer.git
   cd pensum-optimizer
   ```

2. **Prepare your pensum data** (see [JSON Format](#json-format) below)

3. **Run the optimizer**
   ```bash
   # Using your pensum file
   python pensum_optimizer.py your_pensum.json
   
   # Using sample data (for testing)
   python pensum_optimizer.py
   ```

4. **Follow the interactive prompts**
   - Enter convalidated course codes (comma-separated)
   - Set max credits per semester/cuatrimestre
   - Choose optimization algorithm

### Example Session
```
=== Pensum Optimizer Phase 1 ===

Loaded 54 courses from unapec_ing_software.json
Enter convalidated course codes: MAT101, ESP101, ING102
Convalidated courses: {'MAT101', 'ESP101', 'ING102'}
Remaining courses after convalidation: 51
Enter max credits per semester (default 18): 24
Use optimal knapsack? (y/N): y

=== RESULTS ===
Total semesters needed: 12

Semester 1 (24 credits):
  - SOC101: Sociología (3 cr)
  - MAT201: Matemática II (4 cr)
  - ESP106: Español II (3 cr)
  ...
```

## 📋 JSON Format

Create a JSON file with your pensum structure:

```json
{
  "courses": [
    {
      "code": "MAT101",
      "name": "Matemática I",
      "credits": 4,
      "prerequisites": []
    },
    {
      "code": "MAT201", 
      "name": "Matemática II",
      "credits": 4,
      "prerequisites": ["MAT101"]
    },
    {
      "code": "ING205",
      "name": "Base de Datos",
      "credits": 4,
      "prerequisites": ["ING102", "MAT101"]
    }
  ]
}
```

### Required Fields
- `code`: Unique course identifier
- `credits`: Number of credits for the course
- `prerequisites`: Array of course codes that must be completed first

### Optional Fields
- `name`: Course name (can be empty string or omitted)

## 🧠 How It Works

The optimizer uses **graph theory** and **optimization algorithms**:

1. **Model as DAG**: Courses become nodes, prerequisites become directed edges
2. **Topological Scheduling**: Find courses with no pending prerequisites each semester
3. **Knapsack Optimization**: Select optimal course combinations within credit limits
4. **Iterative Planning**: Repeat until all courses are scheduled

### Algorithm Options
- **Greedy Knapsack**: Fast approximation, prioritizes smaller courses
- **Optimal Knapsack**: Dynamic programming approach for maximum courses per semester

## 🎓 Perfect For

- **University Students**
- **Engineering Programs** with complex prerequisite chains
- **Transfer Students** with convalidated credits
- **Working Students** who need flexible scheduling
- **Academic Advisors** planning student pathways

## 🔮 Roadmap

- [ ] Web interface for easy use
- [ ] Support for corequisites (courses taken simultaneously)
- [ ] Course offering schedules (fall/spring/summer availability)
- [ ] Multiple optimization objectives (minimize semesters vs balance load)
- [ ] Export to calendar applications
- [ ] Support for elective requirements and specialization tracks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## ⚠️ Disclaimer

This tool provides mathematical optimization based on course prerequisites and credit constraints. Always verify results with your academic advisor and check official university policies regarding:
- Maximum credits per semester
- Course availability by semester
- Graduation requirements
- Academic standing requirements

---

**Built with ❤️ for students who want to optimize their academic journey**
