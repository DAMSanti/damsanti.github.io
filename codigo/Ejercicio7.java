package unidad1.ejercicio7;

//////////////////////////////////////////////////////////////////////////////////////////////////
/////////           Santiago Manuel Tamayo Arozamena                                    //////////
/////////                       DAM 1 2023                                              //////////
/////////                      Programación                                             //////////
/////////                Ejercicios de los apuntes                                      //////////
////////////////////////////////////////////////////////////////////////////////////////////////// 

import java.util.Scanner;

    public class Ejercicio7 {
        public static void main(String[] args) {
            
            // Creamos objeto teclado
            Scanner teclado = new Scanner(System.in);
            
            boolean llueve, tarea, biblioteca;
            String solucion;
            
            // Entrada de datos 
            System.out.println("Escribe solo \"true\" o \"false\"");
            System.out.print("¿Esta lloviendo? ");
            llueve=teclado.nextBoolean();
            System.out.print("¿Has terminado las tareas? ");
            tarea=teclado.nextBoolean();
            System.out.print("¿Tienes que ir a la biblioteca? ");
            biblioteca=teclado.nextBoolean();


            solucion = ((biblioteca == true) || (llueve!=tarea) && (tarea==true)) ? "" : "No" ;
            System.out.print(solucion + " Puedes salir a la calle ");
    }
}
