import json
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

def lambda_handler(event, context):    
    url = 'https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv'
    df = pd.read_csv(url)
    engine = create_engine('sqlite://', echo=False)
    df.to_sql('ign', engine, index=False)
    
    def test_query(query, expected_query):
        try:
            user_result = engine.execute(query).fetchall()
            expected_result = engine.execute(expected_query).fetchall()

        except Exception as e:
            return e
        return user_result == expected_query

    try:
        editable = event['editable']
        userToken = event['userToken']
        hidden = event['hidden']
        shown = event['shown']

        is_correct = test_query(editable, hidden)
    except:
        editable = 'EMPTY'
        
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "isComplete": is_correct,
                "jsonFeedback": { "test": is_correct },
                "htmlFeedback": "<div>Test: " + str(is_correct) + "</div><div>" + str(editable) + "</div>",
                "textFeedback": "Test result: " + str(is_correct) + "\n" + str(editable),
            }
        )
    }

