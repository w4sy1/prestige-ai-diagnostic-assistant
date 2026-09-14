import math

def normalize(report):
    if not isinstance(report,dict):raise ValueError('Raport musi być obiektem JSON.')
    found={};values={'disk_free_percent':[],'packet_loss':[],'defender_enabled':[],'critical_errors':[]}
    def visit(value,depth=0):
        if depth>20:raise ValueError('Zbyt głęboki raport.')
        if isinstance(value,dict):
            for key,item in value.items():
                canonical={'FreePercent':'disk_free_percent','AntivirusEnabled':'defender_enabled'}.get(key,key)
                if canonical in values:
                    if canonical=='defender_enabled':
                        if type(item) is not bool and item is not None:raise ValueError('Defender wymaga bool.')
                    elif item is not None:
                        if type(item) not in (int,float) or not math.isfinite(item) or item<0:raise ValueError('Nieprawidłowa liczba.')
                        if canonical!='critical_errors' and item>100:raise ValueError('Procent poza zakresem.')
                        if canonical=='critical_errors' and item!=int(item):raise ValueError('Liczba błędów musi być całkowita.')
                    if item is not None:values[canonical].append(item)
                elif isinstance(item,(dict,list)):visit(item,depth+1)
        elif isinstance(value,list):
            for item in value:visit(item,depth+1)
    visit(report)
    for key,items in values.items():
        if items:found[key]=all(items) if key=='defender_enabled' else min(items) if key=='disk_free_percent' else max(items)
    return found
