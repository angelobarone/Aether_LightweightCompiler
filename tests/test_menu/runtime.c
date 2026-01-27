#include <stdio.h>
#include <stdint.h>

int64_t show_menu() {
    printf("\n--- CALCOLATRICE MINILANG ---\n");
    printf("1. Addizione (+)\n");
    printf("2. Sottrazione (-)\n");
    printf("3. Moltiplicazione (*)\n");
    printf("4. Divisione (/)\n");
    printf("5. Esci\n");
    printf("Scegli un'operazione: ");
    return 0;
}

int64_t get_input() {
    long long n;
    scanf("%lld", &n);
    return (int64_t)n;
}

int64_t print_prompt() {
    printf("Inserisci numero: ");
    return 0;
}

int64_t print_result(int64_t n) {
    printf(">> RISULTATO: %ld\n", n);
    return 0;
}

int64_t print_dash(int64_t n) {
    printf("-");
    return 0;
}

int64_t print_error(int64_t n){
    if(n == -9999){
        printf("Codice non valido");
    }
    if (n == -222){
        printf("Stai chiedendo di uscire");
    }
    if (n == -111){
        printf("Programma avviato");
    }
    return 0;
}