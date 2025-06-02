import shutil
from colored import Fore, Back, Style

from verify import get_good_folders

good_folders = get_good_folders()

print(good_folders)

for folder in good_folders:
    try:
        shutil.move(f"{folder}", f"!GOOD_AUDIO/{folder}")
        print(f"{Fore.green}Done! The directory [{folder}] was moved to [!GOOD_AUDIO/{folder}].{Style.reset}")
    except Exception as error:
        print(f"{Fore.red}Error! The directory [{folder}] wasn't moved.{Style.reset}")