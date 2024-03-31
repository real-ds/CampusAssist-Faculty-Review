import csv
#from google.colab import drive
import difflib
import spacy

# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

def extract_nouns_from_question(question):
    # Define a set of question words and the verb "is"
    question_words = {"where", "what", "how", "when", "who", "does", "is"}

    # Process the question using spaCy
    doc = nlp(question)

    # Extract tokens that are not question words or "is"
    nouns = [token.text for token in doc if token.text.lower() not in question_words and token.text.lower() != "is"]

    # Remove possessive marker "'s" from the remaining tokens
    nouns = [token[:-2] if token.endswith("'s") else token for token in nouns]

    return nouns

def tokenize_string(string):
    # Tokenize the string by splitting on spaces and removing punctuation
    return [token.strip(".,?!") for token in string.lower().split()]

def search_record_in_csv(name, csv_file_path, info_type):
    # Tokenize the input name
    name_tokens = tokenize_string(name)

    # Open the CSV file and search for the closest match
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        matches = []
        for row in reader:
            # Tokenize the name from the CSV file
            csv_name_tokens = tokenize_string(row['Name'])
            # Compute similarity using difflib's SequenceMatcher
            similarity = difflib.SequenceMatcher(None, name_tokens, csv_name_tokens).ratio()
            if similarity > 0.6:  # Adjust the threshold as needed
                matches.append((row, similarity))

        if matches:
            # Sort matches by similarity and return the closest match
            matches.sort(key=lambda x: x[1], reverse=True)
            found_record = matches[0][0]
            if info_type.lower() == 'cabin':
                return found_record['Cabin Location']
            elif info_type.lower() == 'email':
                return found_record['Email ID']
    return None

# Function to print CSV content
def print_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def main():
    # Mount Google Drive
    #drive.mount('/content/drive')

    csv_file_path = 'facdata - Sheet1 (1).csv'  # Update with your CSV file path
    #print_csv(csv_file_path)

    while True:
        question = input("Enter your question (type 'quit' to end): ")

        if question.lower() == 'quit':
            print("Program ended.")
            break

        # Extract the nouns from the question
        nouns = extract_nouns_from_question(question)
        if nouns:
            info_type = 'cabin'  # Default to cabin location
            if 'contact' in question.lower() or 'email' in question.lower():
                info_type = 'email'

            # Search for records in CSV based on extracted nouns
            for noun in nouns:
                found_info = search_record_in_csv(noun, csv_file_path, info_type)
                if found_info:
                    print(f"{info_type.capitalize()} found:")
                    print(found_info)
                    break  # Stop searching if info is found
            else:
                print(f"No {info_type} found for any noun in the question.")
        else:
            print("No relevant nouns found in the question.")

if __name__ == "__main__":
    main()
