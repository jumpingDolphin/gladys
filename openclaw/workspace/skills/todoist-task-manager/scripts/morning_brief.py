import sys
import json
import datetime
import os
import subprocess

def get_brief():
    # Load env for token
    token = os.environ.get('TODOIST_PERSONAL_TOKEN')
    if not token:
        return "Erreur : TODOIST_PERSONAL_TOKEN non trouvé."

    # Fetch data from API v1
    cmd = [
        "curl", "-s", "-X", "POST", "https://api.todoist.com/api/v1/sync",
        "-H", f"Authorization: Bearer {token}",
        "-d", "sync_token=*&resource_types=[\"items\",\"projects\"]"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
    except Exception as e:
        return f"Erreur lors de l'appel API : {e}"

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    inbox_project_id = '6fxjfC8p5mX2mWGW'
    gladys_project_id = '6fxjfVH63x9xg5G7'

    tasks_to_show = []
    items = data.get('items', [])
    projects = {p['id']: p['name'] for p in data.get('projects', [])}

    for item in items:
        if item.get('checked') or item.get('is_deleted'):
            continue
        
        # Rule 1: Everything in Inbox
        if item.get('project_id') == inbox_project_id:
            tasks_to_show.append(item)
            continue
            
        # Rule 2: Due today (excluding Gladys project)
        if item.get('due') and item['due']['date'].startswith(today) and item.get('project_id') != gladys_project_id:
            if item not in tasks_to_show:
                tasks_to_show.append(item)

    if not tasks_to_show:
        return "Rien de prévu aujourd'hui dans ton Inbox ou avec une échéance immédiate. Profites-en !"

    brief = [f"Bonjour Simon ! Voici ton brief matinal ({len(tasks_to_show)} tâches) :\n"]
    for task in tasks_to_show:
        p_name = projects.get(task['project_id'], 'Inbox')
        due_tag = " [Aujourd'hui]" if task.get('due') and task['due']['date'].startswith(today) else ""
        brief.append(f"• {task['content']}{due_tag} ({p_name})")
    
    return "\n".join(brief)

if __name__ == "__main__":
    print(get_brief())
