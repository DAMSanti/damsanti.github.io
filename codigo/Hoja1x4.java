package code.hoja1x4;

//////////////////////////////////////////////////////////////////////////////////////////////////
/////////           Santiago Manuel Tamayo Arozamena                                    //////////
/////////                       DAM 1 2023                                              //////////
/////////                      Programación                                             //////////
/////////     Tarea de definición de variables y asignación de valores                  //////////
//////////////////////////////////////////////////////////////////////////////////////////////////

    public class Hoja1x4 {
        enum Meses {ENERO,FEBRERO,MARZO,ABRIL,MAYO,JUNIO,JULIO,AGOSTO,SEPTIEMBRE,OCTUBRE,NOVIEMBRE,DICIEMBRE}

        public static void main(String[ ] args) {
            Meses m = Meses.MARZO;
            
            System.out.println("El mes seleccionado es: " + m);
            try {
                m = Meses.valueOf(MARZO);
                System.out.println("El mes seleccionado es: " + m);
            }
                catch (IllegalArgumentException e) {
                System.out.println("No se pudo asignar 'marzo' a la variable m, sigue siendo " + m);
            }
        }
    }