from flask import Flask, request, render_template
import csv

app = Flask(__name__)

def load_drug_data():
    """Load drug data from the CSV file."""
    drugs = []
    with open('drugs.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            drugs.append(row)
    return drugs

def load_disease_data():
    """Load disease data from the CSV file."""
    diseases = []
    with open('disease.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            diseases.append(row)
    return diseases

@app.route('/', methods=['GET', 'POST'])
def index():
    drug_info = None
    disease_info = None
    drugs = load_drug_data()

    if request.method == 'POST':
        user_option = request.form['option']
        user_input = request.form['input_data'].strip().lower()

        if user_option == 'drug_info':
            # Check for drug information
            for drug in drugs:
                if user_input == drug['Drug Name'].strip().lower():
                    drug_info = drug
                    break

        elif user_option == 'disease_prediction':
            # Check for disease prediction
            diseases = load_disease_data()
            for disease in diseases:
                symptoms = disease['Symptoms'].split(', ')
                if any(symptom.lower() in user_input for symptom in symptoms):
                    disease_info = disease
                    break

            # If a disease is found, recommend drugs for that disease
            if disease_info:
                recommended_drugs = []
                disease_name = disease_info.get('Disease', '')  # Use 'Disease' instead of 'Disease Name'
                
                if disease_name:  # Only proceed if the 'Disease' exists
                    for drug in drugs:
                        indications = drug.get('Indications (Uses)', '')  # Get Indications safely
                        
                        # Ensure 'Indications (Uses)' is a valid string and contains the disease name
                        if indications and disease_name.lower() in indications.lower():
                            recommended_drugs.append(drug)
                
                # Return the disease and recommended drugs information
                return render_template('index.html', disease_info=disease_info, drugs=recommended_drugs)

    return render_template('index.html', drug_info=drug_info, disease_info=disease_info)

if __name__ == '__main__':
    app.run(debug=True)

