import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import random
import threading
import time
from tkinter import scrolledtext, ttk
from customtkinter import ThemeManager

class Observer:
    def __init__(self):
        self.observations = []

    def observe(self, message):
        self.observations.append(message)
        return self.analyze(message)

    def analyze(self, message):
        keywords = {
            'efficiency': ['quick', 'fast', 'efficient', 'streamlined'],
            'quality': ['thorough', 'detailed', 'comprehensive', 'high-quality'],
            'innovation': ['new', 'innovative', 'creative', 'novel'],
            'teamwork': ['collaborate', 'team', 'together', 'cooperation']
        }

        analysis = "Observer: "
        for category, words in keywords.items():
            if any(word in message.lower() for word in words):
                analysis += f"Good {category}. "

        if not analysis.endswith(": "):
            return analysis
        else:
            return "Observer: No significant observations."

class KnowledgeBase:
    def __init__(self):
        self.knowledge = {}

    def add_knowledge(self, key, value):
        self.knowledge[key] = value

    def get_knowledge(self, key):
        return self.knowledge.get(key, None)

    def has_knowledge(self, key):
        return key in self.knowledge

class Task:
    def __init__(self, number, priority, description, team):
        self.number = number
        self.priority = priority
        self.description = description
        self.team = team
        self.status = "Not Started"  # Can be "Not Started", "In Progress", "Completed", or "Failed"

class TreeNode:
    def __init__(self, content, node_type, status="Not Started"):
        self.content = content
        self.node_type = node_type
        self.status = status
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def update_status(self, new_status):
        self.status = new_status

class Question:
    def __init__(self, number, description, choices, agent):
        self.number = number
        self.description = description
        self.choices = choices
        self.agent = agent
        self.status = "Unanswered"  # Can be "Unanswered", "Answered"
        self.selected_choice = None

class Agent:
    def __init__(self, name, team, expertise, gui):
        self.name = name
        self.team = team
        self.expertise = expertise
        self.status = "idle"
        self.learning_module = LearningModule()  
        self.gui = gui
        self.knowledge_base = KnowledgeBase()
        self.initialize_knowledge()
            
    def initialize_knowledge(self):
        if "Planner" in self.team:
            self.knowledge_base.add_knowledge("planning_techniques", ["SWOT analysis", "Gantt charts", "Critical path method"])
        elif "Frontend" in self.team:
            self.knowledge_base.add_knowledge("frontend_frameworks", ["React", "Vue", "Angular"])
        elif "Backend" in self.team:
            self.knowledge_base.add_knowledge("backend_technologies", ["Node.js", "Django", "Flask"])
        # Add more team-specific knowledge initializations here
        
    def __str__(self):
        return f"{self.name} ({self.team})"
    
    def handle_task(self, task):
        self.status = "working"
        # Add message when agent takes a task
        self.gui.chat_display.insert(tk.END, f"{self.name} has taken task #{task.number}: {task.description}\n\n")
        self.gui.chat_display.see(tk.END)
        
        # Use knowledge base for decision making
        if self.knowledge_base.has_knowledge("planning_techniques") and "plan" in task.description.lower():
            technique = random.choice(self.knowledge_base.get_knowledge("planning_techniques"))
            self.gui.chat_display.insert(tk.END, f"{self.name} is using {technique} for planning.\n")
        
        # Simulate task processing
        time.sleep(random.uniform(0.5, 1))
        task.status = "In Progress"
        start_time = time.time()
        # Simulate task completion
        time.sleep(random.uniform(0.5, 1))
        task.status = "Completed" if random.random() > 0.1 else "Failed"
        # Add message when agent completes a task
        self.gui.chat_display.insert(tk.END, f"{self.name} has {task.status.lower()} task #{task.number}\n\n")
        self.gui.chat_display.see(tk.END)
        self.status = "idle"
        end_time = time.time()
        self.learning_module.record_experience(task.description, task.status, end_time - start_time)

    def learn_new_knowledge(self, key, value):
        self.knowledge_base.add_knowledge(key, value)
        self.gui.chat_display.insert(tk.END, f"{self.name} learned new knowledge: {key}\n")

    def storm_response(self, topic):
        # Simulate more creative and in-depth AGENTSTORM responses
        responses = [
            f"{self.name} proposes a revolutionary approach to {topic} using {self.expertise}.",
            f"{self.name} challenges conventional wisdom on {topic} with a {self.team}-inspired solution.",
            f"{self.name} synthesizes ideas from multiple domains to address {topic}.",
            f"{self.name} envisions a future where {topic} transforms the industry.",
            f"{self.name} identifies potential paradigm shifts related to {topic}."
        ]
        return random.choice(responses)

