from colorama import Fore, Style, init
init()

print(Fore.RED + "❌ Esto es un error" + Style.RESET_ALL)
print(Fore.GREEN + "✅ Esto es un éxito" + Style.RESET_ALL)
print("Esto debería ser texto normal")