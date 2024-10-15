import re
import argparse

# Function to load TLDs and second-level TLDs from file
def load_tlds(tld_file):
    tlds = set()
    print(f"Loading TLDs and second-level TLDs from {tld_file}...")
    with open(tld_file, 'r') as file:
        for line in file:
            tld = line.strip().lower()  # Normalize to lowercase
            if tld:
                tlds.add(tld)
    print(f"Loaded {len(tlds)} TLDs and second-level TLDs.\n")
    return tlds

# Function to extract root domains and show progress
def extract_root_domains(domain_file, tlds):
    root_domains = set()
    
    # Pre-compile the regex for extracting domain-like strings
    domain_pattern = re.compile(r'([a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+)')
    
    print(f"Processing domains from {domain_file}...\n")
    
    with open(domain_file, 'r') as file:
        total_lines = sum(1 for _ in open(domain_file, 'r'))  # Count total lines for progress
        file.seek(0)  # Reset file pointer after counting lines
        processed_lines = 0
        
        for line in file:
            processed_lines += 1
            
            # Find all domain-like strings in the line
            domains = domain_pattern.findall(line)
            
            for domain in domains:
                domain = domain.lower()  # Normalize domain to lowercase
                
                # Find the longest matching TLD or second-level TLD
                for tld in tlds:
                    if domain.endswith(tld):
                        # Extract the root domain (handle subdomains and TLDs/SLDs)
                        domain_parts = domain.split('.')
                        
                        # Check if it matches a second-level TLD (e.g., co.uk, com.ac)
                        if len(domain_parts) > 2 and tld.count('.') > 1:
                            root_domain = '.'.join(domain_parts[-(tld.count('.')+1):])
                        else:
                            # Extract the root domain as the last two parts
                            root_domain = '.'.join(domain_parts[-2:])  # Take the last two parts: domain and TLD
                        
                        root_domains.add(root_domain)
                        break  # Stop further checks after the match
            
            # Print progress after every 10 lines processed
            if processed_lines % 10 == 0 or processed_lines == total_lines:
                print(f"Processed {processed_lines}/{total_lines} lines. Root domains found: {len(root_domains)}", end='\r')

    print(f"\nProcessing complete. Found {len(root_domains)} root domains.\n")
    return root_domains

# Main function to tie everything together and save to file
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract root domains from a list of domains using custom TLD files.")
    parser.add_argument('-t', '--tld-file', type=str, required=True, help="File containing TLDs and second-level TLDs")
    parser.add_argument('-d', '--domain-file', type=str, required=True, help="File containing the list of domains to process")
    parser.add_argument('-o', '--output-file', type=str, default='root.txt', help="File to save the extracted root domains")

    args = parser.parse_args()
    
    # Load TLDs and second-level TLDs
    tlds = load_tlds(args.tld_file)
    
    # Extract root domains
    root_domains = extract_root_domains(args.domain_file, tlds)
    
    # Save the root domains to the specified output file
    print(f"Saving root domains to {args.output_file}...")
    with open(args.output_file, 'w') as f:
        for domain in root_domains:
            f.write(f"{domain}\n")
    
    print(f"Root domains successfully saved to {args.output_file}.")

if __name__ == "__main__":
    main()
