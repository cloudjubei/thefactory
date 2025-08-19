import sys
import os

# Add scripts directory to path to allow import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../scripts')))

def run():
    print("Executing migration script as part of test_13_8...")
    
    try:
        # It's better to import here after path modification
        import migrate_tasks
        migrate_tasks.main()
        print("PASS: Migration script executed successfully.")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: Migration script execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run()
