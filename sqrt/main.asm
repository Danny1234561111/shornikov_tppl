%macro save_regs 0
    push rax
    push rbx
    push rcx
    push rdx
%endmacro

%macro restore_regs 0
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro

%macro output 2
    save_regs
    mov rax, 1          ; номер системного вызова для вывода
    mov rdi, 1          ; дескриптор stdout
    mov rsi, %1         ; указатель на данные
    mov rdx, %2         ; длина данных
    syscall
    restore_regs
%endmacro

%macro print_decimal 0
    save_regs
    mov rbx, 0          ; счетчик цифр
    mov rcx, 10         ; делитель для десятичной системы
divide_loop:
    xor rdx, rdx
    div rcx
    push rdx
    inc rbx
    cmp rax, 0
    jne divide_loop

print_loop:
    pop rax
    add rax, '0'        ; преобразование в символ
    mov [output_buffer], al
    output output_buffer, 1
    dec rbx
    cmp rbx, 0
    jg print_loop
    restore_regs
%endmacro

section .text
global _start

_start:
    mov eax, dword [input_num]
    mov dword [first_num], eax
    mov dword [first_den], 2

calculate:
    xor rax, rax
    mov eax, dword [input_num]
    mul dword [first_den]
    mul dword [first_den]
    mov dword [second_num], eax

    mov eax, dword [first_num]
    mul dword [first_num]
    add dword [second_num], eax

    mov eax, dword [first_num]
    mul dword [first_den]
    mov rcx, 2
    mul rcx
    mov dword [second_den], eax

    mov eax, dword [second_num]
    div dword [second_den]
    mov dword [second_num], eax
    mov dword [second_den], 1

check_condition:
    mov eax, dword [second_num]
    mul dword [first_den]
    mov edx, eax
    mov eax, dword [first_num]
    sub eax, edx
    cmp eax, dword [first_den]
    jl finish

update_values:
    mov edx, dword [second_num]
    mov [first_num], edx
    mov edx, dword [second_den]
    mov [first_den], edx
    jmp calculate

finish:
    mov eax, dword [second_num]
    print_decimal
    output newline_char, newline_length
    output completion_msg, msg_length
    output newline_char, newline_length
    mov rax, 60         ; системный вызов для выхода
    xor rdi, rdi
    syscall

section .data
input_num dd 256

completion_msg db 'Completed', 0xA, 0xD
msg_length equ $ - completion_msg
newline_char db 0xA, 0xD
newline_length equ $ - newline_char

section .bss
output_buffer resb 1
first_num resd 1
first_den resd 1
second_num resd 1
second_den resd 1
