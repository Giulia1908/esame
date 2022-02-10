class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    
    def __init__(self, name):
        self.name = name

        # Provo ad aprire e leggere una riga del file
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except:        
            self.can_read = False

    
    def get_data(self):

        # se il fine non può essere aperto o è illeggibile alzo un'eccezione
        if not self.can_read: 
            raise ExamException('Errore, file non aperto o illeggibile')

        else:
            #creo una lista di liste -> ogni sottolista sarà: ['anno-mese', numpasseggeri]
            listaliste = []       
            my_file= open(self.name, 'r')   #apro e leggo il file
            anno_prima=None     #inizializzo l'anno e il mese prima a None
            mese_prima=None

            for line in my_file:    #scorro il file
                elements=line.split(',')    # split() restituisce un array di sottostringhe risultanti dalla divisione della stringa originale 
                elements[-1] = elements[-1].strip()     #con la funzione strip rimuovo il carattere newline(\n)da tutte le linee e gli spazi bianchi all'inizio e alla fine della striga
                #-----------------------------------------------------------------------
                try:
                    elements[1]=int(elements[1]) #il mese può essere convertito 
                    m_a=elements[0].split('-')
                    anno=int(m_a[0])
                    mese=int(m_a[1])                  
                except:         
                    continue    #se non posso eseguire le azioni nel try, passo alla linea successiva
                #-------------------------------------------------------------------------
                
                #controllo che la lunghezza della lista mese-anno non sia maggiore di 2, altrimenti passo alla linea successiva
                if len(m_a)>2:   
                    continue   

                #controllo che i mesi abbiano un valore compreso tra 0 e 12, altrimenti passo alla linea successiva    
                if mese<1 or mese>12:
                    continue

                # controllo che gli anni e i mesi siano in ordine cronologico 
                if anno_prima==None:   #caso base
                    anno_prima=anno
                    mese_prima=mese
                else:
                    if anno_prima<anno:     #caso 1: se l'anno precedente è minore dell'anno della linea
                        anno_prima=anno
                        mese_prima=mese
                    elif anno_prima==anno:   #caso 2: se l'anno precedente è uguale dell'anno della linea
                        if mese_prima<mese:   
                            mese_prima=mese
                        else:
                            raise ExamException('la lista non è in ordine cronologico')
                    else:                 #caso 3: se l'anno precedente è maggiore dell'anno della linea
                        raise ExamException('la lista non è in ordine cronologico')

                listaliste.append(elements)

            my_file.close()
            return listaliste



