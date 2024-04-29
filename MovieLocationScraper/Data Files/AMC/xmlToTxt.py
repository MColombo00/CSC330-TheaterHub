import xml.etree.ElementTree as ET

def extract_urls_from_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        urls = []
        for element in root.iter():
            if 'http' in element.text:
                urls.append(element.text.strip())
        return urls
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

def write_urls_to_text_file(urls, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write('\n'.join(urls))
            print(f"URLs written to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    xml_file = input("choose xml file: ")
    output_file = input("choose text file location: ")

    urls = extract_urls_from_xml(xml_file)
    write_urls_to_text_file(urls, output_file)

if __name__ == "__main__":
    main()
