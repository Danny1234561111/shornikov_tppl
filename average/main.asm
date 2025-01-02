section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    y dd 0, 10, 1, 9, 2, 8, 5
    n equ 7  ; количество элементов в массивах
    sum dq 0
    mean dq 0
    out_file db 'out', 0

section .text
    global _start

_start:
    xor rcx, rcx  ; индекс i = 0
    xor rbx, rbx  ; сумма = 0

.loop:
    cmp rcx, n
    jge .done

    mov eax, [x + rcx*4]
    mov edx, [y + rcx*4]
    sub eax, edx
    add rbx, rax
    inc rcx
    jmp .loop

.done:
    mov rax, rbx
    idiv qword [n] ; правильное деление, без cqo
    mov [mean], rax

    ; syscall open
    mov rax, 2     ; sys_open
    mov rdi, out_file
    mov rsi, 0x2      ; O_WRONLY
    mov rdx, 0
    syscall
    mov rbx, rax

    ; syscall write
    mov rax, 1     ; sys_write
    mov rdi, rbx
    mov rsi, mean
    mov rdx, 8  ; Количество байтов для записи
    syscall

    ; syscall close
    mov rax, 3     ; sys_close
    mov rdi, rbx
    syscall

    ; exit
    mov rax, 60    ; sys_exit
    xor rdi, rdi
    syscall
