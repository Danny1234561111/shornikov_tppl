section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    y dd 0, 10, 1, 9, 2, 8, 5
    n equ 7  ; количество элементов в массивах
    sum dd 0
    mean dd 0
    out_file db 'out', 0

section .text
    global _start

_start:
    xor ecx, ecx  ; индекс i = 0
    xor ebx, ebx  ; сумма = 0

.loop:
    cmp ecx, n
    jge .done

    mov eax, [x + ecx*4]
    sub eax, [y + ecx*4]
    add ebx, eax
    inc ecx
    jmp .loop

.done:
    mov eax, ebx
    cdq
    idiv dword [n]
    mov [mean], eax

    mov eax, 5      ; sys_open
    mov ebx, out_file
    mov ecx, 1      ; O_WRONLY
    mov edx, 0
    int 0x80
    mov ebx, eax

    mov eax, 4      ; sys_write
    mov ecx, mean
    mov edx, 4
    int 0x80

    mov eax, 6      ; sys_close
    int 0x80

    mov eax, 1      ; exit
    xor ebx, ebx
    int 0x80
