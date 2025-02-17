# EXAMPLE FUNCTION FOR READING API KEYS
# IT ASSUMES THAT THEY ARE SAVED IN THE FILE file_name WITH THE FORMAT:

# PUBLIC_KEY=reCRG76Jhd2
# PRIVATE_KEY=zUB4AbFf47yz4v



import os

def read_api_keys(file_name):
    
    key_file = file_name
    
    proj_dir = os.path.abspath(os.path.dirname(''))
    file_path = os.path.join(proj_dir, key_file)
    
    keys = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line: 
                    key, value = line.strip().split('=', 1)
                    keys[key] = value

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error: {e}")
        
    return keys

keys = read_api_keys("TAK.txt")
public_key = keys.get('PUBLIC_KEY')
private_key = keys.get('PRIVATE_KEY')
