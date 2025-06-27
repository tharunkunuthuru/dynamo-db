import json
import os
import base64
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-creds.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def lambda_handler(event, context):
    for record in event['Records']:
        event_name = record['eventName']
        new_image = record.get('dynamodb', {}).get('NewImage', {})
        old_image = record.get('dynamodb', {}).get('OldImage', {})

        # Convert DynamoDB JSON format to regular dict
        def parse_dynamodb_json(ddb_item):
            parsed_item = {}
            for key, value_dict in ddb_item.items():
                value_type, value = next(iter(value_dict.items()))
                if value_type == 'S':
                    parsed_item[key] = value
                elif value_type == 'N':
                    parsed_item[key] = float(value) if '.' in value else int(value)
                elif value_type == 'BOOL':
                    parsed_item[key] = value
                else:
                    parsed_item[key] = value  # default fallback
            return parsed_item

        if event_name == 'INSERT':
            item = parse_dynamodb_json(new_image)
            db.collection('machines').document(item['id']).set(item)
            print(f"INSERTED: {item}")

        elif event_name == 'MODIFY':
            item = parse_dynamodb_json(new_image)
            db.collection('machines').document(item['id']).set(item, merge=True)
            print(f"MODIFIED: {item}")

        elif event_name == 'REMOVE':
            item = parse_dynamodb_json(old_image)
            db.collection('machines').document(item['id']).delete()
            print(f"DELETED: {item['id']}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processed DynamoDB Stream event.')
    }
