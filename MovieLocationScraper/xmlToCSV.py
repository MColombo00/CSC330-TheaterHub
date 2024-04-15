import xml.etree.ElementTree as ET

def extract_urls_from_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        urls = []
        for element in root.iter():
            if 'http' in element.text:
                urls.append(element.text)
        return urls
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

def write_urls_to_text_file(urls, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(','.join(urls))
            print(f"URLs written to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    xml_file = input("Enter the path to the XML file: ")
    output_file = input("Enter the path to the output text file: ")

    urls = extract_urls_from_xml(xml_file)
    write_urls_to_text_file(urls, output_file)

if __name__ == "__main__":
    main()
