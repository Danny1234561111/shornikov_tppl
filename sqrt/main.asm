%macro save_regs 0
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    push rbp
%endmacro

%macro restore_regs 0
    pop rbp
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro

%macro syscall1 1
    mov rax, %1
    syscall
%endmacro

%macro mov_dword 2
    mov dword [%1], %2
%endmacro

%macro print_string 1
    mov rax, 1
    mov rdi, 1
    mov rsi, %1
    mov rdx, %1_len
    syscall
%endmacro

%macro print_decimal_macro 0
    save_regs
    mov rbx, 0          ; счетчик цифр
    mov rcx, 10         ; делитель для десятичной системы
divide_loop:
    xor rdx, rdx
    div rcx
    push rdx
    inc rbx
    cmp eax, 0
    jne divide_loop

print_loop:
    pop rax
    add al, '0'        ; преобразование в символ
    mov [output_buffer], al
    ; Вывод символа :
    mov rax, 1
    mov rdi, 1
    mov rsi, output_buffer
    mov rdx, 1
    syscall
    dec rbx
    cmp rbx, 0
    jg print_loop
    restore_regs
%endmacro

section .data
    input_num dd 144
    result   dq 0
    result_msg db "Result: ", 0
    result_msg_len equ $ - result_msg

section .text
    global _start

_start:
    ; Инициализация
    mov eax, dword [input_num]
    mov ebx, eax
    shr ebx, 1

.loop:
    ; x2 = (x1 + (num / x1)) // 2
    mov ecx, dword [input_num]
    mov eax, ecx
    mov edx, 0
    mov esi, ebx
    div esi
    add eax, ebx
    shr eax, 1
    mov edi, eax

    ; Сравниваем x1 и x2
    sub ebx, edi
    cmp ebx, 1
    jl .done
    mov ebx, edi
    jmp .loop

.done:
    mov_dword result, edi
    mov eax, edi
    print_decimal_macro

    print_string result_msg
    mov rax, 1               ; syscall write
    mov rdi, 1               ; stdout
    mov rsi, output_buffer
    mov rdx, 1               ; длина 1 байт
    syscall

    syscall1 60
    xor rdi, rdi
    syscall

section .bss
    output_buffer resb 1
