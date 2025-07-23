from text_processor import TextCalendar
from table_generator import TableCalendar

def main():
    # Initialize processors
    text_processor = TextCalendar()
    table_generator = TableCalendar()
    
    try:
        # Process the text file
        events = text_processor.process_text('data/sample_texts.txt', input_type="file")
        
        # Generate and print table
        table = table_generator.generate_table(events)
        print(table)
        
    except FileNotFoundError:
        print("Error: sample_texts.txt file not found in data directory")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 