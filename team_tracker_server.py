import sqlite3
from typing import Optional
from fastmcp import FastMCP

mcp = FastMCP("Team Task Tracker")
DB_FILE = "team_tasks.db"

def get_db_connection():
    """Creates a database connection with row factory for easy dictionary access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database and tasks table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            assignee TEXT DEFAULT 'Unassigned',
            due_date TEXT DEFAULT 'Current Sprint',
            status TEXT DEFAULT 'Pending',
            remarks TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database table on startup
init_db()

@mcp.tool()
def add_task(
    title: str, 
    assignee: str = "Unassigned", 
    due_date: str = "Current Sprint", 
    status: str = "Pending", 
    remarks: str = ""
) -> str:
    """Add a new task with an assignee, sprint/timeline due date, status, and remarks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, assignee, due_date, status, remarks) VALUES (?, ?, ?, ?, ?)',
        (title, assignee, due_date, status, remarks)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return f"Task #{task_id} added successfully and assigned to {assignee}."

@mcp.tool()
def list_tasks(
    assignee: Optional[str] = None, 
    status: Optional[str] = None, 
    due_date: Optional[str] = None
) -> str:
    """List and filter tasks by optional parameters: assignee, status, or due_date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if assignee:
        query += " AND LOWER(assignee) = LOWER(?)"
        params.append(assignee)
    if status:
        query += " AND LOWER(status) = LOWER(?)"
        params.append(status)
    if due_date:
        query += " AND LOWER(due_date) = LOWER(?)"
        params.append(due_date)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No tasks match the specified filters or database is empty."
    
    result = []
    for r in rows:
        remarks_str = f" | Remarks: {r['remarks']}" if r["remarks"] else ""
        result.append(
            f"ID #{r['id']} | [{r['status'].upper()}] {r['title']} "
            f"-> Assigned: {r['assignee']} | Due: {r['due_date']}{remarks_str}"
        )
    return "\n".join(result)

@mcp.tool()
def update_task(
    task_id: int, 
    status: Optional[str] = None, 
    remarks: Optional[str] = None, 
    assignee: Optional[str] = None,
    due_date: Optional[str] = None
) -> str:
    """Update specific fields of an existing task (status, remarks, assignee, or due date)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if task exists first
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return f"Error: Task #{task_id} not found."
    
    # Build dynamic update query based on provided fields
    updates = []
    params = []
    
    if status is not None:
        updates.append("status = ?")
        params.append(status)
    if remarks is not None:
        updates.append("remarks = ?")
        params.append(remarks)
    if assignee is not None:
        updates.append("assignee = ?")
        params.append(assignee)
    if due_date is not None:
        updates.append("due_date = ?")
        params.append(due_date)
        
    if updates:
        params.append(task_id)
        cursor.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
        
    conn.close()
    return f"Task #{task_id} updated successfully."

@mcp.tool()
def delete_task(task_id: int) -> str:
    """Delete a task permanently using its numeric ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    
    if deleted_count == 0:
        return f"Error: Task #{task_id} not found."
    return f"Task #{task_id} deleted."

if __name__ == "__main__":
    mcp.run()
