import xml.etree.ElementTree as ET
import pandas as pd
import sys
import logging

# Configure logging
logging.basicConfig(filename='xml_parser_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_xml(xml_file):
    try:
        # Parse XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        data = []

        # Iterate over all ECUC-CONTAINER-VALUE elements
        for container in root.findall('.//{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE'):
            # Extract SHORT-NAME and DEFINITION-REF
            short_name = container.find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
            definition_ref = container.find('.//{http://autosar.org/schema/r4.0}DEFINITION-REF').text
            data.append({'Short Name': short_name, 'Definition Ref': definition_ref})

            # Iterate over all ECUC-CONTAINER-VALUE elements within each container
            for sub_container in container.findall('.//{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE'):
                # Extract SHORT-NAME and DEFINITION-REF for sub-containers
                sub_short_name = sub_container.find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                sub_definition_ref = sub_container.find('.//{http://autosar.org/schema/r4.0}DEFINITION-REF').text
                data.append({'Short Name': sub_short_name, 'Definition Ref': sub_definition_ref})

        return data
    except Exception as e:
        # Handle exceptions during XML parsing
        error_msg = f"Error parsing XML file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        return []

def generate_excel(data, output_path):
    try:
        if not data:
            # Warn if there's no data to create Excel file
            error_msg = "No data to create Excel file."
            logging.warning(error_msg)
            print(error_msg)
            return

        # Create DataFrame from the extracted data and save to Excel file
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        success_msg = f"Excel file created successfully: {output_path}"
        logging.info(success_msg)
        print(success_msg)
    except Exception as e:
        # Handle exceptions during Excel file generation
        error_msg = f"Error creating Excel file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

def cli_mode(xml_file, output_path):
    # Parse XML file and generate Excel file in CLI mode
    data = parse_xml(xml_file)
    generate_excel(data, output_path)


if __name__ == "__main__":
    # Check if script is run in CLI mode
    if len(sys.argv) != 3:
        # Display usage message if arguments are incorrect
        print("Usage: python script.py <xml_file> <output_path>")
        sys.exit(1)
    cli_mode(sys.argv[1], sys.argv[2])
