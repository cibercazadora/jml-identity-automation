import csv
import logging
from graph_users import create_user, update_user, deactivate_user

logging.basicConfig(
    filename='jml_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_hr_events(csv_file):
    results = {
        'created': 0,
        'updated': 0,
        'deactivated': 0,
        'failed': 0
    }

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                action = row['action'].lower()
                if action == 'create':
                    create_user(row)
                    results['created'] += 1
                elif action == 'update':
                    update_user(row)
                    results['updated'] += 1
                elif action == 'deactivate':
                    deactivate_user(row)
                    results['deactivated'] += 1
            except Exception as e:
                results['failed'] += 1
                logging.error(f"PROCESSING ERROR: {row.get('email')} - {str(e)}")

    print("\n--- JML Run Summary ---")
    print(f"Created:     {results['created']}")
    print(f"Updated:     {results['updated']}")
    print(f"Deactivated: {results['deactivated']}")
    print(f"Failed:      {results['failed']}")
    print("----------------------")

if __name__ == "__main__":
    process_hr_events('hr_events.csv')
