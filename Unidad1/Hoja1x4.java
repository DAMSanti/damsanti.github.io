package code.hoja1x4;

//////////////////////////////////////////////////////////////////////////////////////////////////
/////////           Santiago Manuel Tamayo Arozamena                                    //////////
/////////                       DAM 1 2023                                              //////////
/////////                      Programación                                             //////////
/////////     Tarea de definición de variables y asignación de valores                  //////////
//////////////////////////////////////////////////////////////////////////////////////////////////

    public class Hoja1x4 {
        enum Meses {enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre}

        public static void main(String[ ] args) {
            Meses m = Meses.marzo;
            System.out.println("El mes seleccionad es: " + m);
            try {
                m = Meses.valueOf("MARZO");
                System.out.println("El mes seleccionad es: " + m);
            }
                catch (IllegalArgumentException e) {
                System.out.println("No se pudo asignar 'MARZO' a la variable m, sigue siendo " + m);
            }
        }
    }