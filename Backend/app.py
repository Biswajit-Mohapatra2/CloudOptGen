from flask import Flask, request, jsonify
import boto3  # Add this line
from nlp import extract_requirements
from architecture import generate_diagram, estimate_cost_with_aws_api

app = Flask(__name__)

@app.route('/api/generate-diagram', methods=['POST'])
def generate_diagram_api():
  data = request.get_json()
  prompt = data['prompt']
  region = data['region']
  requirements = extract_requirements(prompt)
  diagram = generate_diagram(requirements, region)
  cost = estimate_cost_with_aws_api(diagram)
  response = { 'diagram': diagram, 'cost': cost }
  return jsonify(response)

# ... NLP logic (extract_requirements) and architecture generation logic (generate_diagram) implementations remain similar to previous examples

# Enhanced cost estimation with AWS API:
def estimate_cost_with_aws_api(diagram, region):
  total_cost = 0
  # Use boto3 libraries for different service cost estimation based on diagram and region
  # Example for EC2 with committed use discounts:
  ec2_client = boto3.client('ec2')
  for instance_info in diagram['instances']:
    price_data = get_ec2_price_with_cudp(ec2_client, instance_info['type'], region)
    total_cost += price_data['RecurringCharge']
  # Repeat similar logic for other services and consider scaling, usage patterns for advanced estimation
  return total_cost

# Function to retrieve EC2 pricing with potential committed use discounts:
def get_ec2_price_with_cudp(ec2_client, instance_type, region):
   # Get reserved instance offerings for the given instance type and region
  response = ec2_client.describe_reserved_instances_offerings(
    Filters=[
      {'Name': 'instance-type', 'Values': [instance_type]},
      {'Name': 'region', 'Values': [region]},
    ]
  )

  # Analyze response data for the most cost-effective offering with CUDP
  best_offering = None
  for offering in response['ReservedInstancesOfferings']:
    price_data = offering['RecurringCharges'][0]
    current_cost = price_data['RecurringCharge']
    # Check if offering has CUDP and compare cost with previous best
    if offering['OfferingType'] == 'CUDPOffering' and (not best_offering or current_cost < best_offering['price']):
      best_offering = {
        'price': current_cost,
        'CUDP': offering['CUDP']['Enabled'],
      }

  # If no CUDP offering found, check on-demand pricing
  if not best_offering:
    price_data = ec2_client.describe_prices(Filters=[
      {'Name': 'instanceType', 'Values': [instance_type]},
      {'Name': 'region', 'Values': [region]},
    ])['Prices'][0]
    best_offering = {'price': price_data['Price per Unit']['USD'], 'CUDP': False}

  return best_offering


if __name__ == '__main__':
    app.run(debug=True)

