from flask import Flask, request, jsonify
import torch
import re
import os

# Set environment variable to disable initializing empty weights
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

app = Flask(__name__)

# Global variables for model and tokenizer
model = None
tokenizer = None

# Define PII classes
classes_list = [
    '<pin>', '<api_key>', '<bank_routing_number>', '<bban>', '<company>',
    '<credit_card_number>', '<credit_card_security_code>', '<customer_id>',
    '<date>', '<date_of_birth>', '<date_time>', '<driver_license_number>',
    '<email>', '<employee_id>', '<first_name>', '<iban>', '<ipv4>',
    '<ipv6>', '<last_name>', '<local_latlng>', '<name>', '<passport_number>',
    '<password>', '<phone_number>', '<social_security_number>',
    '<street_address>', '<swift_bic_code>', '<time>', '<user_name>'
]

# Create prompt template
prompt_template = """You are an AI assistant who is responsible for identifying Personal Identifiable Information (PII). You will be given a passage of text and you have to \
identify the PII data present in the passage. You should only identify the data based on the classes provided and not make up any class on your own.

```PII Classes```
{classes}

The given text is:
{text}

The PII data are:
"""

def load_model_if_needed():
    """Load model and tokenizer if they're not already loaded"""
    global model, tokenizer
    
    if model is None or tokenizer is None:
        print("Loading model and tokenizer...")
        
        # Import inside function to avoid initialization errors
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        # Define device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Use specific parameters to avoid initialization issues
        tokenizer = AutoTokenizer.from_pretrained("betterdataai/PII_DETECTION_MODEL")
        model = AutoModelForCausalLM.from_pretrained(
            "betterdataai/PII_DETECTION_MODEL", 
            low_cpu_mem_usage=True,
            trust_remote_code=True
        ).to(device)
        print("Model and tokenizer loaded successfully!")

def detect_pii(text):
    """Function to detect PII in the given text"""
    # Ensure model is loaded
    load_model_if_needed()
    
    # Define device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Format the prompt with the classes and input text
    formatted_prompt = prompt_template.format(
        classes="\n".join(classes_list),
        text=text
    )

    # Tokenize the input
    tokenized_input = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    # Generate output with appropriate parameters
    with torch.no_grad():
        output = model.generate(
            **tokenized_input,
            max_new_tokens=1000,
            temperature=0.1,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode the output
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract just the PII part
    try:
        pii_data = generated_text.split("The PII data are:\n")[1].strip()
    except IndexError:
        # If splitting fails, return a message
        pii_data = "No PII detected or could not parse output"

    return pii_data

def parse_pii_output(pii_output):
    """Parse the PII output into a structured format"""
    pii_dict = {}

    # Use regex to find patterns like '<category> : ['value']'
    pattern = r'<([^>]+)>\s*:\s*\[(.*?)\]'
    matches = re.findall(pattern, pii_output, re.DOTALL)

    for category, values in matches:
        # Clean up the values (removing quotes, etc.)
        values_clean = re.findall(r"'([^']*)'", values)
        if values_clean:
            pii_dict[category] = values_clean

    return pii_dict

@app.route('/detect_pii', methods=['POST'])
def api_detect_pii():
    # Get data from request
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field in request'}), 400
    
    text = data['text']
    
    try:
        # Detect PII
        pii_output = detect_pii(text)
        
        # Parse into structured format
        structured_pii = parse_pii_output(pii_output)
        
        # Return results
        return jsonify({
            'raw_output': pii_output,
            'structured_pii': structured_pii
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)