class ScenarioSimulator:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
    
    def generate_scenario(self):
        scenario = {
            "tasks": random.sample(self.tasks, k=min(random.randint(1, max(1, len(self.tasks))), len(self.tasks))) if self.tasks else [],
            "available_agents": random.sample(self.agents, k=random.randint(1, len(self.agents))) if self.agents else [],
            "time_limit": random.randint(10, 60),
            "resource_constraint": random.choice(["low", "medium", "high"])
        }
        return scenario
    
    def generate_specific_scenario(self, scenario_type):
        if scenario_type == "High Pressure":
            return {
                "tasks": random.sample(self.tasks, k=len(self.tasks)),
                "available_agents": self.agents[:len(self.agents)//2],
                "time_limit": 30,
                "resource_constraint": "high"
            }
        elif scenario_type == "Resource Scarcity":
            return {
                "tasks": random.sample(self.tasks, k=len(self.tasks)//2),
                "available_agents": random.sample(self.agents, k=len(self.agents)//3),
                "time_limit": 45,
                "resource_constraint": "low"
            }
        elif scenario_type == "Complex Tasks":
            complex_tasks = [task for task in self.tasks if task.priority == "High"]
            return {
                "tasks": complex_tasks,
                "available_agents": self.agents,
                "time_limit": 60,
                "resource_constraint": "medium"
            }    
    
    def run_scenario(self, scenario):
        results = {
            "completed_tasks": 0,
            "failed_tasks": 0,
            "time_taken": 0
        }
        
        start_time = time.time()
        for task in scenario["tasks"]:
            available_agent = next((agent for agent in scenario["available_agents"] if agent.team in task.team.split(',')), None)
            if available_agent:
                available_agent.handle_task(task)
                if task.status == "Completed":
                    results["completed_tasks"] += 1
                else:
                    results["failed_tasks"] += 1
            else:
                results["failed_tasks"] += 1
        
        results["time_taken"] = time.time() - start_time
        return results

class LearningModule:
    def __init__(self):
        self.experience = {}
    
    def record_experience(self, task_type, outcome, time_taken):
        if task_type not in self.experience:
            self.experience[task_type] = []
        self.experience[task_type].append((outcome, time_taken))
    
    def get_success_rate(self, task_type):
        if task_type not in self.experience:
            return 0
        outcomes = [exp[0] for exp in self.experience[task_type]]
        return outcomes.count("Completed") / len(outcomes)
    
    def get_average_time(self, task_type):
        if task_type not in self.experience:
            return 0
        times = [exp[1] for exp in self.experience[task_type]]
        return sum(times) / len(times)

class ProjectSetup:
    def __init__(self):
        self.default_setup = {
            "Level 1 Planner": 1,
            "Level 2 Team Orchestra": 1,
            "Level 2-1 Team Plan Build": 1,
            "Level 2-2 Team Structure": 1,
            "Level 2-3 Team Engine choice and build": 1,
            "Level 2-4 Team Art choice and prompt build": 1,
            "Level 2-5 Team Quality Assurance": 1,
            "Level 3 Task Maker Logic": 1,
            "Level 3-1 Team GUI Frontend Logic": 1,
            "Level 3-2 Team Backend Logic": 1,
            "Level 3-3 Team Engine Logic": 1,
            "Level 3-4 Team Preview Art": 1,
            "Level 3-5 Team Quality Assist logic": 1,
            "Level 4 Task Manager Code": 1,
            "Level 4-1 Team GUI Frontend Code": 1,
            "Level 4-2 Team Backend Code": 1,
            "Level 4-3 Team Engine Code": 1,
            "Level 4-4 Team Art Refiner": 1,
            "Level 5 Reviewer": 1,
            "Level 5-1 Team Review GUI Frontend": 1,
            "Level 5-2 Team Review Backend": 1,
            "Level 5-3 Team ReviewArt": 1,
            "Level 5-4 Team ReviewEngine": 1,
            "Level 6 Debugger and Error Fixer": 1,
            "Level 6-1 Team GUI Debug": 1,
            "Level 6-2 Team Backend Debug": 1,
            "Level 6-3 Team Engine Debug": 1,
            "Level 6-4 Team Art Debug": 1,
            "Level 6-5 Team Quality Assist Debug": 1,
            "Level 7 Finalizer": 1,
            "Level 7-1 Team Documentation": 1,
            "Level 7-2 Team Manual and Requirements": 1,
        }
        
    def get_setup(self, project_type, prompt):
        if project_type == "Game" and "2D" in prompt:
            return self.get_2d_game_setup()
        elif project_type == "App" and "Desktop" in prompt:
            return self.get_desktop_app_setup()
        # Add more project type checks here
        else:
            return self.default_setup        
        
    def get_2d_game_setup(self):
        return {
            "Level 1 Planner": 1,
            "Level 2 Team Orchestra": 1,
            "Level 2-1 Team Plan Build": 1,
            "Level 2-2 Team Structure": 1,
            "Level 2-3 Team Engine choice and build": 2,
            "Level 2-4 Team Art choice and prompt build": 3,
            "Level 2-5 Team Quality Assurance": 1,
            "Level 3 Task Maker Logic": 1,
            "Level 3-1 Team GUI Frontend Logic": 1,
            "Level 3-2 Team Backend Logic": 1,
            "Level 3-3 Team Engine Logic": 2,
            "Level 3-4 Team Preview Art": 2,
            "Level 3-5 Team Quality Assist logic": 1,
            "Level 4 Task Manager Code": 1,
            "Level 4-1 Team GUI Frontend Code": 1,
            "Level 4-2 Team Backend Code": 1,
            "Level 4-3 Team Engine Code": 2,
            "Level 4-4 Team Art Refiner": 2,
            "Level 5 Reviewer": 1,
            "Level 5-1 Team Review GUI Frontend": 1,
            "Level 5-2 Team Review Backend": 1,
            "Level 5-3 Team ReviewArt": 2,
            "Level 5-4 Team ReviewEngine": 1,
            "Level 6 Debugger and Error Fixer": 1,
            "Level 6-1 Team GUI Debug": 1,
            "Level 6-2 Team Backend Debug": 1,
            "Level 6-3 Team Engine Debug": 1,
            "Level 6-4 Team Art Debug": 2,
            "Level 6-5 Team Quality Assist Debug": 1,
            "Level 7 Finalizer": 1,
            "Level 7-1 Team Documentation": 1,
            "Level 7-2 Team Manual and Requirements": 1
        }
    
    def get_desktop_app_setup(self):
        setup = self.default_setup.copy()
        setup.update({
            "Level 1 Planner": 1,
            "Level 3-1 Team GUI Frontend Logic": 2,
            "Level 4-1 Team GUI Frontend Code": 2,
            "Level 5-1 Team Review GUI Frontend": 2,
            "Level 6-1 Team GUI Debug": 2
        })
        return setup

class AgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MasterMindGPT-2")
        self.root.geometry("1400x900")
        self.current_goal = "No goal set"
        self.current_work = "Nothing in progress"    
        self.task_tree = None  
        self.project_setup = ProjectSetup()
        self.create_custom_themes()
        
        self.teams = [
            "Level 1 Planner",
            "Level 2 Team Orchestra",
            "Level 2-1 Team Plan Build",
            "Level 2-2 Team Structure",
            "Level 2-3 Team Engine choice and build",
            "Level 2-4 Team Art choice and prompt build",
            "Level 2-5 Team Quality Assurance",
            "Level 3 Task Maker Logic",
            "Level 3-1 Team GUI Frontend Logic",
            "Level 3-2 Team Backend Logic",
            "Level 3-3 Team Engine Logic",
            "Level 3-4 Team Preview Art",
            "Level 3-5 Team Quality Assist logic",
            "Level 4 Task Manager Code",
            "Level 4-1 Team GUI Frontend Code",
            "Level 4-2 Team Backend Code",
            "Level 4-3 Team Engine Code",
            "Level 4-4 Team Art Refiner",
            "Level 5 Reviewer",
            "Level 5-1 Team Review GUI Frontend",
            "Level 5-2 Team Review Backend",
            "Level 5-3 Team ReviewArt",
            "Level 5-4 Team ReviewEngine",
            "Level 6 Debugger and Error Fixer",
            "Level 6-1 Team GUI Debug",
            "Level 6-2 Team Backend Debug",
            "Level 6-3 Team Engine Debug",
            "Level 6-4 Team Art Debug",
            "Level 6-5 Team Quality Assist Debug",
            "Level 7 Finalizer",
            "Level 7-1 Team Documentation",
            "Level 7-2 Team Manual and Requirements"
        ]
        
        self.agent_names = {
            "Level 1 Planner": "Athena",
            "Level 2 Team Orchestra": "Orpheus",
            "Level 2-1 Team Plan Build": "Daedalus",
            "Level 2-2 Team Structure": "Atlas",
            "Level 2-3 Team Engine choice and build": "Hephaestus",
            "Level 2-4 Team Art choice and prompt build": "Apollo",
            "Level 2-5 Team Quality Assurance": "Argus",
            "Level 3 Task Maker Logic": "Prometheus",
            "Level 3-1 Team GUI Frontend Logic": "Hermes",
            "Level 3-2 Team Backend Logic": "Hecate",
            "Level 3-3 Team Engine Logic": "Vulcan",
            "Level 3-4 Team Preview Art": "Iris",
            "Level 3-5 Team Quality Assist logic": "Thoth",
            "Level 4 Task Manager Code": "Odysseus",
            "Level 4-1 Team GUI Frontend Code": "Arachne",
            "Level 4-2 Team Backend Code": "Pythia",
            "Level 4-3 Team Engine Code": "Daedalus",
            "Level 4-4 Team Art Refiner": "Pygmalion",
            "Level 5 Reviewer": "Janus",
            "Level 5-1 Team Review GUI Frontend": "Narcissus",
            "Level 5-2 Team Review Backend": "Mnemosyne",
            "Level 5-3 Team ReviewArt": "Momus",
            "Level 5-4 Team ReviewEngine": "Epimetheus",
            "Level 6 Debugger and Error Fixer": "Asclepius",
            "Level 6-1 Team GUI Debug": "Hygieia",
            "Level 6-2 Team Backend Debug": "Panacea",
            "Level 6-3 Team Engine Debug": "Iaso",
            "Level 6-4 Team Art Debug": "Aceso",
            "Level 6-5 Team Quality Assist Debug": "Aglaea",
            "Level 7 Finalizer": "Nike",
            "Level 7-1 Team Documentation": "Clio",
            "Level 7-2 Team Manual and Requirements": "Themis"
        }
                                
        self.agents = self.create_agents()        
        self.observer = Observer()
        self.tasks = []
        self.questions = []    
        self.task_counter = 1
        self.scenario_simulator = ScenarioSimulator(self.agents, self.tasks)  # Now this line will work
        self.learning_enabled = tk.BooleanVar(value=True)
        self.ai_answer_var = tk.BooleanVar(value=True)                
        self.create_widgets()
        self.agentstorm_active = False            

    def create_custom_themes(self):
        self.custom_themes = {
            "custom_blue": {
                "CTkButton": {
                    "fg_color": ["#1F6AA5", "#1F6AA5"],
                    "hover_color": ["#144870", "#144870"]
                }
            },
            "custom_green": {
                "CTkButton": {
                    "fg_color": ["#2D6A4F", "#2D6A4F"],
                    "hover_color": ["#1B4332", "#1B4332"]
                }
            },
            "custom_gray": {
                "CTkButton": {
                    "fg_color": ["#2C3E50", "#2C3E50"],
                    "hover_color": ["#34495E", "#34495E"]
                }
            }
        }


    def handle_project_type(self, prompt, project_type, use_default):
        print("Handling project type")
        if self.agentstorm_active:
            messagebox.showwarning("AgentStorm Active", "Please wait for the current AgentStorm simulation to complete.")
            return
        
        if not project_type:
            messagebox.showwarning("Project Type Missing", "Please select a project type.")
            return
        
        if not prompt:
            messagebox.showwarning("Prompt Missing", "Please enter a project prompt.")
            return
        
        if project_type == "Custom":
            project_type = simpledialog.askstring("Custom Project Type", "Enter a custom project type:")
            if not project_type:
                return
        
        if project_type == "Game":
            self.choose_game_type(prompt)
        elif project_type == "App":
            self.choose_app_type(prompt)
        
        setup = self.project_setup.default_setup if use_default else self.project_setup.get_setup(project_type, prompt)
        
        print(f"Project Type: {project_type}")
        print(f"Prompt: {prompt}")
        print(f"Using {'default' if use_default else 'custom'} setup")
        print(f"Setup: {setup}")
        print(f"Total agents in setup: {sum(setup.values())}")
        
        self.clear_existing_agents()
        print("now creating agents form setup")
        self.create_agents_from_setup(setup)
        self.update_agent_buttons()
        
        print("\nStarting full run simulation")
        self.chat_display.insert(tk.END, f"Starting project: {project_type} - {prompt}\n\n")
        self.chat_display.see(tk.END)
        
        threading.Thread(target=self.simulate_full_run, args=(prompt,), daemon=True).start()

    def clear_existing_agents(self):
        self.agents.clear()
        for widget in self.agents_display.winfo_children():
            widget.destroy()        
    
    def display_task_tree(self):
        tree_window = ctk.CTkToplevel(self.root)
        tree_window.title("Task and Question Tree")
        tree_window.geometry("800x600")
        tree_frame = ctk.CTkScrollableFrame(tree_window)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame)
        tree.pack(fill=tk.BOTH, expand=True)

        # Define tag colors
        tree.tag_configure('not_started', background='gray')
        tree.tag_configure('in_progress', background='yellow')
        tree.tag_configure('completed', background='green')
        tree.tag_configure('failed', background='red')

        def add_node_to_tree(node, parent="", level=0):
            node_text = "  " * level + node.content
            node_id = tree.insert(parent, "end", text=node_text, open=True)
            
            # Assign color based on node status
            if hasattr(node, 'status'):
                tree.item(node_id, tags=(node.status.lower().replace(" ", "_"),))
            
            for child in node.children:
                add_node_to_tree(child, node_id, level + 1)

        if self.task_tree:
            add_node_to_tree(self.task_tree)

        tree_window.focus_force()
        self.focus_window(tree_window)

    def create_agent(self, name, team, expertise):
        print(f"Creating agent standard: {name} ({team})")
        return Agent(name, team, expertise, self)

    def create_agents(self):
        agents = []
        for team in self.teams:
            agent_name = self.agent_names.get(team, f"Agent{team.split()[-1]}")
            expertise = "Specialized in " + " ".join(team.split()[2:])
            agents.append(self.create_agent(agent_name, team, expertise))
            print(f"Created agent default: {agent_name} ({team})")
        return agents
    
    def create_agents_from_setup(self, setup):
        agents = []
        for team, count in setup.items():
            for i in range(count):
                agent_name = f"{self.agent_names.get(team, 'Agent')}_{i+1}"
                expertise = "Specialized in " + " ".join(team.split()[2:])
                agents.append(self.create_agent(agent_name, team, expertise))
                print(f"Created agent from setup: {agent_name} ({team})")
        
        if not any(agent.team == "Level 1 Planner" for agent in agents):
            planner_name = f"{self.agent_names.get('Level 1 Planner', 'Planner')}_1"
            agents.append(self.create_agent(planner_name, "Level 1 Planner", "Specialized in Planning"))
        
        return agents

    def run_simulation(self):
        scenario = self.scenario_simulator.generate_scenario()
        results = self.scenario_simulator.run_scenario(scenario)
        self.chat_display.insert(tk.END, f"Scenario Results: {results}\n\n")
        self.chat_display.see(tk.END)

    def focus_window(self, window):
        window.lift()
        window.focus_force()
        window.grab_set()
        window.wait_window()
        self.safe_destroy(window)

    def delete_question(self, question):
        self.questions.remove(question)
        self.update_questions_display()

    def add_question(self):
        add_question_window = ctk.CTkToplevel(self.root)
        add_question_window.title("Add Question")
        add_question_window.geometry("400x500")

        ctk.CTkLabel(add_question_window, text="Description:").grid(row=0, column=0, pady=5)
        description_entry = ctk.CTkEntry(add_question_window, width=300)
        description_entry.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(add_question_window, text="Choices (comma-separated):").grid(row=1, column=0, pady=5)
        choices_entry = ctk.CTkEntry(add_question_window, width=300)
        choices_entry.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(add_question_window, text="Agent:").grid(row=2, column=0, pady=5)
        agent_var = tk.StringVar(value=self.agents[0].name)
        agent_dropdown = ctk.CTkOptionMenu(add_question_window, variable=agent_var, values=[agent.name for agent in self.agents])
        agent_dropdown.grid(row=2, column=1, pady=5)

        def submit_question():
            description = description_entry.get()
            choices = [choice.strip() for choice in choices_entry.get().split(',')]
            agent = next(agent for agent in self.agents if agent.name == agent_var.get())
            
            if not description or len(choices) < 2:
                messagebox.showwarning("Invalid Input", "Please enter a description and at least two choices.")
                return
            
            question = Question(len(self.questions) + 1, description, choices, agent)
            self.questions.append(question)
            self.update_questions_display()
            add_question_window.destroy()

        ctk.CTkButton(add_question_window, text="Submit", command=submit_question).grid(row=3, column=0, columnspan=2, pady=10)
        self.focus_window(add_question_window)
        add_question_window.grid_columnconfigure(1, weight=1)

    def update_questions_display(self):
        for widget in self.questions_display.winfo_children():
            widget.destroy()

            question_count = len(self.questions)
            self.questions_count_label.configure(text=f"Questions and Choices({question_count})")

        for i, question in enumerate(self.questions):
            question_frame = ctk.CTkFrame(self.questions_display)
            question_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

            status_colors = {
                "Unanswered": "gray",
                "Answered": "green"
            }

            question_button = ctk.CTkButton(
                question_frame,
                text=f"#{question.number} | Agent: {question.agent.name} | Status: {question.status}",
                fg_color=status_colors[question.status],
                command=lambda q=question: self.show_question_details(q)
            )
            question_button.grid(row=0, column=0, sticky="ew")

            answer_button = ctk.CTkButton(
                question_frame,
                text="Answer",
                command=lambda q=question: self.answer_question(q)
            )
            answer_button.grid(row=0, column=1)

            delete_button = ctk.CTkButton(
                question_frame,
                text="Delete",
                command=lambda q=question: self.delete_question(q)
            )
            delete_button.grid(row=0, column=2)
            question_frame.grid_columnconfigure(0, weight=1)
        self.questions_display.grid_columnconfigure(0, weight=1)

    def show_question_details(self, question):
        details = f"Question #{question.number}\nDescription: {question.description}\nAgent: {question.agent.name}\nChoices: {', '.join(question.choices)}\nStatus: {question.status}"
        if question.selected_choice:
            details += f"\nSelected Choice: {question.selected_choice}"
        messagebox.showinfo("Question Details", details)
                
    def answer_question(self, question):
        if self.ai_answer_var.get():
            # AI-handled answer
            ai_choice = random.choice(question.choices)
            question.selected_choice = ai_choice
            question.status = "Answered"
            self.update_questions_display()
            self.chat_display.insert(tk.END, f"AI answered question #{question.number}: {ai_choice}\n\n")
            self.chat_display.see(tk.END)
        else:
            # Manual answer
            answer_window = ctk.CTkToplevel(self.root)
            answer_window.title("Answer Question")
            answer_window.geometry("400x300")

            question_label = ctk.CTkLabel(answer_window, text=question.description, wraplength=380)
            question_label.pack(pady=10)

            choice_var = tk.StringVar(value=question.choices[0])
            for choice in question.choices:
                ctk.CTkRadioButton(answer_window, text=choice, variable=choice_var, value=choice).pack(pady=5)

            def update_answer():
                question.selected_choice = choice_var.get()
                question.status = "Answered"
                self.update_questions_display()
                answer_window.destroy()

            ctk.CTkButton(answer_window, text="Submit Answer", command=update_answer).pack(pady=10)
            self.focus_window(answer_window)

    def update_status_labels(self):
        self.goal_label.configure(text=f"Current Goal: {self.current_goal}")
        self.work_label.configure(text=f"Current Work: {self.current_work}")

    def simulate_full_run(self, prompt):
        phases = [
            ("Initializing project", self.initialize_project),
            ("Planning phase", self.execute_planning_phase),
            ("Subtask creation phase", self.execute_subtask_creation_phase),
            ("Question creation phase", self.execute_question_creation_phase),
            ("Detailed task creation phase", self.execute_detailed_task_creation_phase),
            ("Task execution phase", self.execute_task_execution_phase),
            ("Review phase", self.execute_review_phase),
            ("Debugging phase", self.execute_debugging_phase),
            ("Finalization phase", self.execute_finalization_phase)
        ]
        
        if not self.agents:
            print("Error: No agents created. Aborting simulation.")
            self.chat_display.insert(tk.END, "Error: No agents created. Aborting simulation.\n\n")
            self.chat_display.see(tk.END)
            return
        
        subtasks = None
        for phase_name, phase_function in phases:
            print(f"\nStarting {phase_name}")
            self.chat_display.insert(tk.END, f"Starting {phase_name}...\n")
            self.chat_display.see(tk.END)
            
            if phase_name == "Initializing project":
                result = phase_function(prompt)
            elif phase_name == "Subtask creation phase":
                subtasks = phase_function()
            elif phase_name == "Question creation phase":
                result = phase_function(subtasks)
            else:
                result = phase_function()
            
            print(f"Completed {phase_name}")
            self.chat_display.insert(tk.END, f"Completed {phase_name}\n\n")
            self.chat_display.see(tk.END)
            
        print("\nFull run simulation completed")
        self.chat_display.insert(tk.END, "Project simulation completed!\n\n")
        self.chat_display.see(tk.END)


    def initialize_project(self, prompt):
        self.task_tree = TreeNode("Project", "goal")
        prompt_node = TreeNode(prompt, "prompt")
        self.task_tree.add_child(prompt_node)
        self.current_goal = prompt
        self.current_work = "Planning"
        self.update_status_labels()
        self.update_chat_display(f"Received prompt: {prompt}\n\n")

    def execute_planning_phase(self):
        self.current_work = "creating a high-level plan"
        self.update_status_labels()
        try:
            planner = next(agent for agent in self.agents if agent.team == "Level 1 Planner")
            plan_node = self.simulate_planning(planner, self.current_goal, self.update_chat_display)
        
            # Add the plan_node to the task tree
            self.task_tree.children[0].add_child(plan_node)
            
            # Update the current work to reflect the completed plan
            self.current_work = f"high-level plan created: {plan_node.content}"
        except StopIteration:
            # Handle the case where no planner is found
            self.current_work = "Unable to create high-level plan: No Level 1 Planner found"
            self.update_chat_display("Error: No Level 1 Planner agent available.\n")
        
        if not self.task_tree or not self.task_tree.children:
            # Initialize task_tree if it's not already set up
            self.task_tree = TreeNode("Project", "goal")
            prompt_node = TreeNode(self.current_goal, "prompt")
            self.task_tree.add_child(prompt_node)
                       
        self.update_status_labels()

    def execute_subtask_creation_phase(self):
        self.current_work = "creating subtasks"
        self.update_status_labels()
        
        if self.task_tree and self.task_tree.children:
            if self.task_tree.children[0].children:
                subtasks = self.simulate_subtask_creation(self.task_tree.children[0].children[0], self.update_chat_display)
            else:
                # Handle case where first child doesn't have children
                subtasks = self.simulate_subtask_creation(self.task_tree.children[0], self.update_chat_display)
        else:
            # Handle case where task_tree is empty or has no children
            self.update_chat_display("Error: Task tree is not properly initialized.\n")
            subtasks = []
        
        return subtasks

    def execute_question_creation_phase(self, subtasks):
        self.current_work = "creating questions"
        self.update_status_labels()
        self.update_questions_display()
        self.simulate_question_creation(subtasks, self.update_chat_display)    
    
    def execute_detailed_task_creation_phase(self):
        self.current_work = "creating detailed tasks"
        self.update_status_labels()
        detailed_tasks = self.simulate_detailed_task_creation([subtask.content for subtask in self.task_tree.children[0].children[0].children], self.update_chat_display)
        return detailed_tasks
    
    def execute_task_execution_phase(self):
        self.current_work = "working on tasks"
        self.update_status_labels()
        self.simulate_task_execution(self.tasks, self.update_chat_display)
        
    def execute_review_phase(self):
        self.current_work = "reviewing the work"
        self.update_status_labels()
        self.simulate_review(self.update_chat_display)
        
    def execute_debugging_phase(self):
        self.current_work = "debugging and fixing issues"
        self.update_status_labels()
        self.simulate_debugging(self.update_chat_display)
        
    def execute_finalization_phase(self):
        self.current_work = "finalizing the project"
        self.update_status_labels()
        self.simulate_finalization(self.update_chat_display)
        
    def update_chat_display(self, message):
        self.chat_display.insert(tk.END, message)
        self.chat_display.see(tk.END)
        self.update_observer(message)            
    
    def update_observer(self, message):
        observation = self.observer.observe(message)
        self.root.after(0, lambda: self.observer_display.insert(tk.END, f"Observation: {observation}\n\n"))
        self.root.after(0, self.observer_display.see, tk.END)
    
    def simulate_planning(self, planner, prompt, update_gui):
        update_gui(f"{planner.name} is creating a high-level plan...\n")
        time.sleep(random.uniform(0.1, 0.5))
        plan = f"Plan for '{prompt}': 1. Analyze requirements 2. Design solution 3. Implement core features 4. Test and refine 5. Deliver final product"
        update_gui(f"Plan created: {plan}\n\n")
        plan_node = TreeNode(plan, "plan")
        self.task_tree.children[0].add_child(plan_node)
        return plan_node

    def simulate_subtask_creation(self, plan_node, update_gui):
        subtasks = []
        for team in self.teams:
            if team.startswith("Level 2"):
                try:
                    agent = next(a for a in self.agents if a.team == team)
                except StopIteration:
                    update_gui(f"No agent found for team {team}. Skipping subtask creation for this team.\n")
                    continue
                
                update_gui(f"{agent.name} is creating subtasks...\n")
                self.current_work = f"creating subtasks for {team}"
                self.root.after(0, self.update_status_labels)
                time.sleep(random.uniform(0.1, 0.5))
                subtask = f"Subtask for {team}: {random.choice(['Design', 'Implement', 'Test'])} {random.choice(['frontend', 'backend', 'database', 'API'])}"
                subtask_node = TreeNode(subtask, "subtask")
                plan_node.add_child(subtask_node)
                subtasks.append(subtask)             
                update_gui(f"Subtask created: {subtask}\n")
        
        update_gui("\n")
        self.root.after(0, self.update_tasks_display)
        return subtasks

    def simulate_question_creation(self, subtasks, update_gui):
        for team in self.teams:
            if team.startswith("Level 3"):
                agent = next(a for a in self.agents if a.team == team)
                update_gui(f"{agent.name} is creating questions...\n")
                self.current_work = f"creating questions for {team}"
                self.root.after(0, self.update_status_labels)
                time.sleep(random.uniform(0.1, 0.5))
                question = Question(self.task_counter, f"Question for {subtasks[random.randint(0, len(subtasks)-1)]}", 
                [f"Answer {i+1}" for i in range(4)], agent)
                self.questions.append(question)
                self.task_counter += 1
                update_gui(f"Question created: {question.description}\n")
                    
        update_gui("\n")
        self.root.after(0, self.update_questions_display)

    def simulate_detailed_task_creation(self, subtasks, update_gui):
        detailed_tasks = []
        for team in self.teams:
            if team.startswith("Level 3"):
                agent = next(a for a in self.agents if a.team == team)
                update_gui(f"{agent.name} is creating detailed tasks...\n")
                self.current_work = f"creating detailed tasks for {team}"
                self.root.after(0, self.update_status_labels)
                time.sleep(random.uniform(0.1, 0.5))
                
                subtask = random.choice(subtasks)
                task = Task(self.task_counter, random.choice(["Low", "Medium", "High"]),
                            f"Detailed task for {subtask}", team)
                
                # Add task to the tree
                subtask_node = self.find_subtask_node(subtask)
                if subtask_node:
                    task_node = TreeNode(task.description, "task")
                    subtask_node.add_child(task_node)
                
                detailed_tasks.append(task)
                self.tasks.append(task)
                self.task_counter += 1
                update_gui(f"Detailed task created: {task.description}\n")
                self.root.after(0, self.update_tasks_display)
                time.sleep(0.05)  # Small delay to allow GUI update
                
        update_gui("\n")
        return detailed_tasks

    def find_subtask_node(self, subtask):
        def search_tree(node):
            if node.node_type == "subtask" and node.content == subtask:
                return node
            for child in node.children:
                result = search_tree(child)
                if result:
                    return result
        return search_tree(self.task_tree)

    def simulate_task_execution(self, detailed_tasks, update_gui):
        for team in self.teams:
            if team.startswith("Level 4"):
                agent = next(a for a in self.agents if a.team == team)
                update_gui(f"{agent.name} is working on tasks...\n")
                self.current_work = f"working on tasks for {team}"
                self.root.after(0, self.update_status_labels)
                for task in detailed_tasks:
                    agent.handle_task(task)
                    self.root.after(0, self.update_tasks_display)
                    time.sleep(0.05)  # Small delay to allow GUI update
 
        update_gui("\n")

    def simulate_review(self, update_gui):
        for team in self.teams:
            if team.startswith("Level 5"):
                agent = next(a for a in self.agents if a.team == team)
                update_gui(f"{agent.name} is reviewing the work...\n")
                self.current_work = f"reviewing the work for {team}"
                self.root.after(0, self.update_status_labels)
                time.sleep(random.uniform(0.1, 0.5))
                update_gui(f"Review complete: {random.choice(['Passed', 'Needs improvements'])}\n")
 
        update_gui("\n")

    def simulate_debugging(self, update_gui):
        for team in self.teams:
            if team.startswith("Level 6"):
                agent = next(a for a in self.agents if a.team == team)
                update_gui(f"{agent.name} is debugging and fixing issues...\n")
                self.current_work = f"debugging and fixing issues for {team}"
                self.root.after(0, self.update_status_labels)
                time.sleep(random.uniform(0.1, 0.5))
                update_gui(f"Debugging complete: {random.randint(0, 5)} issues fixed\n")
 
        update_gui("\n")

    def simulate_finalization(self, update_gui):
        for team in self.teams:
            if team.startswith("Level 7"):
                agent = next(a for a in self.agents if a.team == team)
                update_gui(f"{agent.name} is finalizing the project...\n")
                self.current_work = f"finalizing the project for {team}"
                self.root.after(0, self.update_status_labels)
                time.sleep(random.uniform(0.1, 0.5))
                update_gui(f"Finalization complete: {agent.team} tasks finished\n")

        update_gui("\nProject simulation completed!\n\n")

    def create_toplevel_window(self, title, geometry, content_function):
        window = ctk.CTkToplevel(self.root)
        window.title(title)
        window.geometry(geometry)
        content_function(window)
        self.focus_window(window)
        return window

    def open_options_window(self):
        def content(window):
            # Color theme options
            ctk.CTkLabel(window, text="Color Theme:").pack(anchor="w", padx=10, pady=5)
            themes = ["Dark Blue", "Dark Green", "Dark Gray", "Light Blue", "Light Green", "Light Gray"]
            color_menu = ctk.CTkOptionMenu(window, values=themes, command=self.change_color_theme)
            color_menu.pack(fill="x", padx=10, pady=5)

            # Observer toggle
            self.observer_var = tk.BooleanVar(value=True)
            observer_check = ctk.CTkCheckBox(window, text="Enable Observer", variable=self.observer_var, command=self.toggle_observer)
            observer_check.pack(anchor="w", padx=10, pady=5)

            # Auto retry failed tasks
            self.auto_retry_var = tk.BooleanVar(value=False)
            auto_retry_check = ctk.CTkCheckBox(window, text="Auto Retry Failed Tasks", variable=self.auto_retry_var)
            auto_retry_check.pack(anchor="w", padx=10, pady=5)

            # AI/Manual question answering
            self.ai_answer_var = tk.BooleanVar(value=True)
            ai_answer_check = ctk.CTkCheckBox(window, text="AI-handled Question Answers", variable=self.ai_answer_var)
            ai_answer_check.pack(anchor="w", padx=10, pady=5)

            # Start/Stop AGENTSTORM button
            self.agentstorm_button = ctk.CTkButton(window, text="Start AGENTSTORM", command=self.toggle_agentstorm)
            self.agentstorm_button.pack(fill="x", padx=10, pady=5)
            
            # Learning Module toggle
            ctk.CTkCheckBox(window, text="Enable Learning Module", variable=self.learning_enabled).pack(anchor="w", padx=10, pady=5)

            # Scenario Simulation button
            ctk.CTkButton(window, text="Run Scenario Simulation", command=self.open_scenario_window).pack(fill="x", padx=10, pady=5)

        self.create_toplevel_window("Options", "400x400", content)

    def open_prompt_window(self):
        def content(window):
            ctk.CTkLabel(window, text="Enter your prompt:").pack(pady=10)
            prompt_entry = ctk.CTkEntry(window, width=300)
            prompt_entry.pack(pady=10)

            project_types = ["App", "Game", "Project for ideas", "Excel file"]
            project_var = tk.StringVar(value=project_types[0])
            project_dropdown = ctk.CTkOptionMenu(window, variable=project_var, values=project_types)
            project_dropdown.pack(pady=10)
            
            self.setup_preview = ctk.CTkLabel(window, text="", wraplength=400)
            self.setup_preview.pack(pady=10)
            
            self.use_default_var = tk.BooleanVar(value=False)
            ctk.CTkCheckBox(window, text="Use default setup", variable=self.use_default_var, command=self.update_setup_preview).pack(pady=10)

            def submit_prompt():
                prompt = prompt_entry.get()
                project_type = project_var.get()
                use_default = self.use_default_var.get()
                window.destroy()
                threading.Thread(target=self.handle_project_type, args=(prompt, project_type, use_default), daemon=True).start()

            ctk.CTkButton(window, text="Submit", command=submit_prompt).pack(pady=10)

            self.update_setup_preview()  # Initial update

        self.create_toplevel_window("Enter Prompt", "500x300", content)
   
   
    def create_widgets(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
              
        # Observer window
        observer_frame = ctk.CTkFrame(self.root)
        observer_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        observer_label = ctk.CTkLabel(observer_frame, text="Observer")
        observer_label.pack(pady=5)
        
        self.observer_display = scrolledtext.ScrolledText(observer_frame, wrap=tk.WORD, width=30, height=30)
        self.observer_display.pack(expand=True, fill=tk.BOTH)

        # Prompt button and status labels
        prompt_frame = ctk.CTkFrame(self.root)
        prompt_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.start_button = ctk.CTkButton(prompt_frame, text="Start with prompt", command=self.open_prompt_window)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.goal_label = ctk.CTkLabel(prompt_frame, text=f"Current Goal: {self.current_goal}")
        self.goal_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.work_label = ctk.CTkLabel(prompt_frame, text=f"Current Work: {self.current_work}")
        self.work_label.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        prompt_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Chat display
        chat_frame = ctk.CTkFrame(self.root)
        chat_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=70, height=16)
        self.chat_display.pack(expand=True, fill=tk.BOTH)

        # Tasks window
        tasks_frame = ctk.CTkFrame(self.root)
        tasks_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        tasks_label = ctk.CTkLabel(tasks_frame, text="Tasks")
        tasks_label.pack(pady=5)
        
        self.tasks_display = ctk.CTkScrollableFrame(tasks_frame, width=900, height=150)
        self.tasks_display.pack(expand=True, fill=tk.BOTH)
        
        task_button_frame = ctk.CTkFrame(tasks_frame)
        task_button_frame.pack(fill=tk.X, pady=5)
        
        self.add_task_button = ctk.CTkButton(task_button_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=5)

        # Agents window
        agents_frame = ctk.CTkFrame(self.root)
        agents_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")

        # Add the options button above the agents window
        self.options_button = ctk.CTkButton(agents_frame, text="Options", command=self.open_options_window)
        self.options_button.pack(pady=5)

        agents_label = ctk.CTkLabel(agents_frame, text="Agents")
        agents_label.pack(pady=5)

        self.agents_display = ctk.CTkScrollableFrame(agents_frame, width=250, height=800)
        self.agents_display.pack(expand=True, fill=tk.BOTH)

        self.update_agent_buttons()
            
        # Tasks and Questions window
        tasks_questions_frame = ctk.CTkFrame(self.root)
        tasks_questions_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Tasks half
        tasks_frame = ctk.CTkFrame(tasks_questions_frame)
        tasks_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.tasks_count_label = ctk.CTkLabel(tasks_frame, text="Tasks(0)")
        self.tasks_count_label.pack(pady=5)
        
        self.tasks_display = ctk.CTkScrollableFrame(tasks_frame, width=450, height=150)
        self.tasks_display.pack(expand=True, fill=tk.BOTH)
        
        task_button_frame = ctk.CTkFrame(tasks_frame)
        task_button_frame.pack(fill=tk.X, pady=5)
        
        self.add_task_button = ctk.CTkButton(task_button_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=5)

        self.update_tasks_display()
        
        # Questions and Choices half
        questions_frame = ctk.CTkFrame(tasks_questions_frame)
        questions_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
             
        self.questions_count_label = ctk.CTkLabel(questions_frame, text="Questions and Choices(0)")
        self.questions_count_label.pack(pady=5)        
                      
        self.questions_display = ctk.CTkScrollableFrame(questions_frame, width=450, height=150)
        self.questions_display.pack(expand=True, fill=tk.BOTH)
        
        question_button_frame = ctk.CTkFrame(questions_frame)
        question_button_frame.pack(fill=tk.X, pady=5)
        
        self.add_question_button = ctk.CTkButton(question_button_frame, text="Add Question", command=self.add_question)
        self.add_question_button.pack(side=tk.LEFT, padx=5)
        
        self.update_questions_display()
        
        # Display Task Tree button
        self.display_tree_button = ctk.CTkButton(self.root, text="Display Task Tree", command=self.display_task_tree)
        self.display_tree_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        tasks_questions_frame.grid_columnconfigure(0, weight=1)
        tasks_questions_frame.grid_columnconfigure(1, weight=1)

    # Add a new method to clean up agent buttons
    def cleanup_agent_buttons(self):
        for button in self.agent_buttons:
            if button.winfo_exists():
                button.destroy()
        self.agent_buttons.clear()

    def safe_destroy(self, widget):
        if widget.winfo_exists():
            widget.destroy()

    def open_scenario_window(self):
        scenario_window = ctk.CTkToplevel(self.root)
        scenario_window.title("Scenario Simulation")
        scenario_window.geometry("300x200")

        scenarios = ["Random", "High Pressure", "Resource Scarcity", "Complex Tasks"]
        scenario_var = tk.StringVar(value=scenarios[0])        
        ctk.CTkOptionMenu(scenario_window, variable=scenario_var, values=scenarios).pack(pady=10)
        
        def run_selected_scenario():
            selected_scenario = scenario_var.get()
            if selected_scenario == "Random":
                scenario = self.scenario_simulator.generate_scenario()
            else:
                scenario = self.scenario_simulator.generate_specific_scenario(selected_scenario)
            results = self.scenario_simulator.run_scenario(scenario)
            self.chat_display.insert(tk.END, f"Scenario '{selected_scenario}' Results: {results}\n\n")
            self.chat_display.see(tk.END)
            scenario_window.destroy()
        ctk.CTkButton(scenario_window, text="Run Scenario", command=run_selected_scenario).pack(pady=10)
        self.focus_window(scenario_window)
                                
    def change_color_theme(self, theme):
        if theme.startswith("Dark"):
            ctk.set_appearance_mode("dark")
            bg_color = "gray20"
            text_color = "white"
        else:
            ctk.set_appearance_mode("light")
            bg_color = "gray90"
            text_color = "black"
        
        if "Blue" in theme:
            accent_color = "blue"
        elif "Green" in theme:
            accent_color = "green"
        else:  # Gray
            accent_color = "gray"
        
        def update_widget_colors(widget):
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=accent_color, text_color=text_color)
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=bg_color)
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=text_color)
            
            for child in widget.winfo_children():
                update_widget_colors(child)
        
        update_widget_colors(self.root)
        
        # Update colors for text widgets
        self.chat_display.configure(bg=bg_color, fg=text_color)
        self.observer_display.configure(bg=bg_color, fg=text_color)
        
        self.root.update_idletasks()
        self.root.update()

    def toggle_observer(self):
        if self.observer_var.get():
            self.observer_display.pack(expand=True, fill=tk.BOTH)
        else:
            self.observer_display.pack_forget()

    def update_setup_preview(self, *args):
        project_type = self.project_var.get() if hasattr(self, 'project_var') else "App"
        use_default = self.use_default_var.get()
        
        if use_default:
            setup = self.project_setup.default_setup
            plan_name = "Default Setup"
        else:
            setup = self.project_setup.get_setup(project_type, "")
            plan_name = f"{project_type} Specific Setup"
        
        total_agents = sum(setup.values())
        
        preview_text = f"Plan: {plan_name}\nTotal Agents: {total_agents}"
        
        self.setup_preview.configure(text=preview_text)

    def choose_app_type(self, prompt):
        app_window = ctk.CTkToplevel(self.root)
        app_window.title("Choose App Type")
        app_window.geometry("300x150")

        ctk.CTkLabel(app_window, text="Select app type:").pack(pady=10)
        app_types = ["Desktop", "Server-client based"]
        app_var = tk.StringVar(value=app_types[0])
        app_dropdown = ctk.CTkOptionMenu(app_window, variable=app_var, values=app_types)
        app_dropdown.pack(pady=10)

        def submit_app_type():
            app_type = app_var.get()
            app_window.destroy()
            setup = self.project_setup.get_setup("App", f"{prompt} - {app_type} app")
            self.clear_existing_agents()
            self.create_agents_from_setup(setup)
            self.update_agent_buttons()
            threading.Thread(target=self.simulate_full_run, args=(f"{prompt} - {app_type} app",), daemon=True).start()

        ctk.CTkButton(app_window, text="Submit", command=submit_app_type).pack(pady=10)
        self.focus_window(app_window)

    def choose_game_type(self, prompt):
        game_window = ctk.CTkToplevel(self.root)
        game_window.title("Choose Game Type")
        game_window.geometry("300x150")

        ctk.CTkLabel(game_window, text="Select game type:").pack(pady=10)
        game_types = ["2D", "3D"]
        game_var = tk.StringVar(value=game_types[0])
        game_dropdown = ctk.CTkOptionMenu(game_window, variable=game_var, values=game_types)
        game_dropdown.pack(pady=10)

        def submit_game_type():
            game_type = game_var.get()
            game_window.destroy()
            setup = self.project_setup.get_setup("Game", f"{prompt} - {game_type} game")
            self.clear_existing_agents()
            self.create_agents_from_setup(setup)
            self.update_agent_buttons()
            threading.Thread(target=self.simulate_full_run, args=(f"{prompt} - {game_type} game",), daemon=True).start()

        ctk.CTkButton(game_window, text="Submit", command=submit_game_type).pack(pady=10)
        self.focus_window(game_window)

        
    def update_agent_buttons(self):
        def update():
            for widget in self.agents_display.winfo_children():
                widget.destroy()
            
            # Initialize the list to store button references
            self.agent_buttons = []    
            
            agent_count = len(self.agents)
            count_label = ctk.CTkLabel(self.agents_display, text=f"Total Agents: {agent_count}")
            count_label.pack(pady=5, padx=5, fill=tk.X)
                        
            grouped_agents = {}
            for agent in self.agents:
                major_level = agent.team.split()[1].split('-')[0]
                if major_level not in grouped_agents:
                    grouped_agents[major_level] = {}
                sub_level = agent.team.split()[1]
                if sub_level not in grouped_agents[major_level]:
                    grouped_agents[major_level][sub_level] = []
                grouped_agents[major_level][sub_level].append(agent)

            for major_level, sub_levels in grouped_agents.items():
                major_frame = ctk.CTkFrame(self.agents_display)
                major_frame.pack(pady=5, padx=5, fill=tk.X)

                sub_levels_frame = ctk.CTkFrame(major_frame)
                sub_levels_frame.pack(fill=tk.X, padx=10)

                def toggle_major_group(frame=sub_levels_frame):
                    if frame.winfo_viewable():
                        frame.pack_forget()
                    else:
                        frame.pack(fill=tk.X, padx=10)

                major_short_name = ' '.join(next(iter(sub_levels.values()))[0].team.split()[2:4])
                major_label = ctk.CTkButton(major_frame, text=f"Level {major_level} {major_short_name}", font=("Arial", 12, "bold"), command=toggle_major_group)
                major_label.pack(pady=2, padx=5, fill=tk.X)

                for sub_level, agents in sub_levels.items():
                    sub_frame = ctk.CTkFrame(sub_levels_frame)
                    sub_frame.pack(pady=2, fill=tk.X)

                    agents_frame = ctk.CTkFrame(sub_frame)
                    agents_frame.pack(fill=tk.X, padx=10)

                    def toggle_sub_group(frame=agents_frame):
                        if frame.winfo_viewable():
                            frame.pack_forget()
                        else:
                            frame.pack(fill=tk.X, padx=10)

                    sub_short_name = ' '.join(agents[0].team.split()[2:4])
                    sub_label = ctk.CTkButton(sub_frame, text=f"Level {sub_level} {sub_short_name}", font=("Arial", 11), command=toggle_sub_group)
                    sub_label.pack(pady=1, padx=5, fill=tk.X)

                    for agent in agents:
                        agent_button = ctk.CTkButton(
                            agents_frame,
                            text=f"{agent.name}",
                            command=lambda a=agent: self.show_agent_details(a)
                        )
                        agent_button.pack(pady=1, fill=tk.X)
                        self.agent_buttons.append(agent_button)

                    # Initially collapse the sub-group
                    agents_frame.pack_forget()

                # Initially collapse the major group
                sub_levels_frame.pack_forget()

        self.root.after(0, update)

    def show_agent_details(self, agent):
        details = f"Name: {agent.name}\nTeam: {agent.team}\nExpertise: {agent.expertise}\nStatus: {agent.status}"
        messagebox.showinfo("Agent Details", details)

    def process_prompt(self):
        prompt = self.prompt_entry.get()
        if not prompt:
            messagebox.showwarning("Empty Prompt", "Please enter a prompt.")
            return
        
        threading.Thread(target=self.simulate_full_run, args=(prompt,), daemon=True).start()
        self.prompt_entry.delete(0, tk.END)
              
        #self.chat_display.insert(tk.END, f"User: {prompt}\n\n")
        #for agent in self.agents:
            #agent.status = "working"
            #self.update_agent_buttons(self)
            #self.display_agent_response(agent, prompt)
        #self.chat_display.see(tk.END)
        #self.prompt_entry.delete(0, tk.END)

    def display_agent_storm_response(self, agent, topic):
        def update():
            self.chat_display.insert(tk.END, f"AGENTSTORM in progress... ({agent.name})\n")
            self.chat_display.update()
            time.sleep(random.uniform(0.5, 1.0))  # Longer thinking time for more complex ideas
            self.chat_display.delete("end-2l", "end-1c")
            response = agent.storm_response(topic)  # New method for AGENTSTORM responses
            self.chat_display.insert(tk.END, f"{response}\n\n")
            self.chat_display.see(tk.END)
            
            observation = self.observer.observe(response)
            self.observer_display.insert(tk.END, f"AGENTSTORM Observation: {observation}\n\n")
            self.observer_display.see(tk.END)
            
            agent.status = "cooled down"
            self.update_agent_buttons()
            threading.Timer(7.0, self.set_agent_idle, [agent]).start()  # Longer cooldown period

        self.root.after(0, update)

    def set_agent_idle(self, agent):
        agent.status = "idle"
        self.update_agent_buttons()

    def toggle_agentstorm(self):
        if self.agentstorm_active:
            self.agentstorm_active = False
            self.agentstorm_button.configure(text="Start AGENTSTORM")
        else:
            self.agentstorm_active = True
            self.agentstorm_button.configure(text="Stop AGENTSTORM")
            threading.Thread(target=self.run_agentstorm, daemon=True).start()

    def run_agentstorm(self):
        topics = [
            "Innovative AI applications",
            "Blockchain integration in software",
            "Next-gen user interfaces",
            "Quantum computing implications",
            "Sustainable software practices"
        ]
        
        while self.agentstorm_active:
            topic = random.choice(topics)
            self.chat_display.insert(tk.END, f"AGENTSTORM topic: {topic}\n\n")
            for agent in self.agents:
                agent.status = "brainstorming"
                self.update_agent_buttons()
                self.display_agent_storm_response(agent, topic)
            time.sleep(random.uniform(5, 10))  # Longer wait between topics for more in-depth responses
        
        self.chat_display.insert(tk.END, "AGENTSTORM session concluded.\n\n")
        self.chat_display.see(tk.END)

    def add_task(self):
        add_task_window = ctk.CTkToplevel(self.root)
        add_task_window.title("Add Task")
        add_task_window.geometry("400x500")

        ctk.CTkLabel(add_task_window, text="Priority:").grid(row=0, column=0, pady=5)
        priority_var = tk.StringVar(value="Medium")
        priority_frame = ctk.CTkFrame(add_task_window)
        priority_frame.grid(row=0, column=1, pady=5)
        for i, priority in enumerate(["Low", "Medium", "High"]):
            ctk.CTkRadioButton(priority_frame, text=priority, variable=priority_var, value=priority).grid(row=0, column=i, padx=5)

        ctk.CTkLabel(add_task_window, text="Description:").grid(row=1, column=0, pady=5)
        description_entry = ctk.CTkEntry(add_task_window, width=300)
        description_entry.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(add_task_window, text="Team:").grid(row=2, column=0, pady=5)
        team_frame = ctk.CTkScrollableFrame(add_task_window, width=300, height=300)
        team_frame.grid(row=2, column=1, pady=5)

        team_vars = {role: tk.BooleanVar() for role in self.teams}
        grouped_teams = {}
        for team in self.teams:
            level = team.split()[1].split('-')[0]
            if level not in grouped_teams:
                grouped_teams[level] = []
            grouped_teams[level].append(team)

        for level, teams in grouped_teams.items():
            level_frame = ctk.CTkFrame(team_frame)
            level_frame.pack(fill=tk.X, pady=2)

            teams_frame = ctk.CTkFrame(level_frame)
            teams_frame.pack(fill=tk.X, padx=10)

            def toggle_level(frame=teams_frame):
                if frame.winfo_viewable():
                    frame.pack_forget()
                else:
                    frame.pack(fill=tk.X, padx=10)

            level_button = ctk.CTkButton(level_frame, text=f"Level {level}", command=toggle_level)
            level_button.pack(fill=tk.X)

            for team in teams:
                ctk.CTkCheckBox(teams_frame, text=team, variable=team_vars[team]).pack(anchor=tk.W)

            # Initially collapse the level
            teams_frame.pack_forget()

        def submit_task():
            priority = priority_var.get()
            description = description_entry.get()
            team = ",".join([role for role, var in team_vars.items() if var.get()])
            
            if not description or not team:
                messagebox.showwarning("Invalid Input", "Please enter a description and select at least one team member.")
                return
            
            task = Task(self.task_counter, priority, description, team)
            self.tasks.append(task)
            self.task_counter += 1
            self.update_tasks_display()
            add_task_window.destroy()
        
        ctk.CTkButton(add_task_window, text="Submit", command=submit_task).grid(row=3, column=0, columnspan=2, pady=10)
        
         # Configure the column weight before focusing the window
        add_task_window.grid_columnconfigure(1, weight=1)
    
        self.focus_window(add_task_window)

    def update_display(self, items, display_widget, item_type):
        for widget in display_widget.winfo_children():
            widget.destroy()
        
        count_label = getattr(self, f"{item_type}s_count_label")
        count_label.configure(text=f"{item_type.capitalize()}s({len(items)})")

        for i, item in enumerate(items):
            item_frame = ctk.CTkFrame(display_widget)
            item_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

            status_colors = {
                "Not Started": "gray",
                "In Progress": "yellow",
                "Completed": "green",
                "Failed": "red",
                "Unanswered": "gray",
                "Answered": "green"
            }

            item_button = ctk.CTkButton(
                item_frame,
                text=self.get_item_text(item, item_type),
                fg_color=status_colors[item.status],
                command=lambda i=item: self.show_item_details(i, item_type)
            )
            item_button.grid(row=0, column=0, sticky="ew")

            action_button = ctk.CTkButton(
                item_frame,
                text="Change Status" if item_type == "task" else "Answer",
                command=lambda i=item: self.change_item_status(i) if item_type == "task" else self.answer_question(i)
            )
            action_button.grid(row=0, column=1)

            delete_button = ctk.CTkButton(
                item_frame,
                text="Delete",
                command=lambda i=item: self.delete_item(i, item_type)
            )
            delete_button.grid(row=0, column=2)

            item_frame.grid_columnconfigure(0, weight=1)

        display_widget.grid_columnconfigure(0, weight=1)

    def get_item_text(self, item, item_type):
        if item_type == "task":
            return f"#{item.number} | {item.priority} | Team: {item.team} | Status: {item.status}"
        elif item_type == "question":
            return f"#{item.number} | Agent: {item.agent.name} | Status: {item.status}"

    def show_item_details(self, item, item_type):
        if item_type == "task":
            self.show_task_details(item)
        elif item_type == "question":
            self.show_question_details(item)

    def delete_item(self, item, item_type):
        if item_type == "task":
            self.tasks.remove(item)
        elif item_type == "question":
            self.questions.remove(item)
        self.update_display(getattr(self, f"{item_type}s"), getattr(self, f"{item_type}s_display"), item_type)

    def update_tasks_display(self):
        self.update_display(self.tasks, self.tasks_display, "task")

    def update_questions_display(self):
        self.update_display(self.questions, self.questions_display, "question")

    def delete_task(self, task):
        self.tasks.remove(task)
        self.update_tasks_display()

    def show_task_details(self, task):
        details = f"Task #{task.number}\nPriority: {task.priority}\nDescription: {task.description}\nTeam: {task.team}\nStatus: {task.status}"
        messagebox.showinfo("Task Details", details)

    def change_task_status(self, task):
        status_window = ctk.CTkToplevel(self.root)
        status_window.title("Change Task Status")
        status_window.geometry("300x200")

        status_var = tk.StringVar(value=task.status)
        for status in ["Not Started", "In Progress", "Completed", "Failed"]:
            ctk.CTkRadioButton(status_window, text=status, variable=status_var, value=status).pack(pady=5)

        def update_status():
            new_status = status_var.get()
            task.status = new_status
            # Update the corresponding tree node
            self.update_tree_node_status(task.description, new_status)
            self.update_tasks_display()
            status_window.destroy()

        ctk.CTkButton(status_window, text="Update", command=update_status).pack(pady=10)
        self.focus_window(status_window)

    def update_tree_node_status(self, task_description, new_status):
        def update_node(node):
            if node.content == task_description:
                node.update_status(new_status)
                return True
            for child in node.children:
                if update_node(child):
                    return True
            return False

        update_node(self.task_tree)

    # Add a progress bar GUI to to the task display to show task completion percentage.
    def update_task_progress(self):
        for task in self.tasks:
            if task.status == "In Progress":
                task.progress = random.randint(0, 100)
            else:
                task.progress = 100
        self.update_tasks_display()
        
    # Implement periodic updates to the task status based on agent progress.
    def collaborate_on_task(self, task):
        team_agents = [agent for agent in self.agents if agent.team in task.team.split(',')]
        for agent in team_agents:
            agent.handle_task(task)
        self.update_tasks_display()

    # Create a message passing system between teams to simulate information flow:
    def pass_message(self, from_team, to_team, message):
        self.chat_display.insert(tk.END, f"{from_team} to {to_team}: {message}\n\n")
        self.chat_display.see(tk.END)
        
 
    #Task Prioritization:
    # Implement a method to automatically adjust task priorities based on dependencies and completion status of other tasks.
    def prioritize_tasks(self):
        for task in self.tasks:
            if task.dependencies:
                dependencies_met = all(agent.status == "completed" for agent in self.agents if task.id in agent.dependencies)
                if not dependencies_met:
                    task.priority = "High"
                else:
                    task.priority = "Medium"
            else:
                task.priority = "Low"
        self.update_tasks_display()
        
    # Implement a method to automatically assign tasks to agents based on their Team and availability.
    def assign_tasks(self):
        for agent in self.agents:
            if agent.status == "idle":
                agent_tasks = [task for task in self.tasks if agent.team in task.team.split(',')]
                if agent_tasks:
                    agent.current_task = agent_tasks[0]
                    agent_tasks[0].status = "In Progress"
                    agent.status = "working"
        self.update_tasks_display()
        
    # Implement a method to automatically update task status based on agent progress.
    def update_task_status(self):
        for task in self.tasks:
            if task.status == "In Progress":
                agents_working = [agent for agent in self.agents if agent.status == "working"]
                if not agents_working:
                    task.status = "Completed"
                else:
                    task.status = "In Progress"
        self.update_tasks_display()
        
    # Implement a method to automatically generate a report of task status and completion.
    def generate_task_report(self):
        completed_tasks = [task for task in self.tasks if task.status == "Completed"]
        failed_tasks = [task for task in self.tasks if task.status == "Failed"]
        report = f"Task Report\n\nCompleted Tasks:\n"
        for task in completed_tasks:
            report += f"Task #{task.number} - {task.description}\n"
        report += "\nFailed Tasks:\n"
        for task in failed_tasks:
            report += f"Task #{task.number} - {task.description}\n"
        self.chat_display.insert(tk.END, f"{report}\n")
        self.chat_display.see(tk.END)
        
    #Implement a task queue for each team to manage multiple tasks.
    def manage_task_queue(self):
        for agent in self.agents:
            agent_tasks = [task for task in self.tasks if agent.team in task.team.split(',')]
            agent_tasks.sort(key=lambda task: task.priority)
            agent.task_queue = agent_tasks
            agent.current_task = None
            
             
if __name__ == "__main__":
    root = ctk.CTk()
    app = AgentGUI(root)
    root.mainloop()
