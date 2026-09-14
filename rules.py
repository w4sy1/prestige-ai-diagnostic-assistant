def evaluate(metrics):
    alerts=[]
    def add(code,risk,evidence,reason,check):alerts.append({'code':code,'risk':risk,'evidence':evidence,'reason':reason,'what_to_check':check})
    disk=metrics.get('disk_free_percent')
    if disk is not None and disk<10:add('LOW_DISK','WYSOKIE' if disk<5 else 'ŚREDNIE',disk,'Mało wolnego miejsca może utrudniać aktualizacje i zapis.','Przejrzyj zajętość dysku i plan czyszczenia; nie usuwaj plików w ciemno.')
    loss=metrics.get('packet_loss')
    if loss is not None and loss>2:add('PACKET_LOSS','WYSOKIE' if loss>=10 else 'ŚREDNIE',loss,'Utrata odpowiedzi może oznaczać problem lub limitowanie ICMP.','Porównaj pomiary bramy, kilku hostów i połączenia kablowego.')
    if metrics.get('defender_enabled') is False:add('DEFENDER_DISABLED','WYSOKIE',False,'Defender nieaktywny; może działać inny antywirus.','Sprawdź rzeczywistego dostawcę ochrony i polityki.')
    if metrics.get('critical_errors',0)>0:add('SYSTEM_ERRORS','ŚREDNIE',metrics['critical_errors'],'Zarejestrowano błędy krytyczne.','Sprawdź czas, źródło i korelację z objawami w dzienniku Windows.')
    return alerts

def score(alerts):
    weights={'INFORMACYJNE':0,'NISKIE':5,'ŚREDNIE':15,'WYSOKIE':30,'KRYTYCZNE':50}
    return min(100,sum(weights[a['risk']] for a in alerts))