def compute_avg_monthly_difference(time_series, first_year, last_year):
    #controllo che first_year e last_year siano di tipo striga
    if isinstance(first_year, str)==False:
       raise ExamException('il primo anno non è di tipo stringa')
    if isinstance(last_year, str)==False:
       raise ExamException('l ultimo anno non è di tipo stringa')

    #trasformo in interi first_year e last_year
    try:
        primo=int(first_year)
        ultimo=int(last_year)
    except:
        raise ExamException('first_year e last_year non sono convertibili in interi')
    
    #controllo che first_year e last_year siano presenti nel file
    flag_1=False
    flag_2=False
    for line in time_series:
        data=line[0].split('-')
        anno=int(data[0])
        if anno==primo:  
            flag_1=True
        if anno==ultimo: 
            flag_2=True

    if flag_1==False and flag_2==False:
        raise ExamException('i valori di first_year e last_year non sono presenti nel file')         
    elif flag_1==False:
        raise ExamException('il valore di first_year non è presente nel file')
    elif flag_2==False:
        raise ExamException('il valore di last_year non è presente nel file')
     

    #controllo che il primo anno sia minore del secondo 
    elif last_year<=first_year:
        raise ExamException('first_year  è maggiore o uguale di last_year')
    

    lista = fill(time_series)      #inizializzo una lista che contiene tutti di dati 
    #------------------------------------------------------------------------------------------------------------
    #stampo anno : [numero passeggeri per ogi mese]
    #questa parte non influisce sul calcolo della media, potrebbe essere tranquillamente cancellata
    g=0      #posizione di gennaio del primo anno
    d=12     #posizione di gennaio dell'anno 
    for j in range(primo, ultimo+1):
        l=lista[g:d]
        g=d
        d=d+12
        #print(j,':',l) 
    #--------------------------------------------------------------------------------------------------------------
    
    b=time_series[0]     #b=['anno-mese']
    a=b[0].split('-')    #a=['anno']
    first_y = int(a[0])   #first_y=anno
    
    differenza=primo-first_y     

    #creo una lista che contiene la variazione media nel numero di passeggeri per ogni mese
    media=[]
    for i in range(12):    #per la posizione di ogni mese...
        somma=0
        c=False
        x=ultimo-primo
        for j in range(ultimo-primo):   
            if lista[differenza*12+(j*12)+i] == None:    #se l'elemento del mese è nullo...
                x = x-1 

            elif  lista[differenza*12+(j*12)+12+i]==None:     #se l'elemento dello stesso mese ma dell'anno successivo è nullo...
                x=x-1
                lista[differenza*12+(j*12)+12+i]=lista[differenza*12+(j*12)+i]  #il mese dell'anno successivo diventa quello dell'anno corrente
            else:
                #calcollo la sommatoria delle differenze
                somma=somma+(lista[differenza*12+(j*12)+12+i]-lista[differenza*12+(j*12)+i])     #esempio: (gennaio_1950-gennaio_1949)+...+...
                c=True
        if c == True:
            med=somma/x
            media.append(med)
        else:
            media.append(0)  #se non è possibile 
                   
    return media

# creo una funzione che mette None dove i dati nel file sono mancanti
def fill (lista):
    #controlo che il file non sia vuoto, se è vuoto alzo un'eccezione
    if len(lista)==0:
        raise ExamException('il file è vuoto')

    a = lista[-1]     #prendo l'ultimo elemento della lista
    b = a[0].split('-')  #b=['ultimo_anno-ultimo_mese']
    last_y = int(b[0])    #last_y =ultimo_anno
    last_m = int(b[1])    #last_m =ultimo_mese

    ip_anno = None    #anno precedente
    ip_mese = None    #mese precedente

    result = []  #creo una lista vuota che conterrà tutti dati e None dove essi sono mancanti

    counter = True 
    i=0
    k=True

    while counter == True:
        try:    #provo a dividere la prima riga 
            line = lista[i]
            data = line[0].split('-')
            anno = int(data[0])
            mese = int(data[1])
        except:
            pass   #se non è possibile passo alla successiva

        if ip_anno == None:    #caso base
            ip_anno = anno     #la variabile è uguale al primo anno
            ip_mese = 1        # // è uguale al primo mese (posizione di gennaio)
        else:            
            if last_y == ip_anno and ip_mese == 12:   #caso in cui arrivo a dicembre dell'ultimo anno 
                if k == True:
                    result.append(line[1])
                else:
                    result.append(None)     #se l'ultimo elemento dell'ultimo anno manca, metto None
                counter = False 

            elif last_y == ip_anno and last_m <= ip_mese:    #caso in cui  mi trovo nell'ultimo anno e a un mese minore o uguale all'ultimo
                if ip_mese == mese and ip_anno == anno:     
                    result.append(line[1])
                else:
                    result.append(None)     
                k = False  

            elif ip_mese == mese and ip_anno == anno:
                result.append(line[1])
                i = i + 1

            else:
                result.append(None)

            ip_mese = ip_mese + 1 #passo alla posizione del mese successivo

            if ip_mese == 13:  
                ip_mese = 1      #torno alla posizione del primo mese(gennaio)
                ip_anno = ip_anno + 1   #passo all'anno successivo

    return result
