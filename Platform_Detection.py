import platform
def Platform(): #stringa della piattaforma
    return platform.system()

def IsLinux(): #ritorna se la piattaforma è linux
    if platform.system() == "Linux": return True
    return False

def DoThisOnPlatform(platform,onTrue,args, onFalse = None, Fargs = None): #se piattaforma fai questo con questi parametri, opzionalmente fai questo altro, ritorna esito del paragone e azione
    if Platform() == platform:
        return True, onTrue(*args)
    elif (onFalse != None):
        return False, onFalse(*Fargs)
    return False