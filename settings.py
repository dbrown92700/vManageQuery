import dotenv
from cryptography.fernet import Fernet
import os
from getpass import getpass

# To generate new key use the python Fernet.generate_key()
setting_key = b'6VrUb_qjs0a0m8RbUmlbBinIblpjmeME4Iuf3-LiSOU='
configdir = os.path.abspath(__file__).removesuffix('/settings.py')


# Function either retrieves the setting value from the environment "variable"
# or prompts the user with "prompt" for the value if it doesn't exist.
# Secret can be set to True or False to hide input and encrypt the stored variable.
def get_setting(variable, prompt, secret=False):
    dotenv.load_dotenv(f'{configdir}/.env')
    try:
        response = os.environ[variable]
        if secret:
            print(f'{variable} = ########')
            response = Fernet(setting_key).decrypt((response.encode('ascii'))).decode('ascii')
        else:
            print(f'{variable} = {response}')
    except KeyError:
        if secret:
            response = getpass(prompt)
            dotenv.set_key(f'{configdir}/.env', variable,
                           Fernet(setting_key).encrypt(bytes(response, 'ascii')).decode('ascii'))
        else:
            response = input(prompt)
            dotenv.set_key(f'{configdir}/.env', variable, response)
    return response


print('Settings:')

vmanage_add = get_setting('VMANAGE_ADDRESS', 'Input vManage Address: ', False)
print(vmanage_add)
vmanage_user = get_setting('VMANAGE_USER', 'Input vManage Username: ', False)
vmanage_password = get_setting('VMANAGE_PASSWORD', 'Input vManage Password: ', True)

if input('Type "reset" to clear the settings, or anything else to proceed: ') == 'reset':
    os.remove(f'{configdir}/.env')
    print('Restart script to enter new settings.\n')
    exit()
