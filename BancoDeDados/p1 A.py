from abc import ABC, abstractmethod


class DispositivosInteligentes(ABC):
   
    @abstractmethod
    def __init__(self, local):
        self.local = local 
        self.estado =False
       
        pass
    
    @abstractmethod
    def exibir_estado (self,exibir):
        
        pass
    
    @abstractmethod
    def liga(self,ligar ):

        pass
    
    @abstractmethod
    def desliga(self, desligar):
        
        pass
    
class Lampada(DispositivosInteligentes):
   
    def __init__(self, local):
        super().__init__(local)
        self.intensidade = 0

    def ligar_lamp(self):
        self.estado = True
        return f"a lampada no(a) {self.local} esta ligada "
    
    def deligar_lamp(self):
        self.estado = False
        self.intesidade=0
        return f"a lampada no(a) {self.local} esta desligada "
    def ajustar_intensidade (self,intensidade:int):
        
        
        if self.estado:
            
            if (0<=intensidade<=100):
                self.intesidade = intensidade
                return{
                    f"intesidade ajustada para{intensidade}"
                }
            else: 
                return{f"intesidade invalida, por favor de 0 a 100"}
        else:
            return "Não é possível ajustar a intensidade: a lâmpada está desligada."
    
    
    def exibir_estado_lamp(self):
     return f"a lampada esta no(a) {self.local} {'ligada'if self.estado else'desligada'} com a intensidade de {self.intensidade}"   
   
  
class ArCondicionado(DispositivosInteligentes):
    
    def __init__(self, local):
        super().__init__(local)
        self.temperatura= 21

    def ligar_ar(self):
        self.estado =True
        return f" o ar-condicionado no(a) {self.local} esta ligado"    
    def deligar_ar(self,desligar):
        self.estado=  False
        self.temperatura= 21 
        return f"o ar-condicionado no(a) {self.local} esta desligado"
        
    def temperatura_do_ar (self,temperatura:int):
        if self.estado:
            if(15<=temperatura<=30):
                self.temperatura = temperatura
                return{f"a temperatura foi ajustada para {temperatura}C"}
            else:
                return{"temperatura invalida de 15c a 30C "}
        
        else:
            return "Não é possível ajustar a temperatura: o ar-condicionado está desligado."

              
 
    def exibir_estado(self):
        return f"o ar-condicionado esta no(a) {self.local} {'ligado'if self.estado else'desligado'} com a temperatura de {self.temperatura}C"
    
    
lampada_do_quarto = Lampada("quarto")  
ligar_lampada= lampada_do_quarto.ligar_lamp()
ajuste_intensidade= lampada_do_quarto.ajustar_intensidade(80)
desligar_lampada= lampada_do_quarto.deligar_lamp()
estado_da_lampada= lampada_do_quarto.exibir_estado_lamp()

ar_condicionado= ArCondicionado("sala")
ligar_arcondicionado= ar_condicionado.ligar_ar()
ajuste_temperatura= ar_condicionado.temperatura_do_ar(23)
desligar_ar_condicionado= ar_condicionado.deligar_ar()
estado_do_ar_condicionado= ar_condicionado.exibir_estado()

resultado= {
    "lampada":{

        "ligar lampada":ligar_lampada,
        "intensidade da lampada":ajuste_intensidade,
        "desligar lampada":desligar_lampada,
        "estado da lampada":estado_da_lampada

    }  ,
    "ar-condicionado":{

       "ligar ar-condicionado":ligar_arcondicionado,
        "intensidade do ar-condicionado":ajuste_temperatura,
        "desligar ar-condicionado":desligar_ar_condicionado,
        "estado do ar-condicionado":estado_do_ar_condicionado
    }      
}
for dispositivo, operacoes in resultado.items():
    print(f"\n{dispositivo}:")
    for operacao, resultado in operacoes.items():
        print(f"{operacao}: {resultado}")

    
    
    
    
    