Overview
CampusCurrency is a terminal-based personal expense tracker built specifically for university students, with a focus on international students managing money in a new country. Users are allowed to record, organise, and reflect on their daily spending, with all data saved automatically between sessions.

How Expenses Are Recorded :
Each expense captures four pieces of information:
Date - filled automatically using today's date
Category - selected from a fixed numbered menu
Amount - validated to reject non-numeric input
Description - a short personal note for context

How Expenses Are Categorised : 
Expenses are grouped into categories designed around real student spending habits: Food & Groceries, Transport, Rent & Utilities, Textbooks & Supplies, Entertainment, Health, and Other. These fixed number of categories ensures consistency across the entries, keeping the summaries and analysis accurate.

How Expenses Are Stored :
Expenses will be held in memory using a 2D list while the program runs. Every time an expense is added or deleted, the list is written to a CSV file and when the program starts again, it reads the file back into memory, so data persists permanently between sessions.

Data Analysis : 
Three layers of analysis:
1. View All Expenses - displays the full history in a formatted, numbered table.
2. Spending Summary by Category & Donut chart display - totals spending per category and displays a grand total, helping users identify where most of their money is going.
3. Monthly Budget Tracker with Warnings - the user sets a monthly budget, and the program filters expenses to the current month, calculates remaining balance, displays percentage used, and triggers tiered warning messages (over budget, close to limit, or on track).

Advanced Topics Implemented as follows : 
File I/O - database.py .
Multi-Dimensional Lists - all expenses are stored as a 2D list and iterated for display, summary, and budget calculations.
Concepts also includes Classes & Objects, Functions, Loops, Conditionals, and Dictionaries.
 
Project Scope & Value: 
CampusCurrency is designed to remove friction from expense tracking and provide actionable insight, especially for International students navigating unfamiliar costs while studying in a new country. The budget warning system creates a feedback loop that encourages reflection before overspending, and persistent file storage builds a real spending history over time without any manual effort from the user.
