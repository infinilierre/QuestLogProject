import sys
import shlex  
from questlog.manager import QuestLogManager

def execute_command(manager, args):
    """Routes the command to the correct manager function."""
    if not args:
        return
    
    primary_cmd = args[0].lower()

    try:
        if primary_cmd == "quest":
            sub_cmd = args[1].lower()
            if sub_cmd == "list":
                for i, q in enumerate(manager.quests, 1):
                    print(f"{i}. {q.name}")
            
            elif sub_cmd == "view":
                quest = manager.find_quest(args[2])
                if quest:
                    print(f"Quest: {quest.name}\nRequired Items:")
                    for item, qty in quest.items.items():
                        print(f"- {item}: {qty}")
            
            elif sub_cmd == "gap":
                gaps = manager.get_gap(args[2])
                if gaps:
                    print(f"Missing items for '{args[2]}':")
                    for item, qty in gaps.items():
                        print(f"- {item}: {qty}")
                else:
                    print(f"No missing items for '{args[2]}'.")
            
            elif sub_cmd == "complete":
                manager.complete_quest(args[2])
                print(f"Successfully completed '{args[2]}'.")

        elif primary_cmd == "inventory":
            sub_cmd = args[1].lower()
            if sub_cmd == "add":
                manager.inventory.add_item(args[2], int(args[3]))
                manager.save_inventory()
                print(f"Added {args[3]} of {args[2]} to inventory.")
            
            elif sub_cmd == "process":
                manager.process_batch_file(args[2])
                print(f"Batch processing complete. See '{manager.config['report_file']}' for results.")

        elif primary_cmd == "plan":
            print("Completable Quests:")
            found_any = False
            for q in manager.quests:
                if manager.can_complete(q):
                    print(f"- {q.name}")
                    found_any = True
            if not found_any:
                print("- No quests are currently completable.")

        else:
            print(f"Unknown command: {primary_cmd}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    
    try:
        manager = QuestLogManager("config.json")
    except Exception as e:
        print(f"Failed to start application: {e}")
        return

   
    if len(sys.argv) > 1 and sys.argv[1] == "manage":
        print("--- QuestLog Interactive Mode ---")
        print("Type 'exit' to quit.")
        while True:
            try:
                user_input = input("> ").strip()
                if not user_input or user_input.lower() == "exit":
                    print("Inventory saved. Goodbye!")
                    break
                
                
                command_parts = shlex.split(user_input)
                execute_command(manager, command_parts)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Input error: {e}")
    else:
        
        execute_command(manager, sys.argv[1:])

if __name__ == "__main__":
    main()