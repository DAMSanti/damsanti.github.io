package unidad1.ejercicio8;

//////////////////////////////////////////////////////////////////////////////////////////////////
/////////           Santiago Manuel Tamayo Arozamena                                    //////////
/////////                       DAM 1 2023                                              //////////
/////////                      Programación                                             //////////
/////////                Ejercicios de los apuntes                                      //////////
////////////////////////////////////////////////////////////////////////////////////////////////// 

import java.util.Scanner;

    public class Ejercicio8 {
        public static void main(String[] args) {
            
            // Creamos objeto teclado
            Scanner teclado = new Scanner(System.in);
            
            final double premanz = 2.35, prepera = 1.95 ;
            double manzana, pera ;
            
            // Entrada de datos 
            System.out.print("Cuantos kilos de manzanas se vendieron el primer semestre:  ");
            manzana=teclado.nextDouble();
            System.out.print("Cuantos kilos de manzanas se vendieron el segundo semestre:  ");
            manzana=teclado.nextDouble() + manzana ;
            System.out.print("\nCuantos kilos de peras se vendieron el primer semestre:  ");
            pera=teclado.nextDouble();
            System.out.print("Cuantos kilos de peras se vendieron el segundo semestre:  ");
            pera=teclado.nextDouble() + pera ;
            
            System.out.print("\nLos beneficios anuales son de:  " + ( manzana * premanz + pera * prepera) );
            
    }
}
