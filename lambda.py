import boto3
import requests
import re
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    # URL of the page to scrape
    url = "https://www.pplelectric.com/site/Ways-to-Save/Rates-and-Shopping"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Use the correct selector based on your earlier determination
    rate_text = soup.select_one('your_selector').text
    
    # Parse the price
    pattern = r"\b(\d+\.\d{3})¢/kWh\b"
    match = re.search(pattern, rate_text)
    if match:
        rate = match.group(1)
    else:
        rate = "No match found"
    
    # Save the rate to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PPandLPrices')
    table.put_item(
       Item={
            'date': context.aws_request_id,  # Using AWS request ID as a unique identifier for simplicity
            'rate': rate
        }
    )
    return {
        'statusCode': 200,
        'body': f"Successfully saved rate: {rate}"
    }
