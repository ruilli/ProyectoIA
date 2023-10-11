import matplotlib.pyplot as plt
from pomegranate import *
from pomegranate import Node
def Incertidumbre(n,m,b):
    if b>=0 and b<=0.3:
        var3="ninguna"
    elif b>0.3 and b<0.6:
        var3="suave"
    elif b>=0.6 and b<=1:
        var3="fuerte"
    MomentoDia=["Mañana","Tarde","Noche"]
    lluvia=["Si","No"]
    var1=MomentoDia[n]#input momento de dia
    var2=lluvia[m]#input lluvia si,no
    momento_del_dia = Node(DiscreteDistribution({
        'Mañana': 1/3,
        'Tarde': 1/3,
        'Noche': 1/3
    }), name='momento_del_dia')

    intencidad_de_lluvia = Node(DiscreteDistribution({
        'ninguna': 1/3,
        'suave': 1/3,
        'fuerte': 1/3
    }), name='intencidad_de_lluvia')

    retraso = Node(ConditionalProbabilityTable([

        ["Mañana","ninguna","si",0],["Mañana","ninguna","no",1],
        ["Tarde","ninguna","si",0],["Tarde","ninguna","no",1],
        ["Noche","ninguna","si",0],["Noche","ninguna","no",1],
        ["Mañana","suave","si",0.2],["Mañana","suave","no",0.8],
        ["Tarde","suave","si",0.8],["Tarde","suave","no",0.2],
        ["Noche","suave","si",0.1],["Noche","suave","no",0.9],
        ["Mañana","fuerte","si",0.2],["Mañana","fuerte","no",0.8],
        ["Tarde","fuerte","si",0.8],["Tarde","fuerte","no",0.2],
        ["Noche","fuerte","si",0.1],["Noche","fuerte","no",0.9],
    ],[momento_del_dia.distribution, intencidad_de_lluvia.distribution]), name="retraso")

    modelo = BayesianNetwork("Red Bayesiana de Rutas")
    modelo.add_states(momento_del_dia,retraso,intencidad_de_lluvia)
    #Añadimos bordes que conecten nodos
    modelo.add_edge(momento_del_dia, retraso)
    modelo.add_edge(intencidad_de_lluvia, retraso)
    #Modelo Final
    modelo.bake()
    # Calculemos las predicciones
    predicciones = modelo.predict_proba({
        "momento_del_dia":var1,
        "intencidad_de_lluvia":var3
    })
    # Visualizemos las predicciones para cada nodo
    for nodo, prediccion in zip(modelo.states, predicciones):
        if isinstance(prediccion, str):
            print(f"{nodo.name}: {prediccion}")
        else:
            for valor, probabilidad in prediccion.parameters[0].items():
                if valor =="si":
                    b=probabilidad
    #Nodo trafico/ depende de MomentoDia y lluvia
    trafico=0
    if var1=="Tarde" and var2=="No":
        trafico="Alto"; print("TardeNo")
    elif var1=="Tarde" and var2=="Si":
        trafico="Medio";print("Tardesi")
    elif var1=="Mañana" and var2=="No":
        trafico="Medio";print("MañanaNo")
    elif var1=="Mañana" and var2=="Si":
        trafico="Leve";print("MañanaSi")
    elif var1=="Noche" and var2=="No":
        trafico="Medio";print("NocheNo")
    elif var1=="Noche" and var2=="Si":
        trafico="Leve";print("NocheSi")
    #Nodo semaforo/ depende de MomentoDia y trafico
    semaforo=0
    if var1=="Tarde" and trafico=="Leve":
        semaforo=120+(120*b); print("S+Tarde+Traficoleve")
    elif var1=="Tarde" and trafico=="Medio":
        semaforo=250+(250*b); print("S+Tarde+Trafimedio")
    elif var1=="Tarde" and trafico=="Alto":
        semaforo=500+(500*b); print("S+Tarde+Trafialto")
    elif var1=="Mañana" and trafico=="Leve":
        semaforo=50+(50*b); print("S+Mañana+Traficoleve")
    elif var1=="Mañana" and trafico=="Medio":
        semaforo=200+(200*b); print("S+Mañana+Trafimedio")
    elif var1=="Mañana" and trafico=="Alto":
        semaforo=400+(400*b); print("S+Mañana+Trafialto")
    elif var1=="Noche" and trafico=="Leve":
        semaforo=50+(50*b); print("S+Noche+Traficoleve")
    elif var1=="Noche" and trafico=="Medio":
        semaforo=200+(200*b); print("S+Noche+Trafimedio")
    elif var1=="Noche" and trafico=="Alto":
        semaforo=400+(400*b); print("S+Noche+Trafialto")
    #Nodo accidente/ depende de lluvia y trafico
    accidente=0
    if var2=="Si" and trafico=="Leve":
        accidente=3000; print("A+S+Traficoleve")
    elif var2=="Si" and trafico=="Medio":
        accidente=4500; print("A+S+Trafimedio")
    elif var2=="Si" and trafico=="Alto":
        accidente=9000; print("A+S+Trafialto")
    elif var2=="No" and trafico=="Leve":
        accidente=1000+(2000*b); print("A+S+Traficoleve")
    elif var2=="No" and trafico=="Medio":
        accidente=2000+(2000*b); print("A+S+Trafimedio")
    elif var2=="No" and trafico=="Alto":
        accidente=4500+(4500*b); print("A+S+rafialto")
    #nodo trencon/depende de trafico
    trancon=0
    if trafico=="Leve":
        trancon=300+(300*b); print("T+Traficoleve")
    elif trafico=="Medio":
        trancon=750+(750*b); print("T+Traficomedio")
    elif trafico=="Alto":
        trancon=1500+(1500*b); print("T+Traficoalto")
    return [semaforo, accidente, trancon]

    