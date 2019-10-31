import json
import boto3


def lambda_handler(event, context):    
    is_correct = False
    status_code_ok = 200
    invokeLambda = boto3.client('lambda', region_name="us-east-1")

    method = event.get('httpMethod',{})
    if method == 'GET':
        with open('index.html', 'r') as f:
            return {
                "statusCode": status_code_ok,
                "headers": {
                'Content-Type': 'text/html',
                },
                "body": f.read()
            }

    invoke_response = None
    response = None
    method = event.get('httpMethod',{})
    if method == 'POST':
        postReq = json.loads(event.get('body', {}))
        try:
            
            editable = postReq["editable"]["0"].strip()
            userToken = postReq["userToken"].strip()
            hidden = postReq["hidden"]["0"].strip()
            shown = postReq["shown"]["0"].strip()

            payload = {
                "userToken": userToken, 
                "editable": editable,
                "hidden": hidden,
                "shown": shown,
            }
            
            response = invokeLambda.invoke(
                FunctionName='is5003_lambda_with_sql',
                InvocationType='RequestResponse',
                Payload = json.dumps(payload),
            )
            
            data = json.loads(response['Payload'].read().decode('utf-8'))
            body = json.loads(data['body'])
            
            is_correct = body['isComplete']
                
        except Exception as e:
            print(e)
            shown = "EMPTY"
            userToken = "EMPTY"
            
        return {
            'statusCode': status_code_ok,
            'body': json.dumps(
                {
                    "isComplete": is_correct,
                    "jsonFeedback": { "test": is_correct },
                    "htmlFeedback": "<div>Test: " + str(is_correct) + "</div><div>" + str(postReq) + "</div>",
                    "textFeedback": "Test result: " + str(is_correct) + "\n" + str(postReq),
                }
            )
        }

